BDO Mode Manager 1.2.0 — instalador Windows x64 para todos os usuários.

- Python e Tkinter incluídos: não é necessário instalar Python.
- Tela de apresentação antes do aceite e pasta padrão em `Arquivos de Programas\BDO Mode Manager`, com escolha de destino. Instalação e desinstalação solicitam permissão de administrador.
- Atalho no menu Iniciar e atalho na área de trabalho marcado por padrão.
- Configurações preservadas nas atualizações, em `%LOCALAPPDATA%\BDOModeManager`.
- Perfis Normal/Batata, ícones e DLLs DXVK incluídos.
- Aviso obrigatório sobre riscos, com aceite explícito e espera de 15 segundos.
- Janela abre antes da busca pelo jogo, com indicador de carregamento e ações bloqueadas durante a procura em segundo plano.
- Caminho salvo válido é reutilizado sem nova busca e sem indicador de carregamento.

**Para instalar, baixe somente BDO-Mode-Manager-v1.2.0-Setup.exe em Assets e execute-o.**
Não é necessário baixar ou instalar Python, DLLs, ferramentas de assinatura ou qualquer outro componente separado. Tudo que o gerenciador precisa já está incluído no instalador.
Os arquivos **Source code (zip)** e **Source code (tar.gz)** gerados pelo GitHub são destinados a desenvolvedores e não são necessários para instalar ou usar o app.

O build atual não possui assinatura digital e pode receber avisos ou bloqueios do Windows.

### Se o Windows bloquear o aplicativo

Baixe somente o instalador desta release oficial. A desativação do Controle de Aplicativo Inteligente reduz a proteção contra aplicativos desconhecidos e afeta o computador inteiro, não apenas este programa. Mantenha o antivírus e a proteção em tempo real ativados.

**Windows 11 — Controle de Aplicativo Inteligente**

1. Abra **Iniciar → Configurações → Privacidade e segurança → Segurança do Windows → Abrir Segurança do Windows**.
2. Entre em **Controle de aplicativos e navegador → Configurações do Controle de Aplicativo Inteligente**.
3. Antes de alterar, leia o aviso mostrado pelo Windows: atualizações recentes permitem reativar esse controle; versões anteriores podem exigir redefinir ou reinstalar o sistema. Se sua tela informar essa restrição, não trate a mudança como temporária.
4. Se você optar por continuar e sua versão permitir a reativação, selecione **Desativado** e execute o instalador e o aplicativo desta release.
5. Ao terminar, volte à mesma tela e reative o controle. Como esta versão não é assinada, o bloqueio pode voltar nas próximas aberturas com a proteção ativa; desativar só durante a instalação não garante a execução posterior.

O Controle de Aplicativo Inteligente não oferece uma exceção por aplicativo. Se você não quiser alterar essa proteção, aguarde uma versão assinada ou use uma máquina de teste. Consulte a [orientação oficial da Microsoft](https://support.microsoft.com/en-us/windows/security/threat-malware-protection/smart-app-control-frequently-asked-questions).

**Windows 10 — aviso do Microsoft Defender SmartScreen**

O Windows 10 não possui Controle de Aplicativo Inteligente. Se aparecer **“O Windows protegeu o computador”**, confira que o arquivo veio desta release e, se decidir executá-lo, clique em **Mais informações → Executar assim mesmo**, quando essa opção estiver disponível. Isso permite essa execução sem desligar globalmente o SmartScreen. Não use esse procedimento para ignorar uma detecção de malware ou uma restrição imposta pela sua organização. Consulte a [documentação de controles de aplicativos da Microsoft](https://support.microsoft.com/en-us/windows/security/windows-security/app-browser-control-in-the-windows-security-app).

No Windows 11, esse mesmo aviso do SmartScreen também pode aparecer separadamente do Controle de Aplicativo Inteligente.

Desinstalar o gerenciador não remove o DXVK do jogo. Use **Remover DXVK** no app antes,
se desejar voltar ao DirectX original. Feche o jogo antes de aplicar ou remover perfis.

O app precisa de acesso de gravação à pasta do jogo. O uso de DLLs de terceiros pode
infringir as regras do Black Desert Online; consulte as políticas oficiais.
