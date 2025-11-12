@echo off
chcp 65001 >nul
echo ======================================================================
echo  Copiando Modulos V4/V5/V6
echo ======================================================================
echo.

set ORIGEM=c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\0. Python
set DESTINO=c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy\modules

echo [V4] Copiando arquivos...
copy "%ORIGEM%\Relatório_Fundos_V4.py" "%DESTINO%\v4\" /Y >nul
if %errorlevel%==0 (echo   OK - Relatório_Fundos_V4.py) else (echo   ERRO - Relatório_Fundos_V4.py)

echo.
echo [V5] Copiando arquivos...
copy "%ORIGEM%\Relatório_Fundos_V5_Enhanced.py" "%DESTINO%\v5\" /Y >nul
if %errorlevel%==0 (echo   OK - Relatório_Fundos_V5_Enhanced.py) else (echo   ERRO - Relatório_Fundos_V5_Enhanced.py)

echo.
echo [V6] Copiando arquivos...
copy "%ORIGEM%\Relatório_Fundos_V6_Optimized.py" "%DESTINO%\v6\" /Y >nul
if %errorlevel%==0 (echo   OK - Relatório_Fundos_V6_Optimized.py) else (echo   ERRO - Relatório_Fundos_V6_Optimized.py)

copy "%ORIGEM%\database_manager_v6.py" "%DESTINO%\v6\" /Y >nul
if %errorlevel%==0 (echo   OK - database_manager_v6.py) else (echo   ERRO - database_manager_v6.py)

copy "%ORIGEM%\analytics_engine_v6.py" "%DESTINO%\v6\" /Y >nul
if %errorlevel%==0 (echo   OK - analytics_engine_v6.py) else (echo   ERRO - analytics_engine_v6.py)

echo.
echo ======================================================================
echo  Verificando arquivos copiados
echo ======================================================================
echo.
echo [V4]
dir "%DESTINO%\v4\*.py" /B 2>nul
echo.
echo [V5]
dir "%DESTINO%\v5\*.py" /B 2>nul
echo.
echo [V6]
dir "%DESTINO%\v6\*.py" /B 2>nul

echo.
echo ======================================================================
echo  Copia concluida!
echo ======================================================================
echo.
echo Proximos passos:
echo   1. git add modules/
echo   2. git commit -m "Add real V4/V5/V6 modules"
echo   3. git push
echo.
pause
