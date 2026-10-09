#ifndef AppVersion
  #error AppVersion deve ser informado pelo script de build.
#endif
#ifndef BuildDir
  #define BuildDir "..\dist\BDO Mode Manager"
#endif
#ifndef OutputDir
  #define OutputDir "..\dist"
#endif

[Setup]
AppId={{63B39355-DF23-493A-A42B-C757AA533DC0}
AppName=BDO Mode Manager
AppVersion={#AppVersion}
AppPublisher=Salazas Corp
VersionInfoCompany=Salazas Corp
VersionInfoVersion={#AppVersion}.0
VersionInfoProductVersion={#AppVersion}
DefaultDirName={userdocs}\BDO Mode Manager
UsePreviousAppDir=no
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir={#OutputDir}
OutputBaseFilename=BDO-Mode-Manager-v{#AppVersion}-Setup
SetupIconFile=..\assets\bdo-mode-manager-spirit-outline.ico
WizardImageFile=..\assets\bdo-mode-manager-spirit-outline.png
WizardSmallImageFile=..\assets\bdo-mode-manager-spirit-outline.png
WizardImageBackColor=clWhite
WizardSmallImageBackColor=clWhite
UninstallDisplayIcon={app}\BDO Mode Manager.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"

[Files]
Source: "{#BuildDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "AVISO-DE-USO.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{userprograms}\BDO Mode Manager"; Filename: "{app}\BDO Mode Manager.exe"; WorkingDir: "{app}"; AppUserModelID: "BDOModeManager.App"
Name: "{userdesktop}\BDO Mode Manager"; Filename: "{app}\BDO Mode Manager.exe"; WorkingDir: "{app}"; Tasks: desktopicon; AppUserModelID: "BDOModeManager.App"

[Run]
Filename: "{app}\BDO Mode Manager.exe"; Description: "Abrir BDO Mode Manager"; Flags: nowait postinstall skipifsilent

[Code]
const
  TempoLeituraMs = 15000;

var
  PaginaAviso: TWizardPage;
  Aceite: TNewRadioButton;
  NaoAceite: TNewRadioButton;
  Contagem: TNewStaticText;
  TimerAviso: UINT_PTR;
  InicioLeitura: Int64;


function SetTimer(hWnd: HWND; nIDEvent: UINT_PTR; uElapse: UINT;
  lpTimerFunc: UINT_PTR): UINT_PTR;
  external 'SetTimer@user32.dll stdcall';
function KillTimer(hWnd: HWND; nIDEvent: UINT_PTR): BOOL;
  external 'KillTimer@user32.dll stdcall';
function GetTickCount64: Int64;
  external 'GetTickCount64@kernel32.dll stdcall';

procedure PararTimerAviso;
begin
  if TimerAviso <> 0 then begin
    KillTimer(0, TimerAviso);
    TimerAviso := 0;
  end;
end;

function LeituraConcluida: Boolean;
begin
  Result := (InicioLeitura <> 0) and
    (GetTickCount64 - InicioLeitura >= TempoLeituraMs);
end;

procedure AtualizarAviso;
var
  Decorrido: Int64;
  Segundos: Integer;
begin
  if WizardForm.CurPageID <> PaginaAviso.ID then Exit;
  Decorrido := GetTickCount64 - InicioLeitura;
  if Decorrido < TempoLeituraMs then begin
    Segundos := (TempoLeituraMs - Decorrido + 999) div 1000;
    Contagem.Caption := Format('Leia o aviso. Avançar será liberado em %d segundos.', [Segundos]);
    WizardForm.NextButton.Caption := Format('%d s', [Segundos]);
    WizardForm.NextButton.Enabled := False;
  end else begin
    Contagem.Caption := 'Para continuar, marque o aceite dos riscos e das condições acima.';
    WizardForm.NextButton.Caption := 'Avançar';
    WizardForm.NextButton.Enabled := Aceite.Checked;
    PararTimerAviso;
  end;
end;

procedure TimerAvisoProc(hWnd: HWND; uMsg: UINT; idEvent: UINT_PTR; dwTime: DWORD);
begin
  AtualizarAviso;
end;

procedure AceiteAlterado(Sender: TObject);
begin
  AtualizarAviso;
end;

function InitializeSetup: Boolean;
begin
  // Instalação silenciosa não pode ignorar o aviso nem o aceite explícito.
  Result := not WizardSilent;
  if not Result then
    Log('Instalação cancelada: o aviso de riscos exige leitura e aceite na interface.');
end;

procedure InitializeWizard;
var
  Destaque: TNewStaticText;
  Texto: TNewMemo;
  Conteudo: AnsiString;
  Paragrafos: String;
begin
  // Mantém o ícone quadrado e centralizado, sem esticar na faixa lateral.
  with WizardForm.WizardBitmapImage do begin
    Top := Top + (Height - Width) div 2;
    Height := Width;
  end;
  with WizardForm.WizardBitmapImage2 do begin
    Top := Top + (Height - Width) div 2;
    Height := Width;
  end;
  WizardForm.WelcomeLabel1.Caption := 'Bem-vindo ao BDO Mode Manager';
  WizardForm.WelcomeLabel2.Caption :=
    'Gerencie os perfis Normal e Batata do Black Desert Online com DXVK/Vulkan.' + #13#10#13#10 +
    'Este assistente instalará o aplicativo para o usuário atual. Python e os componentes necessários já estão incluídos.' + #13#10#13#10 +
    'Na próxima tela, leia a licença de uso e o aviso de riscos antes de continuar.' + #13#10#13#10 +
    'Clique em Avançar para começar ou em Cancelar para sair.';
  PaginaAviso := CreateCustomPage(wpWelcome, 'Licença de uso e aviso de riscos',
    'Leia atentamente antes de continuar a instalação.');


  Destaque := TNewStaticText.Create(PaginaAviso);
  Destaque.Parent := PaginaAviso.Surface;
  Destaque.SetBounds(0, 0, PaginaAviso.SurfaceWidth, ScaleY(40));
  Destaque.AutoSize := False;
  Destaque.WordWrap := True;
  Destaque.Font.Style := [fsBold];
  Destaque.Font.Color := clRed;
  Destaque.Caption := 'Antes de aceitar, saiba do risco:';

  Texto := TNewMemo.Create(PaginaAviso);
  Texto.Parent := PaginaAviso.Surface;
  Texto.SetBounds(0, ScaleY(44), PaginaAviso.SurfaceWidth,
    PaginaAviso.SurfaceHeight - ScaleY(134));
  Texto.ReadOnly := True;
  Texto.ScrollBars := ssVertical;
  Texto.WordWrap := True;
  ExtractTemporaryFile('AVISO-DE-USO.txt');
  if not LoadStringFromFile(ExpandConstant('{tmp}\AVISO-DE-USO.txt'), Conteudo) then
    RaiseException('Não foi possível carregar o aviso de riscos.');
  Paragrafos := UTF8Decode(Conteudo);
  // TMemo do Windows exige CRLF para preservar os parágrafos.
  StringChangeEx(Paragrafos, #13#10, #10, True);
  StringChangeEx(Paragrafos, #10, #13#10, True);
  Texto.Text := Paragrafos;

  Contagem := TNewStaticText.Create(PaginaAviso);
  Contagem.Parent := PaginaAviso.Surface;
  Contagem.SetBounds(0, PaginaAviso.SurfaceHeight - ScaleY(84),
    PaginaAviso.SurfaceWidth, ScaleY(26));
  Contagem.AutoSize := False;
  Contagem.WordWrap := True;

  Aceite := TNewRadioButton.Create(PaginaAviso);
  Aceite.Parent := PaginaAviso.Surface;
  Aceite.SetBounds(0, PaginaAviso.SurfaceHeight - ScaleY(54),
    PaginaAviso.SurfaceWidth, ScaleY(26));
  Aceite.Caption := 'Li e aceito os termos da licença MIT e as condições de uso, ciente dos riscos descritos.';
  Aceite.Checked := False;
  Aceite.OnClick := @AceiteAlterado;

  NaoAceite := TNewRadioButton.Create(PaginaAviso);
  NaoAceite.Parent := PaginaAviso.Surface;
  NaoAceite.SetBounds(0, PaginaAviso.SurfaceHeight - ScaleY(26),
    PaginaAviso.SurfaceWidth, ScaleY(26));
  NaoAceite.Caption := 'Não aceito os termos da licença MIT e as condições de uso.';
  NaoAceite.Checked := True;
  NaoAceite.OnClick := @AceiteAlterado;
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  PararTimerAviso;
  // Preserva Instalar e Concluir nas páginas nativas.
  if (CurPageID <> wpReady) and (CurPageID <> wpFinished) then
    WizardForm.NextButton.Caption := 'Avançar';
  if CurPageID = PaginaAviso.ID then begin
    Aceite.Checked := False;
    NaoAceite.Checked := True;
    InicioLeitura := GetTickCount64;
    AtualizarAviso;
    TimerAviso := SetTimer(0, 0, 200, CreateCallback(@TimerAvisoProc));
    if TimerAviso = 0 then
      RaiseException('Não foi possível iniciar a contagem de leitura do aviso.');
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  if (CurPageID = PaginaAviso.ID) or (CurPageID = wpReady) then
    Result := LeituraConcluida and Aceite.Checked;
end;

procedure DeinitializeSetup;
begin
  PararTimerAviso;
end;
