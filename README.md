# 🎮 BDO Mode Manager

Aplicativo para Windows que configura o **Black Desert Online para usar Vulkan no lugar de DirectX 11**, por meio das DLLs do **DXVK**. Essa camada permite personalizar a renderização das texturas e outras opções gráficas via `dxvk.conf`, incluindo o famoso **modo batata**, que reduz a qualidade visual das texturas para priorizar o desempenho.

O programa automatiza a instalação das DLLs e a troca entre os perfis **Normal** e **Batata**, com uma interface gráfica em Python/Tkinter. A conversão de DirectX para Vulkan é feita pelo DXVK; o aplicativo gerencia seus arquivos e configurações.

## ✨ Funcionalidades

- Localiza automaticamente a instalação do Black Desert Online ou permite selecionar a pasta manualmente.
- Salva o caminho do jogo em `config.json` para reutilizá-lo nas próximas aberturas.
- Aplica o `dxvk.conf` do perfil escolhido e copia as DLLs para a pasta `bin64` do jogo, sem sobrescrever DLLs existentes.
- Identifica qualquer perfil comparando as opções ativas do `dxvk.conf` instalado com os perfis disponíveis, ignorando comentários, espaços ao redor das opções, ordem das linhas e diferenças de quebra de linha.
- Faz backup temporário do `dxvk.conf` durante a aplicação e tenta reverter as alterações em caso de falha.
- Remove as configurações e as DLLs correspondentes ao usar **Remover DXVK**.
- Bloqueia a aplicação de perfis e a remoção do DXVK enquanto o Black Desert está aberto; se não conseguir verificar os processos, não altera os arquivos.
- Adapta a interface ao tema claro ou escuro do Windows.
- Exibe cartões com descrições dos perfis, destaca o perfil ativo e mostra a barra de rolagem apenas quando necessária.
- Usa um ícone próprio na barra de título e na barra de tarefas, com animações nativas ao minimizar e restaurar.
- Mantém uma única instância: abrir novamente traz a janela existente para frente e a restaura se estiver minimizada, mesmo ao executar outra cópia do aplicativo em uma pasta diferente.
- Explica a remoção do DXVK por um tooltip no botão **Remover DXVK**.

## 🖥️ Requisitos

- Windows.
- Python 3 com Tkinter instalado e a extensão `.pyw` associada ao Python. O programa utiliza apenas módulos da biblioteca padrão, sem dependências Python externas.
- Placa de vídeo e driver com suporte a Vulkan compatível com as DLLs DXVK incluídas.
- Black Desert Online instalado, com a pasta `bin64` acessível para gravação.

## 📁 Estrutura do projeto

Mantenha o script, as DLLs e os perfis na seguinte organização:

```text
bdo-mode-manager/
├── BDO Mode Manager.lnk
├── setup_shortcuts.vbs
├── launch.vbs
├── BDO_Mode_Manager.pyw
├── LICENSE
├── README.md
├── assets/
│   ├── bdo-mode-manager-spirit-outline.ico
│   ├── bdo-mode-manager-spirit-outline.png
│   └── bdo-mode-manager-title.png
├── bin64/
│   ├── d3d11.dll
│   └── dxgi.dll
└── game_modes/
    ├── Batata/
    │   └── dxvk.conf
    └── Normal/
        └── dxvk.conf
```

| Arquivo ou pasta | Função |
|---|---|
| `BDO Mode Manager.lnk` | Atalho com ícone próprio; entrada principal do aplicativo. Mantenha-o na pasta do app. |
| `setup_shortcuts.vbs` | Configura o ícone em `%LOCALAPPDATA%\BDOModeManager` e cria o atalho da área de trabalho. |
| `launch.vbs` | Inicializador usado pelo atalho para localizar o Python e abrir o aplicativo. |
| `BDO_Mode_Manager.pyw` | Interface e gerenciamento dos arquivos do jogo. |
| `assets/` | Ícone do aplicativo e imagem da barra de título. |
| `bin64/` | DLLs DXVK copiadas para a pasta `bin64` do jogo. |
| `game_modes/<nome>/dxvk.conf` | Configuração gráfica de cada perfil. |
| `config.json` | Caminho salvo da instalação do jogo; criado ou atualizado pelo aplicativo. |

## ⚠️ Avisos

- O programa altera arquivos dentro da pasta de instalação do jogo (`bin64`). **Use por sua conta e risco.**
- O uso de DLLs de terceiros e a modificação da renderização do cliente **podem infringir as regras ou os termos de uso do Black Desert Online**. Consulte as políticas oficiais da Pearl Abyss antes de utilizar; este projeto não garante que essas alterações sejam permitidas.
- Mantenha uma cópia de segurança da pasta `bin64` original do jogo antes do primeiro uso.
- Feche o jogo antes de aplicar ou remover um perfil.
- O ganho de desempenho do modo batata depende do hardware e das configurações utilizadas.

## ▶️ Como usar

> [!IMPORTANT]
> **Desbloqueie o ZIP antes de extrair no Windows.** Clique com o botão direito no arquivo baixado → **Propriedades** → marque **Desbloquear**, se disponível → **Aplicar**. Só então extraia o pacote e execute o configurador.
>
> Se aparecer o aviso **“O Controle de Aplicativo Inteligente bloqueou um arquivo”**, e você já tiver extraído o ZIP, desbloqueie o ZIP original e extraia novamente para uma nova pasta. Esse procedimento resolveu o bloqueio observado, sem desativar a proteção do Windows. Use apenas o pacote deste repositório; se o aviso continuar, não há garantia de liberação por esse procedimento.

1. Na página de [Releases](https://github.com/AirtonSerra/bdo-mode-manager/releases/latest), abra **Assets** e baixe **BDO-Mode-Manager-v<VERSÃO>-Windows.zip** da versão mais recente. Escolha o pacote para Windows; os arquivos **Source code** são cópias do código do repositório.
2. Siga o aviso acima para desbloquear o ZIP e extraia **todo o conteúdo** para uma pasta. Não abra o aplicativo dentro do ZIP e mantenha os arquivos extraídos juntos.
3. Instale **Python 3 com Tkinter e o launcher do Python**, caso ainda não estejam instalados. O pacote usa Python e não é um executável independente.
4. No primeiro uso, execute **setup_shortcuts.vbs** na pasta extraída. Ele configura o ícone em `%LOCALAPPDATA%\BDOModeManager` e cria o atalho na área de trabalho.
5. Abra o atalho **BDO Mode Manager** na pasta extraída ou na área de trabalho. Essa é a entrada principal do aplicativo; o inicializador localiza o Python sem depender da associação de arquivos `.pyw`.

   Se necessário, também é possível executar diretamente:

   ```powershell
   pythonw .\BDO_Mode_Manager.pyw
   ```

6. Feche o Black Desert Online antes de aplicar um perfil ou remover o DXVK. O aplicativo bloqueia essas operações enquanto o jogo está aberto.
7. Aguarde a localização automática do jogo. Caso necessário, clique em **Alterar pasta** e escolha a pasta de instalação que contém `bin64`.
8. Clique em **Aplicar** no cartão **Batata** ou **Normal**. O perfil identificado fica destacado como **Ativo**. Depois, abra o jogo normalmente.
9. Para retornar ao DirectX original, feche o jogo, clique em **Remover DXVK** e confirme a remoção das DLLs e da configuração instaladas pelo gerenciador.

Para fixar o aplicativo na barra de tarefas, abra-o, clique com o botão direito no ícone da janela na barra de tarefas e selecione **Fixar na barra de tarefas**. Abrir novamente o aplicativo traz a janela existente para frente, inclusive se estiver minimizada.

> [!TIP]
> **Atualizando de uma versão anterior:** desafixe o item antigo, feche o app, abra a versão atualizada pelo atalho e fixe novamente o ícone da janela. O Windows não atualiza automaticamente os itens já fixados.
>
> **Se mover a pasta do aplicativo:** execute **setup_shortcuts.vbs** novamente para recriar o atalho da área de trabalho e refaça a fixação na barra de tarefas.

## 🎨 Perfis disponíveis

| Perfil | Comportamento |
|---|---|
| 🥔 **Batata** | Configura um LOD de texturas elevado (`d3d11.samplerLodBias`), desativa MSAA e ajusta tesselação e filtragem anisotrópica para reduzir a qualidade gráfica. |
| 🖼️ **Normal** | Mantém a qualidade gráfica original do jogo, usando DXVK para renderizar com Vulkan no lugar do DirectX. |

**Os dois perfis usam DXVK/Vulkan.** Selecionar **Normal** não remove essa camada nem retorna ao DirectX original. Para remover a camada instalada pelo gerenciador, use **Remover DXVK**.

Para personalizar um perfil, edite seu `dxvk.conf` e aplique-o novamente. Para adicionar outro perfil, crie uma subpasta em `game_modes/` com um `dxvk.conf`; ela aparecerá na lista na próxima abertura do aplicativo.

## ⚙️ Como funciona

Ao aplicar um perfil, o programa faz uma cópia temporária do `dxvk.conf` existente, instala a configuração selecionada e copia as DLLs ausentes para a pasta `bin64` do jogo. Se houver falha, tenta remover as DLLs copiadas nessa operação e restaurar a configuração anterior. O backup temporário é removido ao final do processo.

O perfil instalado é identificado pelas opções ativas do `dxvk.conf`, sem depender do nome do perfil. Comentários, linhas vazias, ordem das opções, quebras de linha LF/CRLF e a marca BOM do UTF-8 não interferem na comparação. Os valores `True`/`true`, `False`/`false` e `Auto`/`auto` são considerados equivalentes; diferenças nos demais valores continuam relevantes.

Quando não há correspondência, a interface distingue **Sem configuração instalada**, **Configuração personalizada ou desconhecida** e **Configuração ilegível ou inválida**. Se vários perfis têm as mesmas opções, informa **Perfis equivalentes** sem marcar um deles como ativo arbitrariamente. Essas indicações identificam a configuração; não verificam se o jogo está usando Vulkan.

A desinstalação remove o `dxvk.conf` e as DLLs com os mesmos nomes das presentes na pasta `bin64` do programa. Ela não restaura um backup permanente da instalação original e pode remover DLLs de mesmo nome que já existiam antes do uso do gerenciador.

## 📜 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
