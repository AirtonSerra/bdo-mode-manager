import ast
import ctypes
from ctypes import wintypes
import os
from pathlib import Path
import subprocess
import sys
import tkinter as tk
import unittest
import uuid


@unittest.skipUnless(sys.platform == 'win32', 'Propriedades da janela do Windows')
class AtalhoJanelaTests(unittest.TestCase):
    def test_comando_icone_e_identidade_do_item_fixado(self):
        pasta = Path(__file__).resolve().parents[1]
        arvore = ast.parse((pasta / 'BDO_Mode_Manager.pyw').read_text(encoding='utf-8'))
        arvore.body = [no for no in arvore.body if isinstance(no, ast.FunctionDef)
                       and no.name == 'configurar_atalho_da_janela']
        contexto = dict(ctypes=ctypes, wintypes=wintypes, uuid=uuid,
                        subprocess=subprocess, os=os, PASTA_PROGRAMA=str(pasta),
                        CAMINHO_ICONE=str(pasta / 'assets/bdo-mode-manager-spirit-outline.ico'),
                        _hwnd_atalho=None)
        exec(compile(arvore, 'atalho', 'exec'), contexto)
        janela = tk.Tk()
        janela.withdraw()
        try:
            janela.update_idletasks()
            user32 = ctypes.WinDLL('user32')
            user32.GetParent.argtypes = [wintypes.HWND]
            user32.GetParent.restype = wintypes.HWND
            hwnd = user32.GetParent(janela.winfo_id()) or janela.winfo_id()
            contexto['configurar_atalho_da_janela'](hwnd)
            class Chave(ctypes.Structure):
                _fields_ = [('guid', ctypes.c_ubyte * 16), ('pid', wintypes.DWORD)]
            class Valor(ctypes.Structure):
                _fields_ = [('vt', ctypes.c_ushort), ('reservados', ctypes.c_ushort * 3),
                            ('dados', ctypes.c_void_p * 2)]
            shell32 = ctypes.WinDLL('shell32')
            shell32.SHGetPropertyStoreForWindow.argtypes = [wintypes.HWND, ctypes.c_void_p,
                                                          ctypes.POINTER(ctypes.c_void_p)]
            shell32.SHGetPropertyStoreForWindow.restype = ctypes.c_long
            iid = (ctypes.c_ubyte * 16).from_buffer_copy(uuid.UUID(
                '886d8eeb-8cf2-4446-8d02-cdba1dbdcf99').bytes_le)
            store = ctypes.c_void_p()
            self.assertEqual(shell32.SHGetPropertyStoreForWindow(hwnd, iid, ctypes.byref(store)), 0)
            tabela = ctypes.cast(store, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents
            obter = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p,
                                      ctypes.POINTER(Chave), ctypes.POINTER(Valor))(tabela[5])
            liberar = ctypes.WINFUNCTYPE(wintypes.ULONG, ctypes.c_void_p)(tabela[2])
            ole32 = ctypes.WinDLL('ole32')
            ole32.PropVariantClear.argtypes = [ctypes.POINTER(Valor)]
            esperado = {
                2: subprocess.list2cmdline([os.path.join(os.environ['SystemRoot'], 'System32', 'wscript.exe'),
                                           str(pasta / 'launch.vbs')]),
                3: contexto['CAMINHO_ICONE'] + ',0',
                4: 'BDO Mode Manager', 5: 'BDOModeManager.App'}
            try:
                for pid, texto in esperado.items():
                    chave = Chave((ctypes.c_ubyte * 16).from_buffer_copy(uuid.UUID(
                        '9f4c2855-9f79-4b39-a8d0-e1d42de1d5f3').bytes_le), pid)
                    valor = Valor()
                    self.assertEqual(obter(store, ctypes.byref(chave), ctypes.byref(valor)), 0)
                    try:
                        self.assertEqual(valor.vt, 31)
                        self.assertEqual(ctypes.wstring_at(valor.dados[0]), texto)
                    finally:
                        ole32.PropVariantClear(ctypes.byref(valor))
                contexto['configurar_atalho_da_janela'](hwnd)
            finally:
                liberar(store)
        finally:
            janela.destroy()
