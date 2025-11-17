@echo off
echo ========================================
echo  VS Code DevTunnel - Acesso Publico
echo ========================================
echo.
echo Certifique-se que a aplicacao esta rodando em http://localhost:8000
echo.
echo Criando tunel publico sem autenticacao...
echo.

REM Criar túnel público
devtunnel create --allow-anonymous

REM Anotar o ID do túnel e usar
echo.
echo Tunel criado! Anote o ID que apareceu acima.
echo.
pause

echo.
echo Agora iniciando o tunel na porta 8000...
echo.

REM Você precisará substituir TUNNEL_ID pelo ID real
devtunnel port create TUNNEL_ID -p 8000

devtunnel host TUNNEL_ID

echo.
echo DevTunnel encerrado.
pause
