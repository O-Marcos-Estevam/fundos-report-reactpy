# 🌐 Alternativas ao ngrok (Sem Docker)

## 1️⃣ LocalTunnel (RECOMENDADO) ⭐

### Por que usar?
- ✅ Mais fácil de todas
- ✅ Sem instalação prévia
- ✅ Sem conta necessária
- ✅ Funciona via NPX (Node.js)
- ✅ Antivírus não bloqueia

### Como usar:

**Opção A: Script automático**
```bash
.\start-localtunnel.bat
```

**Opção B: Comando direto**
```bash
npx localtunnel --port 8000
```

### O que acontece:
```
your url is: https://funny-cat-12.loca.lt
```

**Primeira vez:** Pode pedir confirmação para instalar. Digite `y`.

**Compartilhar:** Envie a URL `https://xxx.loca.lt` para outras pessoas.

**Nota:** Quando alguém acessar pela primeira vez, o LocalTunnel pode mostrar uma página pedindo para clicar em "Continue". Isso é normal.

---

## 2️⃣ Cloudflare Tunnel

### Por que usar?
- ✅ Cloudflare (empresa confiável)
- ✅ Performance excelente
- ✅ Sem bloqueios de antivírus
- ✅ Sem limite de tempo

### Como usar:

**1. Download:**
- Acesse: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
- Baixe para Windows
- Ou use: `winget install Cloudflare.cloudflared`

**2. Executar:**
```bash
cloudflared tunnel --url http://localhost:8000
```

**3. Resultado:**
```
https://abc-123-def.trycloudflare.com
```

---

## 3️⃣ Serveo (SSH Tunnel)

### Por que usar?
- ✅ Usa SSH (já vem com Git)
- ✅ Zero instalação adicional
- ✅ Muito leve
- ✅ Simples

### Como usar:

**Se você tem Git Bash instalado:**
```bash
ssh -R 80:localhost:8000 serveo.net
```

**Resultado:**
```
Forwarding HTTP traffic from https://abc123.serveo.net
```

**Nota:** Na primeira vez, pode pedir para aceitar a chave SSH. Digite `yes`.

---

## 4️⃣ Expose (Alternativa moderna)

### Como usar:

```bash
npx expose 8000
```

Similar ao LocalTunnel, mas com interface mais moderna.

---

## 5️⃣ Telebit (Open Source)

### Como usar:

**1. Instalar:**
```bash
npm install -g telebit
```

**2. Configurar (primeira vez):**
```bash
telebit init
```

**3. Executar:**
```bash
telebit http 8000
```

---

## 6️⃣ Bore (Rust - Super Rápido)

### Como usar:

**1. Download:**
- Acesse: https://github.com/ekzhang/bore/releases
- Baixe `bore-windows.exe`

**2. Executar:**
```bash
bore local 8000 --to bore.pub
```

---

## 7️⃣ VS Code Port Forwarding (Se usa VS Code)

### Por que usar?
- ✅ Integrado no VS Code
- ✅ Zero configuração extra
- ✅ Funciona automaticamente

### Como usar:

1. Abra o projeto no VS Code
2. Inicie a aplicação (`python app/main.py`)
3. Vá na aba **"PORTS"** (ao lado do Terminal)
4. Clique em **"Forward a Port"**
5. Digite `8000`
6. Clique com botão direito na porta → **"Port Visibility"** → **"Public"**
7. Copie a URL gerada

**URL exemplo:** `https://username-app-8000.githubpreview.dev`

---

## 📊 Comparação Rápida

| Ferramenta | Facilidade | Velocidade | Estabilidade | Grátis? |
|------------|-----------|------------|--------------|---------|
| **LocalTunnel** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ✅ Sim |
| **Cloudflare** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Sim |
| **Serveo** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ Sim |
| **VS Code** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Sim |
| **Bore** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Sim |

---

## 🎯 Recomendação por Caso

### Uso Rápido (5 minutos):
→ **LocalTunnel** (`npx localtunnel --port 8000`)

### Uso Profissional/Longo:
→ **Cloudflare Tunnel**

### Mais Simples Possível:
→ **VS Code Port Forwarding** (se usa VS Code)

### Mais Seguro:
→ **Serveo via SSH**

---

## 🚀 Teste Agora: LocalTunnel

Execute este comando no PowerShell:

```bash
npx localtunnel --port 8000
```

Ou use o script:

```bash
.\start-localtunnel.bat
```

**Tempo total:** ~30 segundos ⚡

---

## ❓ Precisa de Node.js?

**LocalTunnel precisa de Node.js.** Se você não tem:

**Opção 1: Instalar Node.js (recomendado)**
- Download: https://nodejs.org
- Escolha a versão LTS
- Instala em 2 minutos

**Opção 2: Usar Serveo (sem Node.js)**
```bash
ssh -R 80:localhost:8000 serveo.net
```

**Opção 3: Cloudflare (sem Node.js)**
- Download: https://github.com/cloudflare/cloudflared/releases
- Execute: `cloudflared tunnel --url http://localhost:8000`

---

## 💡 Dica: Combinação Perfeita

1. **Desenvolvimento rápido:** LocalTunnel
2. **Demo para cliente:** Cloudflare Tunnel
3. **Teste com equipe:** VS Code Port Forwarding

---

**Todas funcionam SEM Docker e SEM problemas de antivírus!** 🎉
