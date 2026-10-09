# 🎮 BDO Mode Manager

Aplicativo para Windows que configura o **Black Desert Online para usar Vulkan no lugar de DirectX 11**, por meio das DLLs do **DXVK**. Essa camada permite personalizar a renderização das texturas e outras opções gráficas via `dxvk.conf`, incluindo o famoso **modo batata**, que reduz a qualidade visual das texturas para priorizar o desempenho.

O programa automatiza a instalação das DLLs e a troca entre os perfis **Normal** e **Batata**, com uma interface gráfica em Python/Tkinter. A conversão de DirectX para Vulkan é feita pelo DXVK; o aplicativo gerencia seus arquivos e configurações.

## ✨ Funcionalidades

- Abre a janela antes de localizar o Black Desert Online, com indicador de busca e ações bloqueadas durante a procura. A busca ocorre em segundo plano; se o jogo não for encontrado, permite selecionar a pasta manualmente.
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
- A versão instalada inclui Python e Tkinter: o cliente não precisa instalar Python. Para executar o código-fonte, use Python 3 com Tkinter.
- Placa de vídeo e driver com suporte a Vulkan compatível com as DLLs DXVK incluídas.
- Black Desert Online instalado, com a pasta `bin64` acessível para gravação.

## 📁 Arquivos instalados e dados

O instalador instala para todos os usuários, por padrão em
`Arquivos de Programas\BDO Mode Manager`, e permite escolher outra pasta.
A instalação e a desinstalação solicitam permissão de administrador.
Inclui o executável, Python/Tkinter, `assets/`, `bin64/` e `game_modes/`.
Cria um atalho no menu Iniciar e deixa a opção de atalho na área de trabalho marcada por padrão.
O app não depende dos inicializadores `.vbs` na distribuição instalada.

O instalador apresenta uma tela de boas-vindas antes do aceite.
Antes de instalar, o usuário deve ler o aviso sobre DXVK, políticas do jogo e
responsabilidade pelo uso. A página destaca o risco de suspensão ou banimento;
**Avançar** só é liberado após 15 segundos e com o aceite marcado. Retornar à
página reinicia a contagem e o aceite. A instalação silenciosa é recusada para
não ignorar essa confirmação. O aviso fica disponível em `AVISO-DE-USO.txt`
na pasta instalada, junto à licença MIT. O gerenciador é gratuito e de código
aberto; isso não representa autorização de uso pela operadora do jogo.

O caminho do jogo fica em `%LOCALAPPDATA%\BDOModeManager\config.json`,
separado da instalação. Atualizações e desinstalação preservam esses dados.
Se houver um `config.json` antigo ao lado do script ou executável e ainda não
houver configuração atual, o app tenta importá-lo. Para uma instalação antiga
em outra pasta, selecione o jogo novamente no primeiro uso.

Desinstalar o gerenciador remove seus arquivos e atalhos, mas não remove DXVK
da pasta do jogo. Para isso, use **Remover DXVK** antes de desinstalar.

## ⚠️ Avisos

- O programa altera arquivos dentro da pasta de instalação do jogo (`bin64`). **Use por sua conta e risco.**
- O uso de DLLs de terceiros e a modificação da renderização do cliente **podem infringir as regras ou os termos de uso do Black Desert Online**. Consulte as políticas oficiais da Pearl Abyss antes de utilizar; este projeto não garante que essas alterações sejam permitidas.
- Mantenha uma cópia de segurança da pasta `bin64` original do jogo antes do primeiro uso.
- Feche o jogo antes de aplicar ou remover um perfil.
- O ganho de desempenho do modo batata depende do hardware e das configurações utilizadas.

## ▶️ Como usar

1. Na página de [Releases](https://github.com/AirtonSerra/bdo-mode-manager/releases/latest), baixe **BDO-Mode-Manager-v<VERSÃO>-Setup.exe** em **Assets**. Os arquivos **Source code** são o código-fonte.
2. Execute o instalador, autorize a solicitação de administrador e escolha a pasta. O atalho na área de trabalho vem marcado por padrão e pode ser desmarcado.
3. Abra **BDO Mode Manager** pelo menu Iniciar ou pelo atalho. Não é necessário instalar Python, extrair ZIP ou executar scripts de configuração de atalhos.

> [!IMPORTANT]
> Um instalador sem assinatura digital pode receber avisos do SmartScreen ou ser bloqueado pelo Controle de Aplicativo Inteligente. O formato `.exe` não garante liberação. Não desative as proteções do Windows; para distribuição assinada, o publicador precisa de um certificado confiável. O checksum verifica integridade, mas não substitui assinatura.

4. Feche o Black Desert Online antes de aplicar um perfil ou remover o DXVK. O aplicativo bloqueia essas operações enquanto o jogo está aberto.
5. Aguarde a localização automática do jogo. Caso necessário, clique em **Alterar pasta** e escolha a pasta de instalação que contém `bin64`.
6. Clique em **Aplicar** no cartão **Batata** ou **Normal**. O perfil identificado fica destacado como **Ativo**. Depois, abra o jogo normalmente.
7. Para retornar ao DirectX original, feche o jogo, clique em **Remover DXVK** e confirme a remoção das DLLs e da configuração instaladas pelo gerenciador.

Para fixar o aplicativo na barra de tarefas, abra-o, clique com o botão direito no ícone da janela na barra de tarefas e selecione **Fixar na barra de tarefas**. Abrir novamente o aplicativo traz a janela existente para frente, inclusive se estiver minimizada.

> [!TIP]
> **Atualizando de uma versão anterior:** desafixe o item antigo, feche o app, abra a versão atualizada pelo atalho e fixe novamente o ícone da janela. O Windows não atualiza automaticamente os itens já fixados.
>
> Para alterar a pasta instalada, use o instalador em vez de mover os arquivos manualmente.

## 🔧 Gerar o instalador (desenvolvimento)

Use Windows x64, Python 3.12 de 64 bits com Tkinter e Inno Setup 6.7.3.

```powershell
python -m venv .venv-build
.\.venv-build\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv-build\Scripts\python.exe -m unittest discover -s tests -v
.\.venv-build\Scripts\python.exe scripts/build_windows.py v1.2.0
```

Se o compilador não for encontrado, acrescente `--iscc "C:\caminho\ISCC.exe"`.
O build gera `dist/BDO Mode Manager/`, o instalador em `dist/` e seu checksum.
Sem informar a versão, o script usa o arquivo `VERSION` do repositório.
O workflow de release gera esse instalador em Windows ao receber uma tag de versão.
O script `package_release.py` fica disponível apenas para o pacote legado de código-fonte.

Para verificar a abertura e a instância única com dados temporários, feche o app e execute:

```powershell
.\.venv-build\Scripts\python.exe scripts/smoke_windows.py "dist/BDO Mode Manager/BDO Mode Manager.exe"
```

Esse teste abre e fecha o gerenciador sem aplicar perfis ou alterar o jogo.

O build atual não assina os arquivos. Antes de uma publicação assinada, assine
o executável antes de compilar o instalador, configure a assinatura do
desinstalador no Inno Setup e assine o instalador com carimbo de tempo.
Recalcule o checksum após a assinatura final. Valide também as DLLs distribuídas.

Antes de distribuir, valide em uma máquina Windows sem Python: instalação,
abertura, aplicação de perfis, atualização com preservação das configurações,
desinstalação e comportamento com as proteções do Windows ativas.

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

A ação **Remover DXVK** remove o `dxvk.conf` e as DLLs com os mesmos nomes das presentes na pasta `bin64` do programa. Ela não restaura um backup permanente da instalação original e pode remover DLLs de mesmo nome que já existiam antes do uso do gerenciador.

## 📜 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
