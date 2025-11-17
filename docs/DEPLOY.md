# 🚀 Guia de Deploy - Relatório Diário de Fundos

## 📦 Opção 1: Deploy com Docker

### Pré-requisitos
- Docker Desktop instalado (https://www.docker.com/products/docker-desktop)
- Portas 8000 disponível

### Passos:

#### 1. Build da imagem Docker

```bash
cd "C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy"

docker build -t fundos-report-reactpy .
```

#### 2. Executar o container

**Opção A - Comando direto:**
```bash
docker run -d \
  --name fundos-report \
  -p 8000:8000 \
  -v "${PWD}/data:/app/data" \
  fundos-report-reactpy
```

**Opção B - Com docker-compose (Recomendado):**
```bash
docker-compose up -d
```

#### 3. Verificar logs

```bash
docker logs -f fundos-report
```

#### 4. Parar o container

```bash
docker-compose down
# ou
docker stop fundos-report
```

#### 5. Acessar a aplicação

Abra o navegador em: **http://localhost:8000**

---

## 🌍 Opção 2: Deploy com Docker + ngrok

### Pré-requisitos
- Docker rodando (conforme acima)
- ngrok instalado

### Passos:

#### 1. Inicie a aplicação com Docker

```bash
docker-compose up -d
```

#### 2. Instale o ngrok

**Windows (Chocolatey):**
```bash
choco install ngrok
```

**Ou baixe manualmente:**
- https://ngrok.com/download

#### 3. Execute o ngrok

```bash
ngrok http 8000
```

#### 4. Compartilhe a URL

O ngrok vai exibir algo como:

```
Forwarding  https://abc123xyz.ngrok.io -> http://localhost:8000
```

**Copie e compartilhe essa URL!** Qualquer pessoa pode acessar de qualquer lugar! 🌍

---

## 🔒 Opção 3: ngrok com Autenticação

### 1. Criar conta no ngrok (grátis)

- Acesse: https://dashboard.ngrok.com/signup
- Pegue seu authtoken

### 2. Configurar authtoken

```bash
ngrok config add-authtoken SEU_TOKEN_AQUI
```

### 3. Usar domínio reservado (opcional - plano pago)

```bash
ngrok http 8000 --domain=seu-dominio.ngrok.io
```

### 4. Adicionar senha de acesso

```bash
ngrok http 8000 --basic-auth="usuario:senha123"
```

---

## 🐳 Comandos Úteis do Docker

### Ver containers rodando
```bash
docker ps
```

### Ver logs em tempo real
```bash
docker logs -f fundos-report
```

### Acessar terminal do container
```bash
docker exec -it fundos-report bash
```

### Reiniciar container
```bash
docker restart fundos-report
```

### Remover container e imagem
```bash
docker-compose down
docker rmi fundos-report-reactpy
```

### Ver uso de recursos
```bash
docker stats fundos-report
```

---

## 🌐 Opção 4: Deploy na Nuvem

### Render.com (Grátis)

1. Crie conta em https://render.com
2. Conecte seu repositório GitHub
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app/main.py`
4. Deploy automático!

### Railway.app (Grátis)

1. Crie conta em https://railway.app
2. Clique em "New Project"
3. Selecione "Deploy from GitHub repo"
4. Configure variáveis de ambiente
5. Deploy automático!

### Heroku

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

heroku login
heroku create fundos-report-app
git push heroku main
heroku open
```

---

## 🔧 Troubleshooting

### Porta 8000 em uso

```bash
# Windows - Ver processo na porta 8000
netstat -ano | findstr :8000

# Matar processo (substitua PID)
taskkill /PID <PID> /F
```

### Container não inicia

```bash
# Ver logs detalhados
docker logs fundos-report

# Reconstruir imagem
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### ngrok não conecta

```bash
# Verificar se porta está acessível
curl http://localhost:8000

# Reiniciar ngrok com log verbose
ngrok http 8000 --log=stdout
```

---

## 📊 Monitoramento

### Healthcheck com Docker

O docker-compose já inclui healthcheck. Verifique:

```bash
docker inspect fundos-report | grep Health -A 10
```

### Logs estruturados

```bash
# Últimas 100 linhas
docker logs fundos-report --tail 100

# Desde determinado horário
docker logs fundos-report --since 2024-01-01T10:00:00
```

---

## 🎯 Exemplo Completo: Docker + ngrok

### Terminal 1 - Inicie o Docker
```bash
cd "C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy"
docker-compose up
```

### Terminal 2 - Inicie o ngrok
```bash
ngrok http 8000
```

### Compartilhe a URL ngrok

✅ **Acesso local:** http://localhost:8000
✅ **Acesso público:** https://abc123.ngrok.io

---

## 🔐 Segurança

### Para ambientes de produção:

1. **Adicione autenticação:**
   - Implemente login na aplicação
   - Use ngrok com senha: `--basic-auth`

2. **Configure HTTPS:**
   - ngrok já fornece HTTPS automático
   - Para deploy próprio, use Let's Encrypt

3. **Limite de taxa:**
   - Configure rate limiting no FastAPI
   - Use middleware de segurança

4. **Variáveis de ambiente:**
   - Nunca commite senhas no código
   - Use arquivo `.env` (não versionado)

---

## ✅ Checklist Final

- [ ] Docker instalado e rodando
- [ ] Imagem construída com sucesso
- [ ] Container iniciado sem erros
- [ ] Aplicação acessível em localhost:8000
- [ ] ngrok instalado (se for usar acesso público)
- [ ] URL pública funcionando
- [ ] Compartilhado com outras pessoas
- [ ] Logs sendo monitorados

---

## 🆘 Suporte

Se encontrar problemas:

1. Verifique os logs: `docker logs fundos-report`
2. Teste localmente primeiro: http://localhost:8000
3. Verifique firewall e antivírus
4. Reinicie Docker Desktop
5. Reconstrua a imagem: `docker-compose build --no-cache`

---

**Versão do Guia:** 1.0
**Última atualização:** 2025-01-11
