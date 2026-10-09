"""Verifica abertura e instância única do pacote, com dados de usuário isolados."""

import ctypes
from ctypes import wintypes
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def smoke(executable):
    executable = Path(executable).resolve(strict=True)
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
    user32.FindWindowW.restype = wintypes.HWND
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    if user32.FindWindowW(None, 'BDO Mode Manager'):
        raise RuntimeError('Feche a instância atual do app antes deste teste.')
    with tempfile.TemporaryDirectory() as temporary:
        env = dict(os.environ, LOCALAPPDATA=temporary,
                   PATH=os.path.join(os.environ['SystemRoot'], 'System32'))
        # Remove variáveis do ambiente de desenvolvimento: usa o Tk incluído no pacote.
        for name in ('PYTHONHOME', 'PYTHONPATH', 'TCL_LIBRARY', 'TK_LIBRARY'):
            env.pop(name, None)
        startup = subprocess.STARTUPINFO()
        startup.dwFlags = subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = 0
        process = subprocess.Popen([str(executable)], cwd=temporary, env=env,
                                   startupinfo=startup)
        hwnd = None
        try:
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                hwnd = user32.FindWindowW(None, 'BDO Mode Manager')
                if hwnd:
                    pid = wintypes.DWORD()
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    if pid.value == process.pid:
                        break
                if process.poll() is not None:
                    raise RuntimeError(f'O app encerrou antes de abrir: {process.returncode}')
                time.sleep(0.2)
            else:
                raise RuntimeError('A janela não foi criada em 20 segundos.')
            second = subprocess.run([str(executable)], cwd=temporary, env=env,
                                    startupinfo=startup, timeout=10)
            if second.returncode != 0 or process.poll() is not None:
                raise RuntimeError('Falha na verificação de instância única.')
            user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE
            if process.wait(timeout=10) != 0:
                raise RuntimeError('Falha ao fechar o app.')
            print('OK: abertura sem Python no PATH, arquivos incluídos e instância única.')
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)


if __name__ == '__main__':
    smoke(sys.argv[1])
