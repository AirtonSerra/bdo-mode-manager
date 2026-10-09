import ast
import json
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest


class ConfiguracaoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.programa = root / 'app'
        self.programa.mkdir()
        self.dados = root / 'dados'
        self.config = self.dados / 'config.json'
        script = Path(__file__).resolve().parents[1] / 'BDO_Mode_Manager.pyw'
        tree = ast.parse(script.read_text(encoding='utf-8'))
        tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                     and node.name in {'carregar_pasta_bdo_salva', 'salvar_pasta_bdo'}]
        self.ctx = dict(os=os, json=json, sys=SimpleNamespace(frozen=False),
                        PASTA_PROGRAMA=str(self.programa), PASTA_DADOS=str(self.dados),
                        ARQUIVO_CONFIG=str(self.config))
        exec(compile(tree, 'configuracao', 'exec'), self.ctx)

    def test_cria_dados_fora_da_instalacao(self):
        self.ctx['salvar_pasta_bdo']('C:/Jogos/BDO')
        self.assertEqual(self.ctx['carregar_pasta_bdo_salva'](), 'C:/Jogos/BDO')
        self.assertFalse((self.programa / 'config.json').exists())

    def test_migra_configuracao_antiga(self):
        (self.programa / 'config.json').write_text('{"pasta_bdo": "C:/BDO"}')
        self.assertEqual(self.ctx['carregar_pasta_bdo_salva'](), 'C:/BDO')
        self.assertTrue(self.config.is_file())

    def test_configuracao_atual_tem_prioridade(self):
        self.ctx['salvar_pasta_bdo']('C:/Novo')
        (self.programa / 'config.json').write_text('{"pasta_bdo": "C:/Antigo"}')
        self.assertEqual(self.ctx['carregar_pasta_bdo_salva'](), 'C:/Novo')

    def test_migra_ao_lado_do_executavel(self):
        self.ctx['sys'] = SimpleNamespace(frozen=True, executable=str(self.programa / 'app.exe'))
        self.ctx['PASTA_PROGRAMA'] = str(self.programa / '_internal')
        (self.programa / 'config.json').write_text('{"pasta_bdo": "C:/BDO"}')
        self.assertEqual(self.ctx['carregar_pasta_bdo_salva'](), 'C:/BDO')

    def test_configuracao_corrompida_ou_tipo_invalido(self):
        self.dados.mkdir()
        for content in ('{', '[]', '{"pasta_bdo": 123}'):
            with self.subTest(content=content):
                self.config.write_text(content)
                self.assertEqual(self.ctx['carregar_pasta_bdo_salva'](), '')
