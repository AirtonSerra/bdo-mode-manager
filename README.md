# BDO Mode Manager

Aplicativo para Windows que gerencia os perfis **Normal** e **Batata** do Black Desert Online com DXVK, uma camada que traduz DirectX 11 para Vulkan.

**A distribuição atual é um instalador `.exe`. Você não precisa instalar Python, Tkinter nem baixar DLLs separadamente:** os componentes necessários ao gerenciador já acompanham o pacote.

## Baixar e instalar

1. Acesse a página de [Releases](https://github.com/AirtonSerra/bdo-mode-manager/releases/latest).
2. Em **Assets**, baixe o instalador `BDO-Mode-Manager-v<VERSÃO>-Setup.exe`. Os downloads **Source code (zip)** e **Source code (tar.gz)** são destinados ao desenvolvimento.
3. Execute o instalador e autorize a solicitação de administrador.
4. Leia o aviso de uso. Para avançar, aguarde os 15 segundos de leitura e marque o aceite. Se não concordar, cancele a instalação.
5. Escolha a pasta de destino e conclua a instalação. O destino padrão é `Arquivos de Programas\BDO Mode Manager`.
6. Abra **BDO Mode Manager** pelo menu Iniciar ou pelo atalho na área de trabalho, cuja criação vem marcada por padrão no instalador.

O instalador instala o aplicativo para todos os usuários do computador. Não é necessário extrair ZIP, executar arquivos `.vbs` ou configurar atalhos manualmente. A instalação silenciosa é recusada porque o aviso exige leitura e aceite na interface.

## Requisitos para usar

- Windows de 64 bits compatível com o instalador.
- Black Desert Online instalado, com acesso de gravação à sua pasta `bin64`.
- Placa de vídeo e driver com suporte a Vulkan compatível com as DLLs DXVK incluídas.
- Permissão de administrador para instalar e desinstalar o gerenciador.

Python é necessário apenas para trabalhar com o código-fonte ou gerar uma nova distribuição. As instruções ficam no [README de desenvolvimento](scripts/README.md).

## Como usar

1. Feche o Black Desert Online.
2. Abra o gerenciador. Ele reutiliza o caminho salvo quando válido; caso contrário, procura o jogo em segundo plano e mostra o andamento da busca.
3. Se o jogo não for encontrado, use **Alterar pasta** e selecione a pasta de instalação que contém `bin64`.
4. Clique em **Aplicar** no perfil desejado. Após a confirmação de sucesso, abra o jogo normalmente.
5. Para remover a camada instalada pelo gerenciador, feche o jogo, clique em **Remover DXVK** e confirme.

| Perfil | O que aplica |
|---|---|
| **Batata** | Usa DXVK/Vulkan com configurações que reduzem a qualidade visual: LOD de texturas elevado, MSAA desativado e ajustes de tesselação e filtragem anisotrópica. |
| **Normal** | Usa DXVK/Vulkan sem os ajustes de redução de qualidade do perfil Batata, mantendo as demais opções do seu `dxvk.conf`. |

**Normal também usa DXVK.** Para remover essa camada e voltar à renderização original do jogo, use **Remover DXVK**. O ganho de desempenho depende do hardware, do driver e das configurações do jogo.

O aplicativo impede a aplicação e a remoção enquanto detecta o Black Desert aberto. Se não conseguir verificar os processos, também não altera os arquivos.

## O que acompanha o instalador

| Conteúdo | Finalidade |
|---|---|
| `BDO Mode Manager.exe` | Aplicativo com interface gráfica. |
| Runtime Python, Tcl/Tk e bibliotecas auxiliares | Permitem executar o gerenciador sem instalar Python ou Tkinter na máquina. |
| `bin64/d3d11.dll` e `bin64/dxgi.dll` | DLLs DXVK destinadas à pasta `bin64` do jogo. |
| `game_modes/Normal/dxvk.conf` e `game_modes/Batata/dxvk.conf` | Configurações dos perfis disponíveis. |
| `assets/` | Imagens e ícone do aplicativo. |
| `README.md`, `LICENSE` e `AVISO-DE-USO.txt` | Instruções, licença e aviso de uso. |

O EXE instalado utiliza os arquivos que o acompanham. Mantenha a pasta de instalação completa e use o instalador para escolher o destino, em vez de mover apenas o executável.

## Como os arquivos do jogo são alterados

Ao aplicar um perfil, o gerenciador instala seu `dxvk.conf` na pasta `bin64` do jogo e copia as DLLs ausentes. **DLLs que já existem não são sobrescritas.** Os executáveis originais do jogo não são editados.

Durante a aplicação, o `dxvk.conf` anterior recebe um backup temporário. Se ocorrer uma falha, o aplicativo tenta restaurá-lo e remover as DLLs copiadas naquela operação. Esse backup é removido ao final; não é uma cópia permanente da instalação original.

**Remover DXVK** apaga o `dxvk.conf` e os arquivos do jogo com os mesmos nomes das DLLs incluídas no `bin64` do gerenciador, atualmente `d3d11.dll` e `dxgi.dll`. A remoção pode apagar DLLs de mesmo nome que já estavam no jogo antes do uso do aplicativo. Faça uma cópia de segurança da pasta `bin64` original antes do primeiro uso.

## Perfil ativo e interface

O perfil **Ativo** é identificado pelas opções do `dxvk.conf` instalado, comparadas com os perfis disponíveis. Comentários, ordem das opções, espaços ao redor delas e diferenças de quebra de linha não interferem na identificação.

Quando não há correspondência única, a interface informa se a configuração está ausente, personalizada ou desconhecida, ilegível ou inválida, ou se existem perfis equivalentes. Essa identificação não confirma que o jogo esteja renderizando com Vulkan.

A interface acompanha o tema claro ou escuro do Windows. Apenas uma instância fica aberta por sessão do Windows: abrir o gerenciador novamente traz a janela existente para frente e a restaura se estiver minimizada, inclusive ao executar outra cópia em uma pasta diferente.

Para fixá-lo na barra de tarefas, abra o aplicativo, clique com o botão direito em seu ícone na barra e selecione **Fixar na barra de tarefas**. Após atualizar uma versão antiga, se o item fixado continuar apontando para o aplicativo anterior, desafixe-o e fixe novamente a versão atual.

## Configurações, atualização e desinstalação

O caminho do jogo é salvo por usuário em:

```text
%LOCALAPPDATA%\BDOModeManager\config.json
```

Esse arquivo fica separado da instalação e é preservado nas atualizações e na desinstalação. Quando ainda não existe uma configuração nesse local, o aplicativo tenta importar um `config.json` antigo ao lado do executável. Se a versão antiga estava em outra pasta, pode ser necessário selecionar o jogo novamente.

Para atualizar, feche o gerenciador e execute o instalador da nova versão, escolhendo a pasta de destino desejada.

Para desinstalar, use a opção do Windows para remover aplicativos. A desinstalação solicita permissão de administrador e remove os arquivos e atalhos do gerenciador, mas **não remove o DXVK do jogo**. Se desejar removê-lo, use **Remover DXVK** no aplicativo antes de desinstalar.

## Problemas comuns

- **Jogo não encontrado:** use **Alterar pasta** e selecione a pasta que contém `bin64`.
- **Sem permissão para alterar o jogo:** verifique o acesso de gravação à pasta do jogo. Se necessário, abra o gerenciador como administrador.
- **Operação bloqueada com o jogo aberto:** feche o Black Desert e tente novamente.
- **Perfil personalizado ou desconhecido:** o `dxvk.conf` instalado não corresponde aos perfis disponíveis. Aplicar um perfil substitui essa configuração.
- **Arquivos do aplicativo ausentes:** reinstale pelo instalador para recuperar o pacote completo.

## Aviso de uso

O aplicativo é gratuito, de código aberto e não possui vínculo com a Pearl Abyss nem autorização declarada da operadora. O aviso incluído no instalador informa que o uso de DLLs de terceiros pode contrariar as políticas do Black Desert Online e resultar em advertências, suspensão ou banimento. Consulte as regras oficiais antes de decidir utilizar o programa.

O build atual não inclui assinatura digital. Se o Windows apresentar um aviso ou bloqueio, confira a origem do arquivo na release do projeto. O arquivo `.exe.sha256` publicado junto ao instalador permite conferir sua integridade; ele não substitui uma assinatura digital.

O texto completo das condições acompanha a instalação em [AVISO-DE-USO.txt](installer/AVISO-DE-USO.txt). O software é fornecido sob a [Licença MIT](LICENSE).
