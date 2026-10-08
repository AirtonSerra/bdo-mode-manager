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
> **Antes de extrair o ZIP no Windows:** clique com o botão direito no ZIP baixado → **Propriedades** → marque **Desbloquear**, se essa opção aparecer → **Aplicar**. Depois extraia todo o conteúdo. Isso pode resolver o aviso do Controle de Aplicativo Inteligente sobre arquivos vindos da Internet, como confirmado no uso desta versão.
>
> Se já extraiu o pacote antes de desbloquear, desbloqueie o ZIP e extraia novamente para uma nova pasta. Faça isso apenas para o pacote obtido deste repositório; não é necessário desativar a proteção do Windows. Se o bloqueio continuar, esse procedimento não garante a liberação de arquivos considerados não confiáveis pelo sistema.

1. Baixe o ZIP para Windows na página de [Releases](https://github.com/AirtonSerra/bdo-mode-manager/releases), siga o aviso acima e extraia todo o conteúdo para uma pasta.
2. Feche o Black Desert Online antes de aplicar ou remover um perfil.
3. No primeiro uso, execute **setup_shortcuts.vbs** para configurar o ícone e criar o atalho na área de trabalho. Depois abra **BDO Mode Manager** na pasta extraída ou na área de trabalho. Mantenha os arquivos da pasta juntos; se mover a pasta, execute o configurador novamente.

   Se necessário, também é possível executar diretamente:

   ```powershell
   pythonw .\BDO_Mode_Manager.pyw
   ```

4. Aguarde a localização automática do jogo. Caso necessário, clique em **Alterar pasta** e escolha a pasta de instalação que contém `bin64`.
5. Clique em **Aplicar** no cartão **Batata** ou **Normal**. O perfil identificado fica destacado como **Ativo**.
6. Para remover os arquivos do DXVK e a configuração aplicada, clique em **Remover DXVK** e confirme.

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
