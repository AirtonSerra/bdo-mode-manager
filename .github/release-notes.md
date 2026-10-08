### Correções da v1.0.1

- Corrige o ícone e a abertura do aplicativo ao fixar a janela na barra de tarefas do Windows.
- Define o inicializador correto para o item fixado, mantendo a instância única.

> [!TIP]
> **Atualizando de uma versão anterior:** desafixe o item antigo, feche o app, abra esta versão e fixe novamente o ícone da janela. O Windows não atualiza automaticamente os itens já fixados. Se mover a pasta, refaça a fixação.

Versão para Windows com os arquivos necessários para usar o BDO Mode Manager.

> [!IMPORTANT]
> **Desbloqueie o ZIP antes de extrair no Windows.** Clique com o botão direito no arquivo baixado → **Propriedades** → marque **Desbloquear**, se disponível → **Aplicar**. Só então extraia o pacote e execute o configurador.
>
> Se aparecer o aviso **“O Controle de Aplicativo Inteligente bloqueou um arquivo”**, e você já tiver extraído o ZIP, desbloqueie o ZIP original e extraia novamente para uma nova pasta. Esse procedimento resolveu o bloqueio observado nesta versão, sem desativar a proteção do Windows. Use apenas o pacote deste repositório; se o aviso continuar, não há garantia de liberação por esse procedimento.

### Download e uso

1. Baixe o arquivo **BDO-Mode-Manager-v1.0.1-Windows.zip** em Assets.
2. Siga o aviso acima para desbloquear o ZIP e extraia todo o conteúdo para uma pasta; não abra o aplicativo dentro do ZIP.
3. Instale Python 3 com Tkinter e o launcher do Python.
4. No primeiro uso, execute **setup_shortcuts.vbs** para configurar o ícone e criar o atalho na área de trabalho. Depois abra **BDO Mode Manager** na pasta extraída ou na área de trabalho. Se mover a pasta, execute o configurador novamente.
5. Selecione a instalação do jogo e clique em **Aplicar** no perfil desejado.

O pacote inclui o atalho com ícone próprio, inicializador, aplicativo Python, DLLs DXVK, perfis Normal/Batata na pasta `game_modes`, ícones, README e licença. Não inclui configuração pessoal, testes ou arquivos de desenvolvimento. Não é um executável independente: Python precisa estar instalado.

Esta versão corrige os ícones dos atalhos na pasta e na área de trabalho. O configurador instala o ícone em `%LOCALAPPDATA%\BDOModeManager` e cria o atalho da área de trabalho com o caminho correto para o aplicativo. O inicializador continua localizando o Python sem depender da associação de arquivos `.pyw`.

### Recursos

- Perfis Normal e Batata usando DXVK/Vulkan no lugar do DirectX.
- Detecção dos perfis pelas opções ativas, sem depender das quebras de linha.
- Bloqueio de aplicação e remoção enquanto o Black Desert estiver aberto.
- Interface com cartões, ícone próprio e integração à barra de tarefas.
- Instância única: abrir o aplicativo novamente traz a janela existente para frente e a restaura se estiver minimizada, inclusive ao abrir outra cópia em uma pasta diferente.
- Remoção do DXVK com confirmação para voltar ao DirectX original.

### Avisos

O programa altera arquivos da pasta `bin64` do jogo. Mantenha um backup e use por sua conta e risco. O uso de DLLs de terceiros e modificações do cliente pode infringir as regras ou os termos de uso do Black Desert Online; consulte as políticas da Pearl Abyss.

O arquivo `.sha256` permite verificar a integridade do ZIP.
