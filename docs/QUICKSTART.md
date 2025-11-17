# ⚡ Guia Rápido - Acesso Público com Docker + ngrok

## 🎯 Objetivo
Permitir que outras pessoas acessem a aplicação de qualquer lugar via Internet.

---

## 📋 Pré-requisitos

1. **Docker Desktop** instalado
   - Download: https://www.docker.com/products/docker-desktop
   - Certifique-se que está rodando (ícone na bandeja)

2. **ngrok** instalado
   - Download: https://ngrok.com/download
   - Ou via Chocolatey: `choco install ngrok`

---

## 🚀 Passos (5 minutos)

### 1️⃣ Abra o terminal na pasta do projeto

```bash
cd "C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy"
```

### 2️⃣ Inicie com Docker

```bash
docker-compose up -d
```

**Saída esperada:**
```
Creating network "fundos_report_reactpy_default" ...
Creating fundos-report-reactpy ... done
```

### 3️⃣ Verifique se está rodando

```bash
docker ps
```

Deve aparecer: `fundos-report-reactpy`

### 4️⃣ Abra OUTRO terminal e inicie o ngrok

```bash
ngrok http 8000
```

**Você verá algo assim:**

```
ngrok

Session Status                online
Account                       seu-email@example.com
Version                       3.x.x
Region                        United States (us)
Latency                       50ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123xyz.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

### 5️⃣ Copie e compartilhe a URL pública!

📎 **URL para compartilhar:**
```
https://abc123xyz.ngrok.io
```

✅ **Pronto!** Qualquer pessoa pode acessar essa URL de qualquer lugar! 🌍

---

## 🛑 Para Parar Tudo

### Parar ngrok
No terminal do ngrok, pressione `Ctrl+C`

### Parar Docker
```bash
docker-compose down
```

---

## 🔍 Verificar se Funcionou

### Teste local primeiro:
```
http://localhost:8000
```

Se funcionar localmente, a URL do ngrok também vai funcionar!

---

## 🆘 Problemas Comuns

### ❌ "Docker não está rodando"
**Solução:** Abra o Docker Desktop e aguarde iniciar

### ❌ "Porta 8000 em uso"
**Solução:**
```bash
# Ver o que está usando a porta
netstat -ano | findstr :8000

# Parar outros servidores
docker stop $(docker ps -q)
```

### ❌ "ngrok command not found"
**Solução:** Instale o ngrok:
- Download: https://ngrok.com/download
- Extraia e coloque no PATH
- Ou use: `choco install ngrok`

### ❌ "Container failed to start"
**Solução:** Veja os logs:
```bash
docker logs fundos-report-reactpy
```

---

## 🎁 Método Mais Fácil (Windows)

### Use o script automatizado:

```bash
start.bat
```

Escolha opção **[3] Iniciar com Docker + ngrok**

O script faz tudo automaticamente! 🚀

---

## 🔐 Segurança (Opcional)

### Adicionar senha no ngrok:

```bash
ngrok http 8000 --basic-auth="usuario:senha123"
```

Agora só quem souber a senha pode acessar!

---

## 📱 Compartilhando com a Equipe

### Envie essa mensagem:

```
🌐 Acesse o Relatório de Fundos:
https://abc123xyz.ngrok.io

✅ Funciona em qualquer navegador
✅ Não precisa instalar nada
✅ Acesso de qualquer lugar
```

---

## ⏱️ Duração do Acesso

**ngrok grátis:**
- ✅ Funciona perfeitamente
- ⚠️ URL muda toda vez que reinicia
- ⏱️ Sessão expira após 2 horas (pode reconectar)

**ngrok pago ($8/mês):**
- ✅ URL fixa (seu-app.ngrok.io)
- ✅ Sem limite de tempo
- ✅ Mais conexões simultâneas

---

## 🎯 Checklist Final

- [ ] Docker Desktop instalado e rodando
- [ ] Terminal 1: `docker-compose up -d` executado
- [ ] Terminal 2: `ngrok http 8000` executado
- [ ] URL https://xxx.ngrok.io copiada
- [ ] Testei acessar a URL no navegador
- [ ] Compartilhei com a equipe
- [ ] Aplicação funcionando! 🎉

---

## 💡 Dicas Pro

### Manter ngrok rodando em background:

```bash
# Windows (via Task Scheduler)
# Ou use nohup no Linux:
nohup ngrok http 8000 &
```

### Ver estatísticas do ngrok:

Acesse: http://localhost:4040

Mostra todas as requisições em tempo real!

### Logs do Docker em tempo real:

```bash
docker logs -f fundos-report-reactpy
```

---

## 📞 Suporte Rápido

**Tudo funcionando local mas não via ngrok?**
- Reinicie o ngrok
- Verifique se copiou a URL HTTPS (não HTTP)

**Lento para outras pessoas?**
- Normal para ngrok grátis
- Considere upgrade ou deploy em nuvem

**Precisa de acesso permanente?**
- Use Railway.app (grátis)
- Ou Render.com (grátis)
- Veja DEPLOY.md para instruções

---

**Tempo total:** ~5 minutos ⚡
**Dificuldade:** Fácil 😊
**Resultado:** Acesso público mundial! 🌍
