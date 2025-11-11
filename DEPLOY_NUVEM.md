# ☁️ Deploy em Nuvem - Grátis e Permanente

## 🎯 Visão Geral

Escolha uma das plataformas abaixo para fazer deploy **GRATUITO** da sua aplicação ReactPy:

| Plataforma | Facilidade | Grátis? | URL Personalizada | Uptime |
|------------|-----------|---------|-------------------|--------|
| **Railway.app** | ⭐⭐⭐⭐⭐ | ✅ 500h/mês | ✅ Sim | 24/7 |
| **Render.com** | ⭐⭐⭐⭐⭐ | ✅ Sim | ✅ Sim | 24/7 |
| **Fly.io** | ⭐⭐⭐⭐ | ✅ Sim | ✅ Sim | 24/7 |
| **Koyeb** | ⭐⭐⭐⭐ | ✅ Sim | ✅ Sim | 24/7 |

**Recomendação:** Railway.app (mais fácil) ou Render.com (mais estável)

---

# 1️⃣ Railway.app (RECOMENDADO) 🚂

## Por que Railway?
- ✅ Mais fácil de todas
- ✅ Deploy em 2 cliques
- ✅ 500 horas grátis/mês (suficiente para uso contínuo)
- ✅ URL bonita: `seu-app.up.railway.app`
- ✅ GitHub integration automático

## 🚀 Passo a Passo

### 1. Preparar o projeto

Precisamos criar alguns arquivos para o Railway entender o projeto.

**a) Criar arquivo `runtime.txt`:**
```
python-3.11
```

**b) Atualizar `requirements.txt`** (já existe, mas verificar):
```
reactpy>=1.0.0
reactpy[fastapi]>=1.0.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pandas>=2.1.0
plotly>=5.17.0
pyodbc>=5.0.0
openpyxl>=3.1.0
python-multipart>=0.0.6
```

**c) Criar `Procfile`:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**d) Criar arquivo de startup `railway.json`:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app/main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. Subir para GitHub

```bash
# Inicializar git (se ainda não fez)
git init
git add .
git commit -m "Preparar para deploy no Railway"

# Criar repositório no GitHub e fazer push
# (Você pode criar via interface do GitHub)
git remote add origin https://github.com/seu-usuario/fundos-report-reactpy.git
git branch -M main
git push -u origin main
```

### 3. Deploy no Railway

1. **Acesse:** https://railway.app
2. **Clique em:** "Start a New Project"
3. **Login com GitHub**
4. **Selecione:** "Deploy from GitHub repo"
5. **Escolha:** seu repositório `fundos-report-reactpy`
6. **Railway detecta Python automaticamente** ✅
7. **Aguarde o deploy** (~2-3 minutos)
8. **Clique em "Settings"** → **"Generate Domain"**
9. **Pronto!** Sua URL: `https://fundos-report-reactpy.up.railway.app`

### 4. Configurar variáveis de ambiente (se necessário)

No Railway dashboard:
1. Vá em **"Variables"**
2. Adicione variáveis como:
   - `PYTHONUNBUFFERED=1`
   - Outros secrets que seu app precise

---

# 2️⃣ Render.com (Alternativa Excelente) 🎨

## Por que Render?
- ✅ Completamente grátis (sem limite de horas)
- ✅ Muito estável
- ✅ SSL automático
- ✅ Auto-deploy do GitHub

## 🚀 Passo a Passo

### 1. Preparar arquivos

**Criar `render.yaml`:**
```yaml
services:
  - type: web
    name: fundos-report-reactpy
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app/main.py
    envVars:
      - key: PYTHONUNBUFFERED
        value: 1
      - key: PORT
        value: 8000
```

### 2. Ajustar app/main.py

Certifique-se que o servidor usa a porta do ambiente:

```python
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### 3. Deploy no Render

1. **Acesse:** https://render.com
2. **Sign up** com GitHub
3. **New** → **Web Service**
4. **Connect repository:** seu repo do GitHub
5. **Configure:**
   - Name: `fundos-report-reactpy`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app/main.py`
6. **Create Web Service**
7. **URL gerada:** `https://fundos-report-reactpy.onrender.com`

**Nota:** No plano grátis, o Render "dorme" após 15 min sem uso. Acorda automaticamente quando alguém acessa (leva ~30 segundos).

---

# 3️⃣ Fly.io (Para Quem Gosta de Containers) 🪰

## 🚀 Passo a Passo

### 1. Instalar Fly CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### 2. Login e Deploy

```bash
# Login
fly auth login

# Navegar para pasta do projeto
cd "c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy"

# Inicializar (cria fly.toml automaticamente)
fly launch

# Deploy
fly deploy
```

O Fly vai detectar o Dockerfile e fazer deploy automaticamente!

**URL:** `https://fundos-report-reactpy.fly.dev`

---

# 4️⃣ Koyeb (Simples e Rápido) 🚀

## 🚀 Passo a Passo

1. **Acesse:** https://koyeb.com
2. **Sign up** com GitHub
3. **Create App** → **GitHub**
4. **Selecione** seu repositório
5. **Configure:**
   - Builder: Dockerfile
   - Port: 8000
6. **Deploy**

**URL:** `https://fundos-report-reactpy.koyeb.app`

---

# 📝 Arquivos Necessários (Resumo)

Aqui está o que você precisa criar/verificar antes do deploy:

## ✅ Checklist de Arquivos

- [x] `requirements.txt` - Dependências Python
- [ ] `runtime.txt` - Versão do Python (Railway)
- [ ] `Procfile` - Comando de start (Railway/Render)
- [ ] `railway.json` - Config Railway (opcional)
- [ ] `render.yaml` - Config Render (opcional)
- [x] `Dockerfile` - Para Fly.io/Koyeb
- [x] `docker-compose.yml` - Local testing

---

# 🎯 Minha Recomendação Final

### Para você, sugiro: **Railway.app**

**Motivos:**
1. ✅ Mais fácil de configurar
2. ✅ 500h grátis/mês (sobra muito)
3. ✅ Deploy automático do GitHub
4. ✅ URL bonita
5. ✅ Logs em tempo real
6. ✅ Perfeito para dashboards internos

---

# 🚀 Próximos Passos

1. Criar conta no Railway: https://railway.app
2. Fazer fork/push do código para GitHub
3. Conectar Railway ao GitHub
4. Deploy automático!
5. Compartilhar URL: `https://seu-app.up.railway.app`

---

# ⚠️ Limitações do MS Access em Nuvem

**IMPORTANTE:** Seu app usa MS Access (`.mdb`), que é **Windows-only**.

## Soluções:

### Opção A: Converter para SQLite (Recomendado)
- SQLite funciona em Linux (onde rodam os servidores)
- Migrar dados do Access para SQLite
- Código Python quase idêntico

### Opção B: Upload do arquivo .mdb
- Fazer upload do arquivo de dados junto com o código
- Usar biblioteca que lê Access em Linux (limitado)

### Opção C: Deploy Windows (Render Windows)
- Render oferece containers Windows (pago)
- Railway não suporta Windows

### Opção D: Manter .mdb local, API expõe dados
- Access roda local no seu PC
- Aplicação em nuvem consome API dos dados
- Mais complexo, mas funcional

---

# 💡 Recomendação para seu Caso

Dado que você usa Access:

1. **Curto prazo:** Use VS Code DevTunnel (já funcionando)
2. **Médio prazo:** Migre Access → SQLite e faça deploy Railway
3. **Longo prazo:** Considere PostgreSQL (mais robusto)

Quer que eu crie um script para migrar Access → SQLite? 🔄
