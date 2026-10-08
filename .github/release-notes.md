Versão para Windows com os arquivos necessários para usar o BDO Mode Manager.

### Download e uso

1. Baixe o arquivo **BDO-Mode-Manager-v1.0.1-Windows.zip** em Assets.
2. Extraia o ZIP inteiro para uma pasta; não abra o aplicativo dentro do ZIP.
3. Instale Python 3 com Tkinter e o launcher do Python.
4. Abra o atalho **BDO Mode Manager** na pasta extraída.
5. Selecione a instalação do jogo e clique em **Aplicar** no perfil desejado.

O pacote inclui o atalho com ícone próprio, inicializador, aplicativo Python, DLLs DXVK, perfis Normal/Batata na pasta `game_modes`, ícones, README e licença. Não inclui configuração pessoal, testes ou arquivos de desenvolvimento. Não é um executável independente: Python precisa estar instalado.

Nesta versão, o atalho usa um inicializador que localiza o Python, sem depender da associação de arquivos `.pyw` no Windows.

### Recursos

- Perfis Normal e Batata usando DXVK/Vulkan no lugar do DirectX.
- Detecção dos perfis pelas opções ativas, sem depender das quebras de linha.
- Bloqueio de aplicação e remoção enquanto o Black Desert estiver aberto.
- Interface com cartões, ícone próprio e integração à barra de tarefas.
- Remoção do DXVK com confirmação para voltar ao DirectX original.

### Avisos

O programa altera arquivos da pasta `bin64` do jogo. Mantenha um backup e use por sua conta e risco. O uso de DLLs de terceiros e modificações do cliente pode infringir as regras ou os termos de uso do Black Desert Online; consulte as políticas da Pearl Abyss.

O arquivo `.sha256` permite verificar a integridade do ZIP.
