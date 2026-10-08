import os
import ctypes
from ctypes import wintypes
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import winreg


# ============================================================
# BDO MODE MANAGER
# ============================================================

NOME_ARQUIVO = "dxvk.conf"

# Pasta onde o script está localizado.
PASTA_PROGRAMA = os.path.dirname(os.path.abspath(__file__))

# Pasta dos modos de jogo
PASTA_MODOS = os.path.join(
    PASTA_PROGRAMA,
    "Modos de jogo"
)

# Pasta bin64 da raiz do programa
PASTA_BIN64_PROGRAMA = os.path.join(
    PASTA_PROGRAMA,
    "bin64"
)

# Caminho do BDO
PASTA_BDO = ""

# Arquivo de configuração onde o path do BDO é salvo, para não
# precisar procurar/selecionar de novo a cada abertura.
# Fica na própria pasta do programa (ao lado do .pyw) —
# não cria nada em %APPDATA% nem em outro lugar do PC do usuário.
ARQUIVO_CONFIG = os.path.join(PASTA_PROGRAMA, "config.json")


# ============================================================
# CONFIGURAÇÃO SALVA (PATH DO BDO)
# ============================================================

def carregar_pasta_bdo_salva():
    """
    Lê o path do BDO salvo anteriormente no arquivo de config.
    Retorna string vazia se não existir ou estiver corrompido.
    """
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados.get("pasta_bdo", "") or ""
    except (OSError, IOError, ValueError, AttributeError):
        return ""


def salvar_pasta_bdo(pasta):
    """
    Salva o path do BDO no arquivo de config (na pasta do
    programa), para ser reaproveitado na próxima abertura.
    """
    try:
        with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as arquivo:
            json.dump({"pasta_bdo": pasta}, arquivo, ensure_ascii=False, indent=2)
    except (OSError, IOError):
        # Falha ao salvar (ex.: pasta somente leitura) não deve
        # impedir o uso do programa.
        pass


# ============================================================
# TEMA DO WINDOWS
# ============================================================

def windows_usa_tema_escuro():
    """
    Verifica o tema de aplicativos do Windows.

    AppsUseLightTheme:
        0 = modo escuro
        1 = modo claro
    """
    try:
        chave = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )

        valor, _ = winreg.QueryValueEx(
            chave,
            "AppsUseLightTheme"
        )

        winreg.CloseKey(chave)

        return valor == 0

    except (FileNotFoundError, OSError, PermissionError):
        return False


# ============================================================
# CORES
# ============================================================

TEMA_ESCURO = windows_usa_tema_escuro()

if TEMA_ESCURO:
    COR_FUNDO = "#202020"
    COR_FUNDO_SECUNDARIO = "#252525"
    COR_TEXTO = "#ffffff"
    COR_TEXTO_SECUNDARIO = "#c8c8c8"
    COR_ENTRADA = "#303030"
    COR_BOTAO = "#333333"
    COR_BOTAO_ATIVO = "#444444"
    COR_BOTAO_TEXTO = "#ffffff"
    COR_BORDA = "#444444"
    COR_HOVER_MINIMIZAR = "#0078d4"
else:
    COR_FUNDO = "#f0f0f0"
    COR_FUNDO_SECUNDARIO = "#ffffff"
    COR_TEXTO = "#202020"
    COR_TEXTO_SECUNDARIO = "#555555"
    COR_ENTRADA = "#ffffff"
    COR_BOTAO = "#e5e5e5"
    COR_BOTAO_ATIVO = "#d5d5d5"
    COR_BOTAO_TEXTO = "#202020"
    COR_BORDA = "#cccccc"
    COR_HOVER_MINIMIZAR = "#0078d4"

COR_HOVER_FECHAR = "#c42b1c"


# ============================================================
# CORES DE STATUS
# ============================================================

if TEMA_ESCURO:
    COR_SUCESSO = "#4ade80"
    COR_ERRO = "#ff5555"
else:
    COR_SUCESSO = "#008000"
    COR_ERRO = "#cc0000"


# ============================================================
# VALIDAÇÃO DO BDO
# ============================================================

def bdo_valido(pasta):
    if not pasta:
        return False

    pasta = os.path.normpath(pasta)
    pasta_bin64 = os.path.join(pasta, "bin64")

    return (
        os.path.isdir(pasta)
        and os.path.isdir(pasta_bin64)
    )


def obter_bin64_bdo():
    if not PASTA_BDO:
        return ""

    return os.path.join(PASTA_BDO, "bin64")


# ============================================================
# PROCURA AUTOMÁTICA DO BDO
# ============================================================

def procurar_bdo():
    candidatos = []

    pastas_base = [
        os.environ.get("ProgramFiles"),
        os.environ.get("ProgramFiles(x86)"),
        os.environ.get("ProgramData"),
        os.environ.get("LOCALAPPDATA"),
        os.environ.get("APPDATA"),
        os.environ.get("USERPROFILE")
    ]

    nomes = [
        "Black Desert",
        "BlackDesert",
        "Black Desert Online",
        os.path.join("Pearl Abyss", "Black Desert"),
        os.path.join("Pearl Abyss", "BlackDesert"),
        os.path.join("Steam", "steamapps", "common", "Black Desert"),
        os.path.join("Steam", "steamapps", "common", "BlackDesert"),
        # Nome real da pasta na versão Steam do BDO
        os.path.join("Steam", "steamapps", "common", "Black Desert Online")
    ]

    for base in pastas_base:
        if not base:
            continue
        for nome in nomes:
            candidatos.append(os.path.join(base, nome))

    for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        raiz = f"{letra}:\\"
        if not os.path.isdir(raiz):
            continue

        candidatos.extend([
            os.path.join(raiz, "BlackDesert"),
            os.path.join(raiz, "Black Desert"),
            os.path.join(raiz, "Black Desert Online"),
            os.path.join(raiz, "Jogos", "BlackDesert"),
            os.path.join(raiz, "Jogos", "Black Desert"),
            os.path.join(raiz, "Jogos", "Black Desert Online"),
            os.path.join(raiz, "Games", "BlackDesert"),
            os.path.join(raiz, "Games", "Black Desert"),
            os.path.join(raiz, "Games", "Black Desert Online"),
            os.path.join(raiz, "Program Files", "BlackDesert"),
            os.path.join(raiz, "Program Files", "Black Desert"),
            os.path.join(raiz, "Program Files", "Black Desert Online"),
            os.path.join(raiz, "Program Files (x86)", "BlackDesert"),
            os.path.join(raiz, "Program Files (x86)", "Black Desert"),
            os.path.join(raiz, "Program Files (x86)", "Black Desert Online"),
            # Bibliotecas Steam em outras unidades (padrão mais comum na versão Steam)
            os.path.join(raiz, "Steam", "steamapps", "common", "Black Desert"),
            os.path.join(raiz, "Steam", "steamapps", "common", "BlackDesert"),
            os.path.join(raiz, "Steam", "steamapps", "common", "Black Desert Online"),
            os.path.join(raiz, "SteamLibrary", "steamapps", "common", "Black Desert"),
            os.path.join(raiz, "SteamLibrary", "steamapps", "common", "BlackDesert"),
            os.path.join(raiz, "SteamLibrary", "steamapps", "common", "Black Desert Online")
        ])

    vistos = set()
    candidatos_unicos = []

    for candidato in candidatos:
        candidato = os.path.normpath(candidato)
        chave = candidato.lower()
        if chave not in vistos:
            vistos.add(chave)
            candidatos_unicos.append(candidato)

    for candidato in candidatos_unicos:
        if bdo_valido(candidato):
            return candidato

    nomes_alvo = {"blackdesert", "black desert", "black desert online"}
    ignorar = {
        "$recycle.bin",
        "system volume information",
        "windows",
        "programdata",
        "appdata"
    }

    for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        raiz = f"{letra}:\\"
        if not os.path.isdir(raiz):
            continue

        try:
            for pasta_atual, diretorios, arquivos in os.walk(
                raiz,
                topdown=True,
                onerror=lambda erro: None
            ):
                diretorios[:] = [
                    d for d in diretorios
                    if d.lower() not in ignorar
                ]

                nome = os.path.basename(pasta_atual).lower()
                if nome in nomes_alvo:
                    if bdo_valido(pasta_atual):
                        return os.path.normpath(pasta_atual)

        except (PermissionError, OSError):
            continue

    return ""


# ============================================================
# SELEÇÃO MANUAL DO BDO
# ============================================================

def selecionar_bdo():
    global PASTA_BDO

    pasta_inicial = PASTA_BDO
    if not pasta_inicial or not os.path.isdir(pasta_inicial):
        pasta_inicial = PASTA_PROGRAMA

    pasta = filedialog.askdirectory(
        title="Selecione a pasta do Black Desert",
        initialdir=pasta_inicial
    )

    if not pasta:
        return

    pasta = os.path.normpath(pasta)

    if not bdo_valido(pasta):
        messagebox.showerror(
            "BDO Mode Manager - Caminho inválido",
            "A pasta selecionada não é uma instalação "
            "válida do Black Desert.\n\n"
            "A pasta precisa conter:\n\n"
            "bin64\n\n"
            f"Pasta selecionada:\n{pasta}"
        )
        return

    PASTA_BDO = pasta
    salvar_pasta_bdo(PASTA_BDO)
    atualizar_status()
    atualizar_modo_instalado()


# ============================================================
# STATUS DO BDO
# ============================================================

def atualizar_status():
    if PASTA_BDO and bdo_valido(PASTA_BDO):
        texto_path.set(PASTA_BDO)
        status_var.set("✓  Black Desert encontrado")
        status_label.config(fg=COR_SUCESSO)
    else:
        texto_path.set("")
        status_var.set("✕  Black Desert não encontrado")
        status_label.config(fg=COR_ERRO)


# ============================================================
# LEITURA DAS CONFIGURAÇÕES DOS PERFIS
# ============================================================

def ler_configuracao_perfil(caminho):
    """Compara opções ativas, preservando diferenças reais de configuração."""
    try:
        with open(caminho, "r", encoding="utf-8-sig") as arquivo:
            configuracao = {}
            for linha in arquivo:
                linha = linha.strip()
                if not linha or linha.startswith("#"):
                    continue
                chave, separador, valor = linha.partition("=")
                chave, valor = chave.strip(), valor.strip()
                if not separador or not chave or not valor:
                    return None
                # Valores de texto permanecem sensíveis a maiúsculas;
                # somente os literais booleanos e Auto são normalizados.
                if valor.lower() in {"true", "false", "auto"}:
                    valor = valor.lower()
                # Não presume qual definição prevalece em arquivos ambíguos.
                if chave in configuracao and configuracao[chave] != valor:
                    return None
                configuracao[chave] = valor
            return configuracao
    except (OSError, UnicodeError):
        return None


# ============================================================
# LISTAR MODOS
# ============================================================

def listar_modos():
    if not os.path.isdir(PASTA_MODOS):
        return []

    modos = []
    try:
        for nome in os.listdir(PASTA_MODOS):
            caminho = os.path.join(PASTA_MODOS, nome)
            if os.path.isdir(caminho):
                modos.append(nome)
    except (PermissionError, OSError):
        return []

    return sorted(modos, key=str.lower)


# ============================================================
# IDENTIFICAR MODO INSTALADO
# ============================================================

def detectar_perfil_instalado():
    """Retorna (nome, situação), sem escolher entre perfis equivalentes."""
    if not PASTA_BDO or not bdo_valido(PASTA_BDO):
        return None, "Jogo não selecionado"

    arquivo_bdo = os.path.join(obter_bin64_bdo(), NOME_ARQUIVO)
    if not os.path.isfile(arquivo_bdo):
        return None, "Sem configuração instalada"

    configuracao_bdo = ler_configuracao_perfil(arquivo_bdo)
    if configuracao_bdo is None:
        return None, "Configuração ilegível ou inválida"

    correspondencias = []
    for modo in listar_modos():
        arquivo_modo = os.path.join(PASTA_MODOS, modo, NOME_ARQUIVO)
        if not os.path.isfile(arquivo_modo):
            continue

        configuracao_modo = ler_configuracao_perfil(arquivo_modo)
        if configuracao_modo is not None and configuracao_modo == configuracao_bdo:
            correspondencias.append(modo)

    if len(correspondencias) == 1:
        return correspondencias[0], "Reconhecido"
    if correspondencias:
        return None, "Perfis equivalentes: " + ", ".join(correspondencias)
    return None, "Configuração personalizada ou desconhecida"


def identificar_modo_instalado():
    return detectar_perfil_instalado()[0]


# ============================================================
# ATUALIZAR LABEL DO MODO
# ============================================================

def atualizar_modo_instalado():
    modo, situacao = detectar_perfil_instalado()

    if modo:
        modo_var.set(f"Perfil identificado: {modo}")
        modo_label.config(fg=COR_SUCESSO)
    else:
        modo_var.set(situacao)
        modo_label.config(fg=COR_TEXTO_SECUNDARIO)
    criar_botoes_modos()


# ============================================================
# DLLs DO PROGRAMA
# ============================================================

def listar_dlls_programa():
    if not os.path.isdir(PASTA_BIN64_PROGRAMA):
        return []

    try:
        dlls = []
        for nome in os.listdir(PASTA_BIN64_PROGRAMA):
            caminho = os.path.join(PASTA_BIN64_PROGRAMA, nome)
            if os.path.isfile(caminho) and nome.lower().endswith(".dll"):
                dlls.append(nome)
        return sorted(dlls, key=str.lower)
    except (PermissionError, OSError):
        return []


# ============================================================
# VALIDAR BIN64 DO PROGRAMA
# ============================================================

def validar_bin64_programa():
    if not os.path.isdir(PASTA_BIN64_PROGRAMA):
        return (
            False,
            "A pasta bin64 da raiz do programa não foi encontrada.\n\n"
            f"Pasta esperada:\n{PASTA_BIN64_PROGRAMA}"
        )

    dlls = listar_dlls_programa()
    if not dlls:
        return (
            False,
            "A pasta bin64 da raiz do programa não possui nenhuma DLL diretamente nela.\n\n"
            f"Pasta verificada:\n{PASTA_BIN64_PROGRAMA}"
        )

    return (True, "")


# ============================================================
# APLICAR DLLs
# ============================================================

def aplicar_dlls(pasta_bin64_bdo):
    valido, erro = validar_bin64_programa()
    if not valido:
        raise Exception(erro)

    dlls = listar_dlls_programa()
    aplicadas = []
    existentes = []

    for nome_dll in dlls:
        origem = os.path.join(PASTA_BIN64_PROGRAMA, nome_dll)
        destino = os.path.join(pasta_bin64_bdo, nome_dll)

        if not os.path.isfile(origem):
            raise FileNotFoundError(
                "A DLL não foi encontrada.\n\n"
                f"DLL:\n{nome_dll}\n\n"
                f"Caminho esperado:\n{origem}"
            )

        if os.path.isfile(destino):
            existentes.append(nome_dll)
        else:
            shutil.copy2(origem, destino)
            aplicadas.append(nome_dll)

    return (aplicadas, existentes)


# ============================================================
# APLICAR MODO
# ============================================================

def listar_processos_windows():
    """Consulta processos sem encerrar ou modificar nenhum deles."""
    class EntradaProcesso(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD), ("th32DefaultHeapID", ctypes.c_size_t),
            ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", wintypes.LONG),
            ("dwFlags", wintypes.DWORD), ("szExeFile", wintypes.WCHAR * 260),
        ]
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(EntradaProcesso)]
    kernel32.Process32FirstW.restype = wintypes.BOOL
    kernel32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(EntradaProcesso)]
    kernel32.Process32NextW.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    snapshot = kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
    if snapshot == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        entrada = EntradaProcesso()
        entrada.dwSize = ctypes.sizeof(entrada)
        nomes = set()
        disponivel = kernel32.Process32FirstW(snapshot, ctypes.byref(entrada))
        while disponivel:
            nomes.add(entrada.szExeFile.casefold())
            disponivel = kernel32.Process32NextW(snapshot, ctypes.byref(entrada))
        erro = ctypes.get_last_error()
        if erro != 18:  # ERROR_NO_MORE_FILES: término normal da enumeração.
            raise ctypes.WinError(erro)
        return nomes
    finally:
        kernel32.CloseHandle(snapshot)


def permitir_alteracao_com_jogo_fechado():
    try:
        processos = listar_processos_windows()
    except OSError:
        messagebox.showerror(
            "Não foi possível verificar o jogo",
            "Não foi possível verificar se o Black Desert está aberto.\n\n"
            "Nenhum arquivo foi alterado. Tente novamente antes de continuar.")
        return False
    nomes_jogo = {
        "blackdesert.exe", "blackdesert.bin", "blackdesert64.exe",
        "blackdesert64.bin", "blackdesert32.exe", "blackdesert32.bin",
    }
    if nomes_jogo.intersection(nome.casefold() for nome in processos):
        messagebox.showwarning(
            "Black Desert está aberto",
            "Feche o Black Desert antes de aplicar um perfil ou remover o DXVK.\n\n"
            "Nenhum arquivo foi alterado.")
        return False
    return True


def trocar_modo(nome_modo):
    try:
        if not PASTA_BDO:
            raise Exception(
                "A pasta do Black Desert não foi definida.\n\n"
                "Selecione a pasta do BDO antes de aplicar um modo de jogo."
            )

        if not bdo_valido(PASTA_BDO):
            raise Exception(
                "A pasta do Black Desert configurada é inválida.\n\n"
                "Ela precisa conter uma pasta chamada:\n\nbin64"
            )

        pasta_bin64_bdo = obter_bin64_bdo()

        pasta_modo = os.path.join(PASTA_MODOS, nome_modo)
        if not os.path.isdir(pasta_modo):
            raise Exception(f"A pasta do modo '{nome_modo}' não foi encontrada.")

        arquivo_origem = os.path.join(pasta_modo, NOME_ARQUIVO)
        if not os.path.isfile(arquivo_origem):
            raise Exception(
                f"O modo '{nome_modo}' não possui o arquivo '{NOME_ARQUIVO}'.\n\n"
                f"Arquivo esperado:\n{arquivo_origem}"
            )

        valido, erro = validar_bin64_programa()
        if not valido:
            raise Exception(erro)

        arquivo_destino = os.path.join(pasta_bin64_bdo, NOME_ARQUIVO)

        if not permitir_alteracao_com_jogo_fechado():
            return

        backup_dxvk = None
        if os.path.isfile(arquivo_destino):
            backup_dxvk = arquivo_destino + ".bdm_backup"
            shutil.copy2(arquivo_destino, backup_dxvk)

        dlls_aplicadas = []

        try:
            shutil.copy2(arquivo_origem, arquivo_destino)
            dlls_aplicadas, dlls_existentes = aplicar_dlls(pasta_bin64_bdo)
        except Exception:
            for dll in dlls_aplicadas:
                caminho = os.path.join(pasta_bin64_bdo, dll)
                try:
                    if os.path.isfile(caminho):
                        os.remove(caminho)
                except OSError:
                    pass

            try:
                if backup_dxvk:
                    shutil.copy2(backup_dxvk, arquivo_destino)
                elif os.path.isfile(arquivo_destino):
                    os.remove(arquivo_destino)
            except OSError:
                pass

            raise
        finally:
            if backup_dxvk and os.path.isfile(backup_dxvk):
                try:
                    os.remove(backup_dxvk)
                except OSError:
                    pass

        mensagem = (
            f"Modo '{nome_modo}' aplicado com sucesso!\n\n"
            f"Arquivo aplicado:\n• {NOME_ARQUIVO}"
        )

        if dlls_aplicadas:
            mensagem += "\n\nDLLs aplicadas ao BDO:\n"
            for dll in dlls_aplicadas:
                mensagem += f"• {dll}\n"
        else:
            mensagem += (
                "\n\nNenhuma DLL precisou ser aplicada.\n"
                "Todas as DLLs já estavam presentes no BDO."
            )

        if dlls_existentes:
            mensagem += f"\n\n{len(dlls_existentes)} DLL(s) já estavam presentes no BDO."

        messagebox.showinfo("BDO Mode Manager", mensagem)
        atualizar_modo_instalado()

    except PermissionError:
        messagebox.showerror(
            "BDO Mode Manager - Erro de permissão",
            "O Windows não permitiu alterar os arquivos.\n\n"
            "Possíveis causas:\n\n"
            "• O Black Desert está aberto.\n"
            "• A pasta bin64 não permite gravação.\n"
            "• Execute o programa como administrador."
        )
    except Exception as erro:
        messagebox.showerror(
            "BDO Mode Manager - Erro",
            f"Não foi possível aplicar o modo '{nome_modo}'.\n\n"
            f"Detalhes do erro:\n\n{erro}"
        )


# ============================================================
# DESINSTALAR
# ============================================================

def desinstalar():
    try:
        if not PASTA_BDO:
            raise Exception("A pasta do Black Desert não foi definida.")

        if not bdo_valido(PASTA_BDO):
            raise Exception("A pasta do Black Desert configurada é inválida.")

        pasta_bin64_bdo = obter_bin64_bdo()

        if not permitir_alteracao_com_jogo_fechado():
            return

        confirmar = messagebox.askyesno(
            "BDO Mode Manager - Desinstalar",
            "Isso irá remover da bin64 do BDO:\n\n"
            "• dxvk.conf\n"
            "• Todas as DLLs presentes na bin64 do BDO Mode Manager\n\n"
            "Deseja continuar?"
        )

        if not confirmar:
            return

        # Verifica novamente caso o jogo tenha aberto durante a confirmação.
        if not permitir_alteracao_com_jogo_fechado():
            return

        removidos = []

        arquivo_dxvk = os.path.join(pasta_bin64_bdo, NOME_ARQUIVO)
        if os.path.isfile(arquivo_dxvk):
            os.remove(arquivo_dxvk)
            removidos.append(NOME_ARQUIVO)

        dlls = listar_dlls_programa()
        for nome_dll in dlls:
            caminho = os.path.join(pasta_bin64_bdo, nome_dll)
            if os.path.isfile(caminho):
                os.remove(caminho)
                removidos.append(nome_dll)

        if removidos:
            mensagem = "Desinstalação concluída!\n\nArquivos removidos:\n"
            for arquivo in removidos:
                mensagem += f"• {arquivo}\n"
        else:
            mensagem = "Nenhum arquivo precisou ser removido."

        messagebox.showinfo("BDO Mode Manager", mensagem)
        atualizar_modo_instalado()

    except PermissionError:
        messagebox.showerror(
            "BDO Mode Manager - Erro de permissão",
            "O Windows não permitiu remover os arquivos.\n\n"
            "Verifique se o Black Desert está fechado e tente novamente."
        )
    except Exception as erro:
        messagebox.showerror(
            "BDO Mode Manager - Erro",
            f"Não foi possível desinstalar.\n\nDetalhes do erro:\n\n{erro}"
        )


# ============================================================
# CRIAR BOTÕES DOS MODOS
# ============================================================

def criar_botoes_modos():
    for widget in frame_modos.winfo_children():
        widget.destroy()

    modos = listar_modos()
    atual = identificar_modo_instalado()
    if not modos:
        tk.Label(frame_modos, text="Nenhum perfil encontrado em Modos de jogo/.",
                 bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO).pack(pady=12)
        return

    descricoes = {
        "batata": ("🥔", "Texturas simplificadas para priorizar o desempenho"),
        "normal": ("🖼", "Qualidade gráfica original, usando DXVK/Vulkan no lugar do DirectX"),
    }
    for nome in modos:
        ativo = nome == atual
        icone, descricao = descricoes.get(nome.lower(), ("⚙", "Perfil personalizado do DXVK"))
        cor = COR_FUNDO_SECUNDARIO
        borda = COR_SUCESSO if ativo else COR_BORDA
        card = tk.Frame(frame_modos, bg=cor, highlightbackground=borda,
                        highlightcolor=borda, highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))
        card.columnconfigure(0, weight=1)
        titulo_card = tk.Label(card, text=f"{icone}  {nome}", font=("Segoe UI", 13, "bold"),
                               bg=cor, fg=COR_TEXTO, anchor="w")
        titulo_card.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 3))
        resumo = tk.Label(card, text=descricao, font=("Segoe UI", 9),
                          bg=cor, fg=COR_TEXTO_SECUNDARIO, anchor="w",
                          justify="left", wraplength=310)
        resumo.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 12))
        acao = tk.Button(card, text="✓ Ativo" if ativo else "Aplicar",
                         font=("Segoe UI", 10), bg=COR_BOTAO,
                         fg=COR_SUCESSO if ativo else COR_TEXTO,
                         activebackground=COR_BOTAO_ATIVO,
                         activeforeground=COR_TEXTO, relief="flat", bd=0,
                         padx=10, pady=7, cursor="hand2",
                         command=lambda modo=nome: trocar_modo(modo))
        acao.grid(row=0, column=1, rowspan=2, padx=(0, 14))

def minimizar_janela():
    # Minimiza sem recriar o estilo da janela ou perder o botão na barra.
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.GetParent.argtypes = [wintypes.HWND]
    user32.GetParent.restype = wintypes.HWND
    user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.ShowWindow.restype = wintypes.BOOL
    hwnd = user32.GetParent(janela.winfo_id()) or janela.winfo_id()
    user32.ShowWindow(hwnd, 6)  # SW_MINIMIZE


def restaurar_janela(event=None):
    if event is not None and event.widget is not janela:
        return
    try:
        if janela.state() == "normal":
            janela.after_idle(configurar_barra_de_tarefas)
    except tk.TclError:
        pass


_procedimento_janela = None
_procedimento_original = None
_hwnd_personalizado = None
_icones_nativos = []


def configurar_icone_nativo(user32, hwnd):
    if not os.path.isfile(CAMINHO_ICONE):
        return
    user32.LoadImageW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR,
                                 wintypes.UINT, ctypes.c_int, ctypes.c_int, wintypes.UINT]
    user32.LoadImageW.restype = wintypes.HANDLE
    user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT,
                                   wintypes.WPARAM, wintypes.LPARAM]
    user32.SendMessageW.restype = ctypes.c_ssize_t
    if not _icones_nativos:
        # Usa fontes maiores para evitar ampliar um bitmap de apenas 16 px.
        for tamanho in (32, 256):
            icone = user32.LoadImageW(None, CAMINHO_ICONE, 1, tamanho, tamanho, 0x0010)
            if not icone:
                raise ctypes.WinError(ctypes.get_last_error())
            _icones_nativos.append(icone)
    for tipo, icone in enumerate(_icones_nativos):
        user32.SendMessageW(hwnd, 0x0080, tipo, icone)  # WM_SETICON


def configurar_moldura_nativa(user32, hwnd):
    """Preserva as animações nativas sem desenhar a barra de título padrão."""
    global _procedimento_janela, _procedimento_original, _hwnd_personalizado
    if _hwnd_personalizado == hwnd:
        return

    resultado_tipo = ctypes.c_ssize_t
    procedimento_tipo = ctypes.WINFUNCTYPE(
        resultado_tipo, wintypes.HWND, wintypes.UINT,
        wintypes.WPARAM, wintypes.LPARAM)
    set_long = (user32.SetWindowLongPtrW if ctypes.sizeof(ctypes.c_void_p) == 8
                else user32.SetWindowLongW)
    set_long.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
    set_long.restype = ctypes.c_ssize_t
    user32.CallWindowProcW.argtypes = [ctypes.c_void_p, wintypes.HWND,
                                      wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    user32.CallWindowProcW.restype = resultado_tipo

    def procedimento(hwnd_atual, mensagem, wparam, lparam):
        if mensagem == 0x0083:  # WM_NCCALCSIZE: toda a janela é área de conteúdo.
            return 0
        return user32.CallWindowProcW(
            _procedimento_original, hwnd_atual, mensagem, wparam, lparam)

    # A referência global mantém o callback vivo enquanto o Windows o utiliza.
    _procedimento_janela = procedimento_tipo(procedimento)
    ctypes.set_last_error(0)
    _procedimento_original = set_long(
        hwnd, -4, ctypes.cast(_procedimento_janela, ctypes.c_void_p).value)
    if not _procedimento_original:
        raise ctypes.WinError(ctypes.get_last_error())
    _hwnd_personalizado = hwnd

    estilo = user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
    # WS_CAPTION e WS_MINIMIZEBOX permitem ao Windows animar a transição.
    user32.SetWindowLongW(hwnd, -16, estilo | 0x00C00000 | 0x00020000)
    user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND,
                                   ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                   ctypes.c_int, wintypes.UINT]
    user32.SetWindowPos.restype = wintypes.BOOL
    user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, 0x0037)  # FRAMECHANGED, sem mover.


def configurar_barra_de_tarefas():
    """Mantém a janela sem bordas visível na barra de tarefas do Windows."""
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.GetParent.argtypes = [wintypes.HWND]
    user32.GetParent.restype = wintypes.HWND
    user32.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.GetWindowLongW.restype = wintypes.LONG
    user32.SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.LONG]
    user32.SetWindowLongW.restype = wintypes.LONG

    hwnd = user32.GetParent(janela.winfo_id()) or janela.winfo_id()
    estilo = user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE
    # WS_EX_APPWINDOW inclui na barra; WS_EX_TOOLWINDOW exclui da barra.
    novo_estilo = (estilo | 0x00040000) & ~0x00000080
    if novo_estilo != estilo:
        ctypes.set_last_error(0)
        resultado = user32.SetWindowLongW(hwnd, -20, novo_estilo)
        if resultado == 0 and ctypes.get_last_error():
            raise ctypes.WinError(ctypes.get_last_error())
    configurar_moldura_nativa(user32, hwnd)
    configurar_icone_nativo(user32, hwnd)


def mostrar_janela():
    janela.update_idletasks()
    configurar_barra_de_tarefas()
    # O Windows registra o estilo na próxima exibição da janela.
    janela.withdraw()
    janela.after(10, janela.deiconify)


def fechar_janela():
    janela.destroy()


# ============================================================
# EFEITOS DE HOVER DOS BOTÕES DA BARRA
# ============================================================

def minimizar_entrar(event):
    botao_minimizar.config(bg=COR_HOVER_MINIMIZAR, fg="#ffffff")


def minimizar_sair(event):
    botao_minimizar.config(bg=COR_FUNDO_SECUNDARIO, fg=COR_TEXTO)


def fechar_entrar(event):
    botao_fechar.config(bg=COR_HOVER_FECHAR, fg="#ffffff")


def fechar_sair(event):
    botao_fechar.config(bg=COR_FUNDO_SECUNDARIO, fg=COR_TEXTO)


# ============================================================
# ARRASTAR JANELA
# ============================================================

posicao_x = 0
posicao_y = 0


def iniciar_movimento(event):
    global posicao_x
    global posicao_y
    posicao_x = event.x_root
    posicao_y = event.y_root


def mover_janela(event):
    global posicao_x
    global posicao_y

    deslocamento_x = event.x_root - posicao_x
    deslocamento_y = event.y_root - posicao_y

    novo_x = janela.winfo_x() + deslocamento_x
    novo_y = janela.winfo_y() + deslocamento_y

    janela.geometry(f"+{novo_x}+{novo_y}")

    posicao_x = event.x_root
    posicao_y = event.y_root


# ============================================================
# JANELA PRINCIPAL (CENTRALIZADA)
# ============================================================

shell32 = ctypes.WinDLL("shell32", use_last_error=True)
shell32.SetCurrentProcessExplicitAppUserModelID.argtypes = [wintypes.LPCWSTR]
shell32.SetCurrentProcessExplicitAppUserModelID.restype = ctypes.c_long
shell32.SetCurrentProcessExplicitAppUserModelID("BDOModeManager.App")

janela = tk.Tk()
janela.title("BDO Mode Manager")
CAMINHO_ICONE = os.path.join(PASTA_PROGRAMA, "assets", "bdo-mode-manager-spirit-outline.ico")
if os.path.isfile(CAMINHO_ICONE):
    janela.iconbitmap(default=CAMINHO_ICONE)

largura_janela = 520
altura_janela = 600

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

pos_x = (largura_tela - largura_janela) // 2
pos_y = (altura_tela - altura_janela) // 2

janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

janela.resizable(True, True)
janela.minsize(520, 600)
janela.overrideredirect(True)
janela.configure(bg=COR_FUNDO)


# ============================================================
# BARRA DE TÍTULO
# ============================================================

barra_titulo = tk.Frame(
    janela,
    bg=COR_FUNDO_SECUNDARIO,
    height=34
)
barra_titulo.pack(fill="x", side="top")
barra_titulo.pack_propagate(False)


# ============================================================
# TÍTULO DA BARRA
# ============================================================

CAMINHO_ICONE_TOPO = os.path.join(PASTA_PROGRAMA, "assets", "bdo-mode-manager-title.png")
if os.path.isfile(CAMINHO_ICONE_TOPO):
    icone_topo = tk.PhotoImage(file=CAMINHO_ICONE_TOPO)
    label_icone_barra = tk.Label(barra_titulo, image=icone_topo,
                                 bg=COR_FUNDO_SECUNDARIO, bd=0)
    label_icone_barra.pack(side="left", padx=(8, 0))
    label_icone_barra.bind("<Button-1>", iniciar_movimento)
    label_icone_barra.bind("<B1-Motion>", mover_janela)

label_titulo_barra = tk.Label(
    barra_titulo,
    text="BDO Mode Manager",
    font=("Arial", 10, "bold"),
    bg=COR_FUNDO_SECUNDARIO,
    fg=COR_TEXTO
)
label_titulo_barra.pack(side="left", padx=(10, 0))


# ============================================================
# BOTÃO FECHAR
# ============================================================

botao_fechar = tk.Button(
    barra_titulo,
    text="×",
    font=("Arial", 16),
    width=3,
    height=1,
    bg=COR_FUNDO_SECUNDARIO,
    fg=COR_TEXTO,
    activebackground=COR_HOVER_FECHAR,
    activeforeground="#ffffff",
    relief="flat",
    bd=0,
    cursor="hand2",
    command=fechar_janela
)
botao_fechar.pack(side="right", fill="y")
botao_fechar.bind("<Enter>", fechar_entrar)
botao_fechar.bind("<Leave>", fechar_sair)


# ============================================================
# BOTÃO MINIMIZAR
# ============================================================

botao_minimizar = tk.Button(
    barra_titulo,
    text="−",
    font=("Arial", 14),
    width=3,
    height=1,
    bg=COR_FUNDO_SECUNDARIO,
    fg=COR_TEXTO,
    activebackground=COR_HOVER_MINIMIZAR,
    activeforeground="#ffffff",
    relief="flat",
    bd=0,
    cursor="hand2",
    command=minimizar_janela
)
botao_minimizar.pack(side="right", fill="y")
botao_minimizar.bind("<Enter>", minimizar_entrar)
botao_minimizar.bind("<Leave>", minimizar_sair)


# ============================================================
# EVENTOS DA BARRA
# ============================================================

barra_titulo.bind("<ButtonPress-1>", iniciar_movimento)
barra_titulo.bind("<B1-Motion>", mover_janela)

label_titulo_barra.bind("<ButtonPress-1>", iniciar_movimento)
label_titulo_barra.bind("<B1-Motion>", mover_janela)

janela.bind("<Map>", restaurar_janela)


# ============================================================
# TÍTULO PRINCIPAL
# ============================================================

# Layout da interface: instalação, perfil atual, opções e remoção.
conteudo = tk.Frame(janela, bg=COR_FUNDO)
conteudo.pack(fill="both", expand=True, padx=24, pady=18)

tk.Label(conteudo, text="BDO Mode Manager", font=("Segoe UI", 20, "bold"),
         bg=COR_FUNDO, fg=COR_TEXTO, anchor="w").pack(fill="x")
tk.Label(conteudo, text="Configure o DXVK e escolha a qualidade gráfica",
         font=("Segoe UI", 10), bg=COR_FUNDO,
         fg=COR_TEXTO_SECUNDARIO, anchor="w").pack(fill="x", pady=(4, 18))

instalacao = tk.Frame(conteudo, bg=COR_FUNDO_SECUNDARIO,
                      highlightbackground=COR_BORDA, highlightthickness=1)
instalacao.pack(fill="x")
tk.Label(instalacao, text="Instalação do jogo", font=("Segoe UI", 10, "bold"),
         bg=COR_FUNDO_SECUNDARIO, fg=COR_TEXTO, anchor="w").pack(
             fill="x", padx=12, pady=(10, 8))
frame_path = tk.Frame(instalacao, bg=COR_FUNDO_SECUNDARIO)
frame_path.pack(fill="x", padx=12)
texto_path = tk.StringVar()
entrada_path = tk.Entry(frame_path, textvariable=texto_path, state="readonly",
                        font=("Segoe UI", 10), readonlybackground=COR_ENTRADA,
                        fg=COR_TEXTO, relief="flat", bd=0)
entrada_path.pack(side="left", fill="x", expand=True, ipady=8)
botao_selecionar = tk.Button(frame_path, text="Alterar pasta", command=selecionar_bdo,
                             font=("Segoe UI", 9), bg=COR_BOTAO, fg=COR_TEXTO,
                             activebackground=COR_BOTAO_ATIVO,
                             activeforeground=COR_TEXTO, relief="flat", bd=0,
                             padx=10, pady=7, cursor="hand2")
botao_selecionar.pack(side="right", padx=(8, 0))
status_var = tk.StringVar()
status_label = tk.Label(instalacao, textvariable=status_var, font=("Segoe UI", 9),
                        bg=COR_FUNDO_SECUNDARIO, anchor="w")
status_label.pack(fill="x", padx=12, pady=(8, 10))

modo_var = tk.StringVar()
modo_label = tk.Label(conteudo, textvariable=modo_var,
                      font=("Segoe UI", 10, "bold"), bg=COR_FUNDO, anchor="w")
modo_label.pack(fill="x", pady=(18, 10))

# O rodapé fica visível mesmo quando há vários perfis.
rodape = tk.Frame(conteudo, bg=COR_FUNDO)
rodape.pack(side="bottom", fill="x", pady=(8, 0))
tk.Label(rodape, text="Ambos os perfis padrão utilizam Vulkan via DXVK.",
         font=("Segoe UI", 9), bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO,
         anchor="w").pack(fill="x", pady=(0, 10))
botao_desinstalar = tk.Button(rodape, text="Remover DXVK", command=desinstalar,
                              font=("Segoe UI", 10, "bold"), bg=COR_BOTAO, fg=COR_TEXTO,
                              activebackground=COR_BOTAO_ATIVO,
                              activeforeground=COR_TEXTO, relief="flat", bd=0,
                              highlightbackground=COR_BORDA, highlightthickness=1,
                              padx=12, pady=7, cursor="hand2")
botao_desinstalar.pack(anchor="e")


class Tooltip:
    def __init__(self, widget, texto):
        self.widget = widget
        self.texto = texto
        self.agendamento = None
        self.popup = None
        widget.bind("<Enter>", self.agendar, add="+")
        widget.bind("<Leave>", self.ocultar, add="+")
        widget.bind("<ButtonPress>", self.ocultar, add="+")
        widget.bind("<FocusIn>", self.agendar, add="+")
        widget.bind("<FocusOut>", self.ocultar, add="+")
        widget.bind("<Destroy>", self.ocultar, add="+")

    def agendar(self, event=None):
        self.ocultar()
        self.agendamento = self.widget.after(500, self.mostrar)

    def mostrar(self):
        self.agendamento = None
        self.popup = tk.Toplevel(self.widget)
        self.popup.withdraw()
        self.popup.overrideredirect(True)
        tk.Label(self.popup, text=self.texto, justify="left", wraplength=310,
                 font=("Segoe UI", 9), bg=COR_FUNDO_SECUNDARIO, fg=COR_TEXTO,
                 padx=12, pady=10, relief="solid", bd=1).pack()
        self.popup.update_idletasks()
        x = max(0, min(self.widget.winfo_rootx(),
                       self.widget.winfo_screenwidth() - self.popup.winfo_reqwidth()))
        y = max(0, self.widget.winfo_rooty() - self.popup.winfo_reqheight() - 8)
        self.popup.geometry(f"+{x}+{y}")
        self.popup.deiconify()

    def ocultar(self, event=None):
        if self.agendamento is not None:
            self.widget.after_cancel(self.agendamento)
            self.agendamento = None
        if self.popup is not None:
            self.popup.destroy()
            self.popup = None


tooltip_remover = Tooltip(botao_desinstalar,
    "Remove os arquivos do DXVK e a configuração do perfil da pasta do jogo, "
    "permitindo que ele volte a usar o DirectX original.\n\n"
    "Feche o jogo antes de remover. Você poderá confirmar ou cancelar "
    "ao clicar no botão.")

# Lista rolável para acomodar perfis personalizados.
lista = tk.Frame(conteudo, bg=COR_FUNDO)
lista.pack(fill="both", expand=True)
canvas_modos = tk.Canvas(lista, bg=COR_FUNDO, highlightthickness=0)
scroll_modos = tk.Scrollbar(lista, orient="vertical", command=canvas_modos.yview)
def atualizar_barra_perfis(inicio, fim):
    scroll_modos.set(inicio, fim)
    precisa_rolagem = float(inicio) > 0.0 or float(fim) < 1.0
    if precisa_rolagem and not scroll_modos.winfo_manager():
        scroll_modos.pack(side="right", fill="y", before=canvas_modos)
    elif not precisa_rolagem and scroll_modos.winfo_manager():
        scroll_modos.pack_forget()


canvas_modos.configure(yscrollcommand=atualizar_barra_perfis)
canvas_modos.pack(side="left", fill="both", expand=True)
frame_modos = tk.Frame(canvas_modos, bg=COR_FUNDO)
janela_modos = canvas_modos.create_window((0, 0), window=frame_modos, anchor="nw")
frame_modos.bind("<Configure>", lambda event: canvas_modos.configure(
    scrollregion=canvas_modos.bbox("all")))
canvas_modos.bind("<Configure>", lambda event: canvas_modos.itemconfigure(
    janela_modos, width=event.width))
def rolar_perfis(event):
    if scroll_modos.winfo_manager():
        canvas_modos.yview_scroll(int(-event.delta / 120), "units")
janela.bind("<MouseWheel>", rolar_perfis)

# INICIA PROGRAMA
# ============================================================

# 1) Tenta usar o path salvo de uma vez anterior (manual ou automático).
PASTA_BDO = carregar_pasta_bdo_salva()

# 2) Por via das dúvidas, roda a validação de novo: o jogo pode ter
#    sido movido, reinstalado ou desinstalado desde a última vez.
if not bdo_valido(PASTA_BDO):
    # 3) Só cai na busca automática pelo sistema se o path salvo
    #    não existir mais ou não for mais válido.
    PASTA_BDO = procurar_bdo()

# 4) Sempre que houver um path válido (salvo ou recém-encontrado),
#    garante que ele fique salvo para a próxima abertura.
if PASTA_BDO and bdo_valido(PASTA_BDO):
    salvar_pasta_bdo(PASTA_BDO)

atualizar_status()
criar_botoes_modos()
atualizar_modo_instalado()

janela.after(0, mostrar_janela)
janela.mainloop()
