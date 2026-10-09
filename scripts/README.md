# Desenvolvimento e geração da distribuição

O produto entregue ao usuário é o instalador EXE descrito no [README principal](../README.md). Python e as ferramentas abaixo são requisitos de desenvolvimento; o usuário final recebe o runtime e os recursos no pacote.

## Executar o código-fonte

Use Windows e Python 3 com Tkinter. Mantenha `assets/`, `bin64/` e `game_modes/` ao lado de `BDO_Mode_Manager.pyw`.

```powershell
python BDO_Mode_Manager.pyw
```

O código-fonte usa o mesmo arquivo de configuração por usuário que o aplicativo instalado, em `%LOCALAPPDATA%\BDOModeManager\config.json`, e altera a pasta do jogo ao aplicar ou remover perfis.

## Gerar o EXE e o instalador

O workflow do repositório usa Windows, Python 3.12 de 64 bits e Inno Setup 6.7.3. A versão do PyInstaller está fixada em `requirements-build.txt`.

Na raiz do repositório:

```powershell
python -m venv .venv-build
.\.venv-build\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv-build\Scripts\python.exe -m unittest discover -s tests -v
.\.venv-build\Scripts\python.exe scripts/build_windows.py
```

Sem argumento de versão, o script lê `VERSION`. Para informar uma versão explicitamente:

```powershell
.\.venv-build\Scripts\python.exe scripts/build_windows.py v1.2.0
```

Se o compilador do Inno Setup não for encontrado, acrescente `--iscc "C:\caminho\ISCC.exe"`.

| Saída | Conteúdo |
|---|---|
| `dist/BDO Mode Manager/` | EXE, runtime Python/Tkinter, recursos, perfis e DLLs DXVK. |
| `dist/BDO-Mode-Manager-v<VERSÃO>-Setup.exe` | Instalador para todos os usuários, com atalhos, documentação e aviso de uso. |
| `dist/BDO-Mode-Manager-v<VERSÃO>-Setup.exe.sha256` | Checksum SHA-256 do instalador. |

`BDO_Mode_Manager.spec` gera um pacote com executável e arquivos auxiliares, sem console. As DLLs DXVK são copiadas para o subdiretório `bin64` depois do empacotamento: são destinadas ao jogo, não à raiz do executável. O build verifica os recursos obrigatórios e recusa um pacote com `config.json` pessoal.

`installer/BDO_Mode_Manager.iss` define o destino, os atalhos, os arquivos de documentação e o aceite obrigatório. O README principal é incluído no instalador; após alterá-lo, gere novamente o instalador para que a próxima distribuição contenha o texto atualizado.

## Verificar o pacote

Feche qualquer instância do gerenciador e execute:

```powershell
.\.venv-build\Scripts\python.exe scripts/smoke_windows.py "dist/BDO Mode Manager/BDO Mode Manager.exe"
```

Essa verificação abre e fecha o aplicativo, usa dados temporários e verifica a instância única sem aplicar perfis ou alterar o jogo.

Antes de distribuir, valide também em um Windows sem Python instalado: instalação, abertura, aplicação e remoção dos perfis, atualização com preservação das configurações e desinstalação. Confirme o comportamento com as proteções do Windows ativas.

## Publicação

O workflow `.github/workflows/release.yml` é acionado por uma tag no formato `v*.*.*`, que deve corresponder ao arquivo `VERSION`. Ele executa os testes, gera o instalador, verifica o EXE empacotado e publica o instalador e seu checksum na release.

`scripts/package_release.py`, `launch.vbs` e `setup_shortcuts.vbs` pertencem ao fluxo legado de distribuição do código-fonte. Eles não são necessários para instalar ou executar a distribuição atual em EXE.

O build atual não assina o aplicativo nem o instalador. Uma distribuição assinada exige assinar o EXE antes de compilar o instalador, configurar a assinatura do desinstalador e assinar o instalador final. O checksum deve ser recalculado após a assinatura final.

## Perfis personalizados

Os perfis são subpastas de `game_modes/` contendo um `dxvk.conf`. Para adicionar um perfil, crie essa estrutura e reabra o aplicativo. Para alterar um perfil existente, edite seu arquivo e aplique-o novamente. A pasta instalada em Arquivos de Programas pode exigir permissão de administrador para editar esses arquivos.

A comparação de perfis ignora comentários, linhas vazias, ordem das opções, espaços ao redor das opções, BOM UTF-8 e diferenças LF/CRLF. Os valores `True`/`true`, `False`/`false` e `Auto`/`auto` são equivalentes; diferenças nos demais valores permanecem relevantes. Perfis com as mesmas opções são informados como equivalentes, sem escolher arbitrariamente um perfil ativo.
