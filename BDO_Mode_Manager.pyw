import os
import json
import shutil
import hashlib
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
# HASH
# ============================================================

def calcular_hash(caminho):
    sha256 = hashlib.sha256()
    try:
        with open(caminho, "rb") as arquivo:
            while True:
                bloco = arquivo.read(1024 * 1024)
                if not bloco:
                    break
                sha256.update(bloco)
        return sha256.hexdigest()
    except (OSError, IOError):
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

def identificar_modo_instalado():
    if not PASTA_BDO or not bdo_valido(PASTA_BDO):
        return None

    arquivo_bdo = os.path.join(obter_bin64_bdo(), NOME_ARQUIVO)
    if not os.path.isfile(arquivo_bdo):
        return None

    hash_bdo = calcular_hash(arquivo_bdo)
    if not hash_bdo:
        return None

    for modo in listar_modos():
        arquivo_modo = os.path.join(PASTA_MODOS, modo, NOME_ARQUIVO)
        if not os.path.isfile(arquivo_modo):
            continue

        hash_modo = calcular_hash(arquivo_modo)
        if hash_modo and hash_modo == hash_bdo:
            return modo

    return None


# ============================================================
# ATUALIZAR LABEL DO MODO
# ============================================================

def atualizar_modo_instalado():
    modo = identificar_modo_instalado()

    if modo:
        modo_var.set(f"Modo de jogo aplicado: {modo}")
        modo_label.config(fg=COR_SUCESSO)
    else:
        modo_var.set("Modo de jogo aplicado: Nenhum")
        modo_label.config(fg=COR_TEXTO_SECUNDARIO)


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

        confirmar = messagebox.askyesno(
            "BDO Mode Manager - Desinstalar",
            "Isso irá remover da bin64 do BDO:\n\n"
            "• dxvk.conf\n"
            "• Todas as DLLs presentes na bin64 do BDO Mode Manager\n\n"
            "Deseja continuar?"
        )

        if not confirmar:
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

    if not modos:
        aviso = tk.Label(
            frame_modos,
            text=(
                "Nenhum modo de jogo encontrado.\n\n"
                "Verifique a pasta:\n"
                f"{PASTA_MODOS}"
            ),
            font=("Arial", 11),
            justify="center",
            bg=COR_FUNDO,
            fg=COR_TEXTO_SECUNDARIO
        )
        aviso.pack(pady=20)
        return

    for nome_modo in modos:
        botao = tk.Button(
            frame_modos,
            text=nome_modo,
            font=("Arial", 13),
            width=25,
            height=2,
            bg=COR_BOTAO,
            fg=COR_BOTAO_TEXTO,
            activebackground=COR_BOTAO_ATIVO,
            activeforeground=COR_BOTAO_TEXTO,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda modo=nome_modo: trocar_modo(modo)
        )
        botao.pack(pady=5)


# ============================================================
# MINIMIZAR / RESTAURAR / FECHAR
# ============================================================

def minimizar_janela():
    janela.overrideredirect(False)
    janela.iconify()


def restaurar_janela(event=None):
    try:
        if janela.state() == "normal":
            janela.overrideredirect(True)
    except tk.TclError:
        pass


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

janela = tk.Tk()
janela.title("BDO Mode Manager")

largura_janela = 520
altura_janela = 590

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

pos_x = (largura_tela - largura_janela) // 2
pos_y = (altura_tela - altura_janela) // 2

janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

janela.resizable(False, False)
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

titulo = tk.Label(
    janela,
    text="BDO Mode Manager",
    font=("Arial", 20, "bold"),
    bg=COR_FUNDO,
    fg=COR_TEXTO
)
titulo.pack(pady=(25, 5))


# ============================================================
# SUBTÍTULO
# ============================================================

subtitulo = tk.Label(
    janela,
    text="Selecione o modo de jogo:",
    font=("Arial", 13),
    bg=COR_FUNDO,
    fg=COR_TEXTO_SECUNDARIO
)
subtitulo.pack(pady=(0, 15))


# ============================================================
# PASTA DO BDO
# ============================================================

label_bdo = tk.Label(
    janela,
    text="Pasta do Black Desert:",
    font=("Arial", 11, "bold"),
    bg=COR_FUNDO,
    fg=COR_TEXTO
)
label_bdo.pack(pady=(5, 5))


# ============================================================
# CAMPO DO PATH
# ============================================================

frame_path = tk.Frame(janela, bg=COR_FUNDO)
frame_path.pack(padx=20, fill="x")

texto_path = tk.StringVar()

frame_entrada_path = tk.Frame(
    frame_path,
    bg=COR_BORDA,
    bd=1,
    relief="solid"
)
frame_entrada_path.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=4
)

entrada_path = tk.Entry(
    frame_entrada_path,
    textvariable=texto_path,
    font=("Arial", 10),
    state="readonly",
    readonlybackground=COR_ENTRADA,
    fg=COR_TEXTO,
    relief="flat",
    bd=0,
    highlightthickness=0
)
entrada_path.pack(fill="both", expand=True, padx=6, pady=3)


# ============================================================
# BOTÃO SELECIONAR
# ============================================================

botao_selecionar = tk.Button(
    frame_path,
    text="Selecionar",
    font=("Arial", 10),
    bg=COR_BOTAO,
    fg=COR_BOTAO_TEXTO,
    activebackground=COR_BOTAO_ATIVO,
    activeforeground=COR_BOTAO_TEXTO,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=selecionar_bdo
)
botao_selecionar.pack(side="left", padx=(8, 0), ipady=2)


# ============================================================
# STATUS DO BDO
# ============================================================

status_var = tk.StringVar()

status_label = tk.Label(
    janela,
    textvariable=status_var,
    font=("Arial", 10, "bold"),
    bg=COR_FUNDO
)
status_label.pack(pady=(8, 5))


# ============================================================
# MODO INSTALADO
# ============================================================

modo_var = tk.StringVar()

modo_label = tk.Label(
    janela,
    textvariable=modo_var,
    font=("Arial", 11, "bold"),
    bg=COR_FUNDO
)
modo_label.pack(pady=(3, 15))


# ============================================================
# ÁREA DOS MODOS
# ============================================================

frame_modos = tk.Frame(janela, bg=COR_FUNDO)
frame_modos.pack(fill="both", expand=True, padx=20)


# ============================================================
# BOTÃO DESINSTALAR
# ============================================================

botao_desinstalar = tk.Button(
    janela,
    text="Desinstalar",
    font=("Arial", 12),
    width=25,
    height=2,
    bg=COR_BOTAO,
    fg=COR_BOTAO_TEXTO,
    activebackground=COR_BOTAO_ATIVO,
    activeforeground=COR_BOTAO_TEXTO,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=desinstalar
)
botao_desinstalar.pack(pady=(5, 20))


# ============================================================
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

janela.mainloop()
