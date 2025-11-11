@echo off
echo ========================================
echo  Iniciando ngrok para porta 8000
echo ========================================
echo.
echo Certifique-se que a aplicacao esta rodando em http://localhost:8000
echo.
echo Aguarde enquanto o ngrok estabelece a conexao...
echo.

"%LOCALAPPDATA%\Microsoft\WindowsApps\ngrok.exe" http 8000

echo.
echo ngrok encerrado.
pause
