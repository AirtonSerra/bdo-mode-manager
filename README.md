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

## ⚠️ Avisos

- O programa altera arquivos dentro da pasta de instalação do jogo (`bin64`). Use por sua conta e risco.
- Sempre mantenha uma cópia de segurança da pasta `bin64` original do jogo antes do primeiro uso.
- Modificar arquivos do cliente do jogo pode violar os termos de uso do Black Desert Online — verifique as políticas da Pearl Abyss antes de utilizar.

---

## 📜 Licença

Defina aqui a licença de distribuição do projeto (ex.: MIT, GPL-3.0, uso privado, etc.).
