# Guia de Deploy

## Deploy Local

### Pré-requisitos

- Python 3.10+
- MS Access Database Driver (ODBC)
- Windows (para Access)

### Instalação

```bash
# 1. Clone ou baixe o projeto
cd fundos_report_reactpy

# 2. Crie ambiente virtual
python -m venv venv

# 3. Ative o ambiente
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Configure variáveis de ambiente
copy config\.env.example .env
# Edite .env com suas configurações

# 6. Execute a aplicação
python src/app/main.py
```

### Acesso

Abra o navegador em: `http://localhost:8000`

---

## Deploy com Docker

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY config/ config/
COPY data/ data/

# Expor porta
EXPOSE 8000

# Comando de execução
CMD ["python", "src/app/main.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - APP_HOST=0.0.0.0
      - APP_PORT=8000
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

### Comandos

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Deploy em Nuvem

### Railway

**1. Preparação**

Crie arquivo `railway.json` na raiz:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python src/app/main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**2. Deploy**

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar projeto
railway init

# Deploy
railway up

# Ver logs
railway logs
```

**3. Variáveis de Ambiente**

Configure no Railway Dashboard:
- `APP_HOST=0.0.0.0`
- `APP_PORT=8000`
- `DB_PATH=...`

---

### Render

**1. Criar arquivo `render.yaml`**

```yaml
services:
  - type: web
    name: fundos-report
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/app/main.py
    envVars:
      - key: APP_HOST
        value: 0.0.0.0
      - key: APP_PORT
        value: 8000
```

**2. Deploy**

1. Conecte repositório GitHub ao Render
2. Selecione `render.yaml`
3. Configure variáveis de ambiente
4. Deploy automático

---

### Heroku

**1. Criar arquivo `Procfile`**

```
web: python src/app/main.py
```

**2. Criar `runtime.txt`**

```
python-3.10.12
```

**3. Deploy**

```bash
# Login
heroku login

# Criar app
heroku create fundos-report

# Adicionar variáveis
heroku config:set APP_HOST=0.0.0.0
heroku config:set APP_PORT=8000

# Deploy
git push heroku main

# Ver logs
heroku logs --tail
```

---

## Túneis (Exposição Local)

### ngrok

```bash
# Instalar
# Windows: scoop install ngrok
# Mac: brew install ngrok

# Autenticar
ngrok config add-authtoken YOUR_TOKEN

# Expor porta 8000
ngrok http 8000

# Ou usar script
scripts\start-ngrok.bat
```

### localtunnel

```bash
# Instalar
npm install -g localtunnel

# Expor
lt --port 8000 --subdomain fundos-report

# Ou usar script
scripts\start-localtunnel.bat
```

### Visual Studio Dev Tunnels

```bash
# Instalar VS Code Dev Tunnels extension

# Criar túnel
devtunnel create --allow-anonymous

# Expor porta
devtunnel port create 8000

# Ou usar script
scripts\start-devtunnel.bat
```

---

## Configuração de Produção

### Otimizações

**1. Gunicorn (Linux)**

```bash
pip install gunicorn

gunicorn src.app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

**2. Nginx (Reverse Proxy)**

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**3. Variáveis de Ambiente**

```env
APP_DEBUG=False
LOG_LEVEL=WARNING
CACHE_ENABLED=true
PARALLEL_QUERIES=true
```

---

## Monitoramento

### Logs

```python
# Configurar logging em produção
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Check

```python
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
```

### Métricas

- Tempo de execução de relatórios
- Taxa de sucesso/erro
- Uso de memória
- Conexões de banco de dados

---

## Backup

### Dados

```bash
# Backup do histórico
cp data/historico.json data/backup/historico_$(date +%Y%m%d).json

# Backup do banco Access
cp "C:\path\to\Base Fundos_V2.accdb" "C:\path\to\backup\Base_Fundos_$(date +%Y%m%d).accdb"
```

### Automação (Windows Task Scheduler)

```batch
@echo off
set BACKUP_DIR=C:\backup\fundos
set DATE=%date:~-4,4%%date:~-10,2%%date:~-7,2%

xcopy /Y data\historico.json %BACKUP_DIR%\historico_%DATE%.json
```

---

## Solução de Problemas

### Erro: Port Already in Use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux
lsof -i :8000
kill -9 <PID>
```

### Erro: MS Access Driver Not Found

```bash
# Instalar driver ODBC
# Windows: Microsoft Access Database Engine 2016 Redistributable
# https://www.microsoft.com/en-us/download/details.aspx?id=54920
```

### Erro: Module Not Found

```bash
# Verificar módulos instalados
pip list

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

---

## Recursos Adicionais

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
