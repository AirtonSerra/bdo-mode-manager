import ast
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import Mock


class ProtecaoJogoAbertoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        raiz = Path(self.temp.name)
        self.bin64 = raiz / "jogo" / "bin64"
        self.bin64.mkdir(parents=True)
        modos = raiz / "modos"
        (modos / "Teste").mkdir(parents=True)
        (modos / "Teste" / "dxvk.conf").write_text("novo", encoding="utf-8")
        (self.bin64 / "dxvk.conf").write_text("original", encoding="utf-8")
        (self.bin64 / "d3d11.dll").write_bytes(b"original dll")
        self.scope = {
            "os": os, "shutil": shutil, "messagebox": Mock(),
            "PASTA_BDO": str(self.bin64.parent), "PASTA_MODOS": str(modos),
            "NOME_ARQUIVO": "dxvk.conf",
        }
        script = Path(__file__).resolve().parents[1] / "BDO_Mode_Manager.pyw"
        arvore = ast.parse(script.read_text(encoding="utf-8"))
        arvore.body = [no for no in arvore.body if isinstance(no, ast.FunctionDef)]
        exec(compile(arvore, "app", "exec"), self.scope)
        self.scope.update(
            listar_processos_windows=Mock(return_value={"BlackDesert64.exe"}),
            validar_bin64_programa=Mock(return_value=(True, "")),
            listar_dlls_programa=Mock(return_value=["d3d11.dll"]),
            aplicar_dlls=Mock(return_value=([], [])),
            atualizar_modo_instalado=Mock(),
        )

    def assert_preservado(self):
        self.assertEqual((self.bin64 / "dxvk.conf").read_text(), "original")
        self.assertEqual((self.bin64 / "d3d11.dll").read_bytes(), b"original dll")
        self.assertFalse((self.bin64 / "dxvk.conf.bdm_backup").exists())

    def test_aplicar_bloqueado(self):
        self.scope["trocar_modo"]("Teste")
        self.assert_preservado()
        self.scope["aplicar_dlls"].assert_not_called()
        self.scope["messagebox"].showwarning.assert_called_once()

    def test_remover_bloqueado_antes_da_confirmacao(self):
        self.scope["desinstalar"]()
        self.assert_preservado()
        self.scope["messagebox"].askyesno.assert_not_called()

    def test_jogo_aberto_durante_confirmacao(self):
        self.scope["listar_processos_windows"].side_effect = [set(), {"blackdesert64.bin"}]
        self.scope["messagebox"].askyesno.return_value = True
        self.scope["desinstalar"]()
        self.assert_preservado()

    def test_falha_de_consulta_bloqueia_ambas_operacoes(self):
        self.scope["listar_processos_windows"].side_effect = OSError("falha")
        self.scope["trocar_modo"]("Teste")
        self.scope["desinstalar"]()
        self.assert_preservado()
        self.assertEqual(self.scope["messagebox"].showerror.call_count, 2)

    def test_aplicar_com_jogo_fechado(self):
        self.scope["listar_processos_windows"].return_value = {"explorer.exe"}
        self.scope["trocar_modo"]("Teste")
        self.assertEqual((self.bin64 / "dxvk.conf").read_text(), "novo")
        self.scope["aplicar_dlls"].assert_called_once()

    def test_remover_com_jogo_fechado(self):
        self.scope["listar_processos_windows"].return_value = set()
        self.scope["messagebox"].askyesno.return_value = True
        self.scope["desinstalar"]()
        self.assertFalse((self.bin64 / "dxvk.conf").exists())
        self.assertFalse((self.bin64 / "d3d11.dll").exists())


if __name__ == "__main__":
    unittest.main()
