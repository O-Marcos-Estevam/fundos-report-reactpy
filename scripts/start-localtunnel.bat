@echo off
echo ========================================
echo  LocalTunnel - Acesso Publico (porta 8000)
echo ========================================
echo.
echo Certifique-se que a aplicacao esta rodando em http://localhost:8000
echo.
echo Iniciando LocalTunnel...
echo.
echo IMPORTANTE: Na primeira vez, pode pedir para instalar o localtunnel.
echo Digite 'y' e pressione Enter se perguntar.
echo.

npx localtunnel --port 8000

echo.
echo LocalTunnel encerrado.
pause
