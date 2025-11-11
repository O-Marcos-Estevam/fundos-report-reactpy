@echo off
REM Script para iniciar Relatório Diário de Fundos - ReactPy
echo ======================================================================
echo   Relatório Diário de Fundos - ReactPy
echo   Versão 7.0
echo ======================================================================
echo.

:menu
echo Escolha uma opção:
echo.
echo [1] Iniciar com Python (localhost)
echo [2] Iniciar com Docker
echo [3] Iniciar com Docker + ngrok (acesso público)
echo [4] Parar Docker
echo [5] Ver logs do Docker
echo [6] Sair
echo.
set /p choice="Digite o número da opção: "

if "%choice%"=="1" goto python
if "%choice%"=="2" goto docker
if "%choice%"=="3" goto docker_ngrok
if "%choice%"=="4" goto docker_stop
if "%choice%"=="5" goto docker_logs
if "%choice%"=="6" goto end

:python
echo.
echo Iniciando com Python...
echo Acesse: http://localhost:8000
echo.
python app/main.py
goto menu

:docker
echo.
echo Iniciando com Docker...
docker-compose up -d
echo.
echo Container iniciado!
echo Acesse: http://localhost:8000
echo.
pause
goto menu

:docker_ngrok
echo.
echo Iniciando com Docker...
docker-compose up -d
echo.
echo Aguarde alguns segundos...
timeout /t 5 /nobreak > nul
echo.
echo Iniciando ngrok...
echo IMPORTANTE: Copie a URL https://xxx.ngrok.io que aparecer
echo.
start cmd /k "ngrok http 8000"
echo.
echo Aplicação disponível publicamente via ngrok!
echo.
pause
goto menu

:docker_stop
echo.
echo Parando Docker...
docker-compose down
echo.
echo Container parado!
echo.
pause
goto menu

:docker_logs
echo.
echo Logs do Docker (pressione Ctrl+C para sair):
echo.
docker logs -f fundos-report
goto menu

:end
echo.
echo Até logo!
echo.
exit
