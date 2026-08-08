@echo off
setlocal

REM ============================================================
REM  BUILD SCRIPT - BDO Mode Manager
REM  Compila o .exe e copia automaticamente as pastas
REM  necessarias (bin64 e "Modos de jogo") para o diretorio
REM  final, ao lado do executavel.
REM ============================================================

set NOME_APP=BDO Mode Manager
set PYTHON=py -3.12

echo.
echo [1/4] Limpando build anterior...
if exist "%NOME_APP%.spec" del /q "%NOME_APP%.spec"
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [2/4] Compilando com PyInstaller...
%PYTHON% -m PyInstaller --onedir --windowed --name "%NOME_APP%" BDO_Mode_Manager.pyw
if errorlevel 1 (
    echo.
    echo ERRO: A compilacao falhou. Verifique as mensagens acima.
    pause
    exit /b 1
)

echo.
echo [3/4] Copiando pastas necessarias...
xcopy /e /i /y "bin64" "dist\%NOME_APP%\bin64" >nul
xcopy /e /i /y "Modos de jogo" "dist\%NOME_APP%\Modos de jogo" >nul

echo.
echo [4/4] Build concluido!
echo.
echo O programa completo esta em: dist\%NOME_APP%\
echo Distribua essa pasta inteira para os usuarios.
echo.

pause