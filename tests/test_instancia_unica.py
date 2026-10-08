import ast
import ctypes
from ctypes import wintypes
from pathlib import Path
import subprocess
import sys
import time
import unittest
import uuid


def carregar_bloqueio():
    script = Path(__file__).resolve().parents[1] / "BDO_Mode_Manager.pyw"
    arvore = ast.parse(script.read_text(encoding="utf-8"))
    nomes = {"adquirir_instancia_unica", "liberar_instancia_unica", "ativar_janela_existente"}
    arvore.body = [no for no in arvore.body
                   if isinstance(no, ast.FunctionDef) and no.name in nomes]
    contexto = {"ctypes": ctypes, "wintypes": wintypes, "time": time}
    exec(compile(arvore, "instancia", "exec"), contexto)
    return contexto


@unittest.skipUnless(sys.platform == "win32", "Mutex nativo do Windows")
class InstanciaUnicaTests(unittest.TestCase):
    def setUp(self):
        self.nome = "Local\\BDOModeManager.Test." + uuid.uuid4().hex
        self.contexto = carregar_bloqueio()
        self.adquirir = self.contexto["adquirir_instancia_unica"]
        self.liberar = self.contexto["liberar_instancia_unica"]

    def test_segunda_instancia_bloqueada(self):
        handle = self.adquirir(self.nome)
        try:
            self.assertIsNotNone(handle)
            self.assertIsNone(self.adquirir(self.nome))
        finally:
            self.liberar(handle)

    def test_reabrir_depois_de_fechar(self):
        primeiro = self.adquirir(self.nome)
        self.liberar(primeiro)
        segundo = self.adquirir(self.nome)
        try:
            self.assertIsNotNone(segundo)
        finally:
            self.liberar(segundo)

    def test_bloqueio_entre_processos(self):
        codigo = (
            "import runpy,sys; "
            "c=runpy.run_path(sys.argv[1])['carregar_bloqueio'](); "
            "h=c['adquirir_instancia_unica'](sys.argv[2]); "
            "print('ready',flush=True); input(); "
            "c['liberar_instancia_unica'](h)"
        )
        processo = subprocess.Popen(
            [sys.executable, "-c", codigo, str(Path(__file__).resolve()), self.nome],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True,
        )
        try:
            self.assertEqual(processo.stdout.readline().strip(), "ready")
            self.assertIsNone(self.adquirir(self.nome))
            processo.communicate("\n", timeout=5)
            self.assertEqual(processo.returncode, 0)
            handle = self.adquirir(self.nome)
            try:
                self.assertIsNotNone(handle)
            finally:
                self.liberar(handle)
        finally:
            if processo.poll() is None:
                processo.kill()
            processo.communicate()


if __name__ == "__main__":
    unittest.main()
