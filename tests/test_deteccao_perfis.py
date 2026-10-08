import ast
import os
from pathlib import Path
import tempfile
import unittest


RAIZ = Path(__file__).resolve().parents[1]


def carregar_detector():
    # Carrega apenas a lógica de detecção, sem abrir a GUI nem acessar o jogo.
    nomes = {
        "ler_configuracao_perfil", "bdo_valido", "obter_bin64_bdo",
        "listar_modos", "detectar_perfil_instalado", "identificar_modo_instalado",
    }
    arvore = ast.parse((RAIZ / "BDO_Mode_Manager.pyw").read_text(encoding="utf-8"))
    arvore.body = [no for no in arvore.body
                   if isinstance(no, ast.FunctionDef) and no.name in nomes]
    contexto = {"os": os, "NOME_ARQUIVO": "dxvk.conf"}
    exec(compile(arvore, "detector", "exec"), contexto)
    return contexto


class DeteccaoPerfisTests(unittest.TestCase):
    def setUp(self):
        self.temporario = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporario.cleanup)
        self.raiz = Path(self.temporario.name)
        self.bin64 = self.raiz / "jogo" / "bin64"
        self.bin64.mkdir(parents=True)
        self.modos = self.raiz / "modos"
        self.modos.mkdir()
        self.detector = carregar_detector()
        self.detector.update(PASTA_BDO=str(self.bin64.parent), PASTA_MODOS=str(self.modos))

    def perfil(self, nome, texto):
        pasta = self.modos / nome
        pasta.mkdir(exist_ok=True)
        (pasta / "dxvk.conf").write_bytes(texto.encode("utf-8"))

    def instalar(self, texto):
        (self.bin64 / "dxvk.conf").write_bytes(texto.encode("utf-8"))

    def detectar(self):
        return self.detector["detectar_perfil_instalado"]()

    def test_perfis_do_projeto_com_lf_crlf_e_bom(self):
        for nome in ("Normal", "Batata"):
            texto = (RAIZ / "game_modes" / nome / "dxvk.conf").read_text(encoding="utf-8")
            self.perfil(nome, texto.replace("\n", "\r\n"))
        for nome in ("Normal", "Batata"):
            with self.subTest(nome=nome):
                texto = (RAIZ / "game_modes" / nome / "dxvk.conf").read_text(encoding="utf-8")
                self.instalar("\ufeff" + texto)
                self.assertEqual(self.detectar()[0], nome)

    def test_perfil_arbitrario_com_formatacao_diferente(self):
        self.perfil("Meu perfil", "dxvk.enableAsync = True\ndxvk.hud = fps\n")
        self.instalar("# Outro comentário\n\ndxvk.hud=fps\n dxvk.enableAsync=true \n")
        self.assertEqual(self.detectar()[0], "Meu perfil")

    def test_mudanca_real_nao_e_reconhecida(self):
        self.perfil("Meu perfil", "dxvk.hud = fps\n")
        self.instalar("dxvk.hud = frametimes\n")
        self.assertEqual(self.detectar(), (None, "Configuração personalizada ou desconhecida"))

    def test_opcao_comentada_nao_e_ativa(self):
        self.perfil("Normal", "# d3d11.disableMsaa = True\n")
        self.instalar("d3d11.disableMsaa = True\n")
        self.assertIsNone(self.detectar()[0])

    def test_perfis_equivalentes_nao_escolhem_primeiro(self):
        self.perfil("A", "dxvk.hud=fps\n")
        self.perfil("B", "dxvk.hud = fps\n")
        self.instalar("dxvk.hud=fps\n")
        self.assertEqual(self.detectar(), (None, "Perfis equivalentes: A, B"))

    def test_arquivo_ausente(self):
        self.assertEqual(self.detectar(), (None, "Sem configuração instalada"))

    def test_configuracao_invalida_nao_e_ignorada(self):
        for texto in ("linha inválida", "dxvk.hud=fps\ndxvk.hud=frametimes"):
            with self.subTest(texto=texto):
                self.instalar(texto)
                self.assertEqual(self.detectar(), (None, "Configuração ilegível ou inválida"))

    def test_valor_textual_preserva_maiusculas(self):
        self.perfil("A", "dxvk.hud=FPS\n")
        self.instalar("dxvk.hud=fps\n")
        self.assertIsNone(self.detectar()[0])


if __name__ == "__main__":
    unittest.main()
