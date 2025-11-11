# ⚡ Guia Simples: Python + ngrok (Sem Docker)

## 🎯 Objetivo
Deixar outras pessoas acessarem a aplicação **SEM usar Docker**.

---

## 📋 O que você precisa:

1. ✅ Python (já tem)
2. ✅ Dependências instaladas (requirements.txt)
3. ⬇️ **ngrok** - Baixar de: https://ngrok.com/download

---

## 🚀 Passo a Passo (5 minutos)

### 1️⃣ Baixar o ngrok

1. Acesse: **https://ngrok.com/download**
2. Clique em "Download for Windows"
3. Extraia o arquivo `ngrok.exe` para uma pasta fácil:
   ```
   C:\ngrok\ngrok.exe
   ```

### 2️⃣ Abrir DOIS terminais

**Terminal 1: Iniciar a Aplicação**
```bash
cd "C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy"

python app/main.py
```

Deixe rodando! ✅

**Terminal 2: Iniciar o ngrok**
```bash
C:\ngrok\ngrok.exe http 8000
```

(Ajuste o caminho se colocou o ngrok.exe em outro lugar)

### 3️⃣ Copiar a URL pública

No terminal do ngrok, você verá:

```
Forwarding    https://abc123xyz.ngrok.io -> http://localhost:8000
```

**Essa é sua URL pública!** 📎

### 4️⃣ Compartilhar

Envie para outras pessoas:
```
https://abc123xyz.ngrok.io
```

✅ **Pronto!** Qualquer um pode acessar! 🌍

---

## 🛑 Para Parar

**Terminal 1 (Python):** Pressione `Ctrl+C`
**Terminal 2 (ngrok):** Pressione `Ctrl+C`

---

## 📝 Script Automático (Opcional)

Crie um arquivo `start-with-ngrok.bat`:

```batch
@echo off
echo Iniciando aplicacao...
start cmd /k "cd /d C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy && python app/main.py"

timeout /t 5

echo Iniciando ngrok...
start cmd /k "C:\ngrok\ngrok.exe http 8000"

echo.
echo ==============================================
echo  Aplicacao iniciada!
echo
echo  Aguarde 5 segundos e copie a URL do ngrok
echo  (Janela que abriu)
echo ==============================================
pause
```

Agora é só dar duplo clique no `.bat`! 🖱️

---

## ✅ Vantagens deste método:

✅ Não precisa Docker
✅ Mais rápido para começar
✅ Fácil de debugar (vê os logs direto)
✅ Funciona em qualquer Windows

---

## 🆘 Problemas Comuns

### ❌ "python: command not found"
**Solução:** Use caminho completo:
```bash
C:\Users\MarcosEstevamLinsMor\AppData\Local\Programs\Python\Python311\python.exe app/main.py
```

### ❌ "ngrok não funciona"
**Solução:** Use caminho completo:
```bash
C:\caminho\completo\para\ngrok.exe http 8000
```

### ❌ "Porta 8000 em uso"
**Solução:** Mate o processo:
```bash
netstat -ano | findstr :8000
taskkill /PID <numero_do_PID> /F
```

---

## 💡 Dica: Ver Estatísticas

Enquanto ngrok está rodando, acesse:
```
http://localhost:4040
```

Mostra todas as requisições em tempo real! 📊

---

## 🔐 Adicionar Senha (Opcional)

```bash
C:\ngrok\ngrok.exe http 8000 --basic-auth="usuario:senha123"
```

Agora precisa de usuário e senha para acessar!

---

**Tempo total:** 5 minutos ⚡
**Funciona?** SIM! 🎉
**Precisa Docker?** NÃO! ❌
