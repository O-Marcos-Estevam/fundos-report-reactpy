# 📥 Como Instalar o ngrok (3 Métodos)

## Método 1: Download Direto (Mais Fácil) ⭐

### Passo 1: Baixar
1. Acesse: https://ngrok.com/download
2. Clique em **"Download for Windows"**
3. Baixa um arquivo ZIP

### Passo 2: Extrair
1. Extraia o arquivo `ngrok.exe` do ZIP
2. Coloque em uma pasta fácil, exemplo:
   ```
   C:\ngrok\ngrok.exe
   ```

### Passo 3: Adicionar ao PATH (Opcional mas recomendado)
1. Pesquise "Variáveis de Ambiente" no Windows
2. Clique em "Variáveis de Ambiente"
3. Em "Variáveis do Sistema", selecione "Path"
4. Clique em "Editar" → "Novo"
5. Adicione: `C:\ngrok`
6. Clique OK em tudo

### Passo 4: Testar
Abra um NOVO terminal e digite:
```bash
ngrok version
```

Se funcionar, você verá a versão!

---

## Método 2: Winget (Windows Package Manager)

Se você tem Windows 10/11 atualizado:

```bash
winget install ngrok.ngrok
```

---

## Método 3: Scoop

Se você usa Scoop:

```bash
scoop install ngrok
```

---

## 🚀 Como Usar Depois de Instalado

### Sem adicionar ao PATH:
```bash
C:\ngrok\ngrok.exe http 8000
```

### Com PATH configurado:
```bash
ngrok http 8000
```

---

## 🔐 Configurar Conta (Opcional - Grátis)

Para usar sem limitações:

### 1. Criar conta
- Acesse: https://dashboard.ngrok.com/signup
- Crie conta grátis

### 2. Pegar authtoken
- Após login, vá em: https://dashboard.ngrok.com/get-started/your-authtoken
- Copie o token

### 3. Configurar
```bash
ngrok config add-authtoken SEU_TOKEN_AQUI
```

---

## ✅ Verificação Rápida

Execute este comando para testar:

```bash
ngrok http 8000
```

Deve aparecer:
```
ngrok

Session Status                online
...
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000
```

**Funcionou? Você está pronto!** 🎉

---

## 🆘 Problemas?

### "ngrok não é reconhecido como comando"

**Solução A:** Use caminho completo:
```bash
C:\caminho\para\ngrok.exe http 8000
```

**Solução B:** Adicione ao PATH (veja Método 1, Passo 3)

### "Failed to complete tunnel connection"

**Solução:** Verifique se porta 8000 está acessível:
```bash
curl http://localhost:8000
```

Se não responder, inicie a aplicação primeiro:
```bash
python app/main.py
# ou
docker-compose up -d
```

---

## 💡 Dica: Atalho Rápido

Crie um arquivo `start-ngrok.bat` na pasta do projeto:

```batch
@echo off
C:\ngrok\ngrok.exe http 8000
```

Agora é só dar duplo clique nele! 🖱️
