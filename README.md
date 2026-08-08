# BDO Mode Manager

Aplicativo de desktop para Windows que gerencia e aplica **modos de jogo** (perfis de configuração `dxvk.conf` + DLLs) no **Black Desert Online**, com detecção automática da instalação do jogo e interface gráfica personalizada que se adapta ao tema do Windows.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4)
![GUI](https://img.shields.io/badge/GUI-Tkinter-informational)

---

## ✨ Funcionalidades

- **Detecção automática do Black Desert Online**: procura a pasta de instalação em locais comuns (`Program Files`, `Steam`, unidades de disco, etc.) e valida se contém a pasta `bin64`.
- **Seleção manual da pasta do jogo**, com validação do caminho escolhido.
- **Identificação do modo atualmente aplicado**, comparando o hash SHA-256 do `dxvk.conf` instalado com os modos disponíveis.
- **Aplicação de modos com um clique**: copia o `dxvk.conf` do modo escolhido e as DLLs necessárias para a pasta `bin64` do jogo.
- **Backup automático e rollback**: antes de aplicar um modo, o `dxvk.conf` atual é copiado como backup; se algo falhar durante a aplicação, as alterações são revertidas automaticamente.
- **Desinstalação**: remove o `dxvk.conf` e as DLLs aplicadas pelo programa, restaurando a pasta `bin64` do jogo ao estado original.
- **Interface adaptada ao tema do Windows** (claro/escuro), lida diretamente do registro do sistema.
- **Janela customizada**, sem a barra de título padrão do Windows, com suporte a arrastar, minimizar e fechar.

---

## 🖥️ Requisitos

- **Windows** (o programa utiliza o módulo `winreg`, exclusivo do Windows).
- **Python 3** com as bibliotecas padrão `tkinter`, `winreg`, `shutil`, `hashlib` e `os` (todas nativas do Python — nenhuma dependência externa é necessária).

---

## 📁 Estrutura de pastas esperada

O programa deve ser executado a partir de uma pasta com a seguinte organização:

```
BDO Mode Manager/
├── BDO_Mode_Manager.pyw
├── BlackDesert.ico
├── bin64/
│   ├── dll1.dll
│   ├── dll2.dll
│   └── ...
└── Modos de jogo/
    ├── Modo A/
    │   └── dxvk.conf
    ├── Modo B/
    │   └── dxvk.conf
    └── ...
```

| Pasta/arquivo         | Descrição                                                                 |
|------------------------|----------------------------------------------------------------------------|
| `bin64/`               | Contém as DLLs que serão copiadas para a pasta `bin64` do Black Desert.   |
| `Modos de jogo/<nome>/`| Cada subpasta representa um modo de jogo e deve conter um `dxvk.conf`.   |
| `BlackDesert.ico`      | Ícone do aplicativo/jogo.                                                 |

---

## ▶️ Como usar

1. Coloque o arquivo `BDO_Mode_Manager.pyw` na pasta que contém as subpastas `bin64` e `Modos de jogo` (conforme a estrutura acima).
2. Execute o arquivo `BDO_Mode_Manager.pyw` (duplo clique ou `pythonw BDO_Mode_Manager.pyw`).
3. Ao abrir, o programa tenta localizar automaticamente a instalação do Black Desert Online.
   - Caso não encontre, clique em **Selecionar** e escolha manualmente a pasta de instalação do jogo (a pasta deve conter uma subpasta `bin64`).
4. O programa exibirá qual modo (se algum) está atualmente aplicado no jogo.
5. Clique no botão correspondente a um dos **modos de jogo** listados para aplicá-lo.
6. Para remover as alterações feitas pelo programa, clique em **Desinstalar**.

> ⚠️ **Feche o Black Desert Online** antes de aplicar ou remover um modo, para evitar erros de permissão ao gravar arquivos na pasta `bin64`.

---

## ⚙️ Como funciona

### Aplicar um modo
1. Faz backup do `dxvk.conf` atual da pasta `bin64` do jogo (se existir).
2. Copia o `dxvk.conf` do modo selecionado para a `bin64` do jogo.
3. Copia todas as DLLs presentes na pasta `bin64` do programa para a `bin64` do jogo (DLLs já existentes não são sobrescritas).
4. Se qualquer etapa falhar, as DLLs copiadas são removidas e o `dxvk.conf` original é restaurado a partir do backup.
5. O backup temporário é removido ao final do processo.

### Identificar o modo instalado
O programa calcula o hash **SHA-256** do `dxvk.conf` presente na `bin64` do jogo e compara com o hash de cada `dxvk.conf` das pastas em `Modos de jogo/`, exibindo o nome do modo correspondente (ou "Nenhum" caso não haja correspondência).

### Desinstalar
Remove o `dxvk.conf` e todas as DLLs presentes na pasta `bin64` do programa que também estejam na `bin64` do jogo, restaurando-a ao estado anterior à aplicação de qualquer modo.

---

## 🎨 Interface

- A janela detecta automaticamente se o Windows está em **tema claro ou escuro** (via registro `AppsUseLightTheme`) e ajusta as cores da interface de acordo.
- Barra de título personalizada com botões de **minimizar** e **fechar**, e suporte para arrastar a janela clicando e segurando o topo.

---

## 📦 Gerando o executável (.exe)

O `BDO_Mode_Manager.pyw` pode ser compilado em um executável autônomo (`.exe`) usando o **PyInstaller**, através do script `build.bat` incluído no repositório.

### Dependências para compilar

| Dependência | Observação |
|---|---|
| **Python 3.12** | Recomendado especificamente. Versões instaladas pelo novo *Python Install Manager* (ex.: Python 3.13/3.14 instalados via `py install`) usam uma estrutura de pastas (`AppData\Local\Python\pythoncore-X.Y-64`) que o PyInstaller ainda não localiza corretamente, causando falha ao empacotar os dados do Tcl/Tk (`FileNotFoundError: Tcl data directory ... not found`). Use o [instalador clássico do Python 3.12](https://www.python.org/downloads/release/python-3120/) para evitar esse problema. |
| **PyInstaller** | Instalado automaticamente pelo `build.bat`, caso ainda não esteja presente (`pip install pyinstaller`). |
| **`bin64/`** e **`Modos de jogo/`** | Precisam existir na raiz do projeto antes de rodar o build — são copiadas automaticamente para dentro da pasta de saída. |

### Como compilar

1. Certifique-se de que o Python 3.12 está instalado (`py list` deve listar `3.12`).
2. Rode o `build.bat` na raiz do projeto:
   ```powershell
   .\build.bat
   ```
3. O script executa, em sequência: limpeza de builds anteriores → compilação com PyInstaller (`--onedir --windowed`) → cópia das pastas `bin64` e `Modos de jogo` para dentro da pasta de saída.
4. O resultado final fica em `dist\BDO Mode Manager\` — essa pasta inteira (com o `.exe`, a subpasta `_internal`, `bin64` e `Modos de jogo`) é o que deve ser distribuído/zipado.

> ⚠️ **Importante ao criar o `build.bat`**: se você **baixar** o arquivo `.bat` diretamente de um navegador, chat, ou link (mesmo deste repositório), o Windows marca o arquivo com o atributo *Mark of the Web* (MOTW) — a flag de "veio da internet". Isso é o mesmo motivo que faz o `.exe` compilado ser bloqueado pelo **Controle de Aplicativo Inteligente** ao ser distribuído (veja a seção seguinte).
>
> Se o `.bat` baixado for bloqueado ou gerar avisos ao rodar, a forma mais confiável de contornar é: **criar um novo arquivo `.bat` manualmente** (botão direito → Novo → Documento de Texto → renomear a extensão para `.bat`) e **colar o conteúdo do script dentro dele**, em vez de executar o arquivo baixado diretamente. Um arquivo criado localmente dessa forma não recebe a marcação MOTW, então roda sem passar pelas verificações extras de segurança do Windows.

---

## 🔒 Sobre o bloqueio de segurança do Windows no .exe distribuído

Ao distribuir o `.exe` gerado (via zip, Discord, Google Drive, etc.), quem for baixar pode ver o aviso **"O Controle de aplicativo inteligente bloqueou um arquivo que pode não ser seguro"**. Isso acontece porque o executável não possui uma **assinatura digital de código** reconhecida pela Microsoft — é o comportamento padrão do Windows para qualquer executável de terceiros baixado da internet, independentemente de o programa ser seguro ou não.

Para o usuário final destravar a execução, uma das opções abaixo resolve:

- **Desbloquear o arquivo**: botão direito no `.exe` → Propriedades → aba Geral → marcar "Desbloquear" → Aplicar.
- **Desligar o Controle de Aplicativo Inteligente** (se ainda estiver em modo "Avaliação"): Configurações → Privacidade e segurança → Segurança do Windows → Controle de aplicativos e navegador → Controle de aplicativo inteligente → Desligado.

Para eliminar esse aviso definitivamente para todos os usuários, seria necessário assinar o executável com um certificado de assinatura de código (pago) ou distribuir via Microsoft Store.

---

## ⚠️ Avisos

- O programa altera arquivos dentro da pasta de instalação do jogo (`bin64`). Use por sua conta e risco.
- Sempre mantenha uma cópia de segurança da pasta `bin64` original do jogo antes do primeiro uso.
- Modificar arquivos do cliente do jogo pode violar os termos de uso do Black Desert Online — verifique as políticas da Pearl Abyss antes de utilizar.

---

## 📜 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

Você é livre para usar, copiar, modificar e distribuir este software, desde que mantenha o aviso de copyright original.
