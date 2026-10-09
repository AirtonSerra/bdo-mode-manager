import ast
from pathlib import Path
import queue
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


class BuscaInicialTests(unittest.TestCase):
    def setUp(self):
        script = Path(__file__).resolve().parents[1] / 'BDO_Mode_Manager.pyw'
        tree = ast.parse(script.read_text(encoding='utf-8'))
        names = {'executar_busca_bdo', 'concluir_busca_bdo',
                 'acompanhar_busca_bdo', 'iniciar_busca_bdo', 'inicializar_bdo'}
        tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                     and node.name in names]
        self.ctx = dict(queue=queue, time=SimpleNamespace(monotonic=lambda: 100),
                        threading=Mock(), PASTA_BDO='', BUSCA_EM_ANDAMENTO=False,
                        COR_TEXTO_SECUNDARIO='gray')
        for name in ('janela', 'loader_busca', 'botao_selecionar', 'botao_desinstalar',
                     'status_var', 'status_label', 'modo_var', 'carregar_pasta_bdo_salva',
                     'bdo_valido', 'procurar_bdo', 'salvar_pasta_bdo', 'atualizar_status',
                     'criar_botoes_modos', 'atualizar_modo_instalado'):
            self.ctx[name] = Mock()
        exec(compile(tree, 'busca', 'exec'), self.ctx)

    def test_iniciar_agenda_busca_sem_executar_io_na_thread_da_janela(self):
        self.ctx['iniciar_busca_bdo']()
        self.ctx['carregar_pasta_bdo_salva'].assert_not_called()
        self.ctx['procurar_bdo'].assert_not_called()
        self.ctx['threading'].Thread.return_value.start.assert_called_once()
        self.ctx['botao_selecionar'].config.assert_called_with(state='disabled')
        self.ctx['botao_desinstalar'].config.assert_called_with(state='disabled')
        self.ctx['loader_busca'].start.assert_called_once()
        self.ctx['janela'].after.assert_called_once()

    def test_inicializacao_com_path_salvo_nao_exibe_loader_nem_inicia_busca(self):
        self.ctx['carregar_pasta_bdo_salva'].return_value = 'C:/BDO'
        self.ctx['bdo_valido'].return_value = True
        self.ctx['inicializar_bdo']()
        self.assertEqual(self.ctx['PASTA_BDO'], 'C:/BDO')
        self.ctx['loader_busca'].start.assert_not_called()
        self.ctx['loader_busca'].pack.assert_not_called()
        self.ctx['threading'].Thread.assert_not_called()
        self.ctx['procurar_bdo'].assert_not_called()
        self.ctx['botao_selecionar'].config.assert_called_with(state='normal')

    def test_inicializacao_com_path_movido_inicia_busca_com_loader(self):
        self.ctx['carregar_pasta_bdo_salva'].return_value = 'C:/Antigo'
        self.ctx['bdo_valido'].return_value = False
        self.ctx['inicializar_bdo']()
        self.ctx['loader_busca'].start.assert_called_once()
        self.ctx['threading'].Thread.return_value.start.assert_called_once()

    def test_inicializacao_sem_configuracao_inicia_busca_com_loader(self):
        self.ctx['carregar_pasta_bdo_salva'].return_value = ''
        self.ctx['inicializar_bdo']()
        self.ctx['loader_busca'].start.assert_called_once()

    def test_path_salvo_valido_e_reutilizado_sem_varrer_discos(self):
        results = queue.Queue()
        self.ctx['carregar_pasta_bdo_salva'].return_value = 'C:/BDO'
        self.ctx['bdo_valido'].return_value = True
        self.ctx['executar_busca_bdo'](results)
        self.assertEqual(results.get_nowait(), ('C:/BDO', False))
        self.ctx['procurar_bdo'].assert_not_called()
        self.ctx['status_var'].set.assert_not_called()

    def test_sem_instalacao_libera_selecao_manual(self):
        results = queue.Queue()
        results.put(('', False))
        self.ctx['acompanhar_busca_bdo'](results, 112)
        self.assertFalse(self.ctx['BUSCA_EM_ANDAMENTO'])
        self.ctx['botao_selecionar'].config.assert_called_with(state='normal')
        self.ctx['loader_busca'].stop.assert_called_once()
        self.ctx['salvar_pasta_bdo'].assert_not_called()
        self.ctx['janela'].after.assert_not_called()

    def test_timeout_descarta_resultado_tardio_sem_sobrescrever_pasta_manual(self):
        results = queue.Queue()
        self.ctx['acompanhar_busca_bdo'](results, 99)
        self.ctx['botao_selecionar'].config.assert_called_with(state='normal')
        self.ctx['PASTA_BDO'] = 'D:/EscolhaManual'
        results.put(('C:/ResultadoTardio', False))
        self.ctx['janela'].after.assert_not_called()
        self.assertEqual(self.ctx['PASTA_BDO'], 'D:/EscolhaManual')

    def test_falha_de_io_e_enviada_sem_acessar_widgets(self):
        results = queue.Queue()
        self.ctx['carregar_pasta_bdo_salva'].side_effect = OSError('disco indisponível')
        self.ctx['executar_busca_bdo'](results)
        self.assertEqual(results.get_nowait(), ('', True))
        self.ctx['status_var'].set.assert_not_called()

    def test_resultado_encontrado_e_aplicado_pela_thread_da_interface(self):
        results = queue.Queue()
        results.put(('C:/BDO', False))
        self.ctx['acompanhar_busca_bdo'](results, 112)
        self.assertEqual(self.ctx['PASTA_BDO'], 'C:/BDO')
        self.ctx['salvar_pasta_bdo'].assert_called_once_with('C:/BDO')
        self.ctx['atualizar_modo_instalado'].assert_called_once()
