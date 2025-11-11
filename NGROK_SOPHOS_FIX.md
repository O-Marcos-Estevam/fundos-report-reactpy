# 🛡️ Solução: Sophos bloqueando ngrok

## Problema
O Sophos Endpoint Agent está bloqueando o ngrok por detectá-lo como PUA (Potentially Unwanted Application).

## Solução 1: Adicionar Exceção no Sophos (Recomendado)

### Passo 1: Abrir o Sophos
1. Clique no ícone do Sophos na bandeja do sistema
2. Ou procure "Sophos" no menu Iniciar

### Passo 2: Adicionar Exceção
1. Vá em **Configurações** ou **Settings**
2. Procure por **Exclusões** ou **Exclusions**
3. Adicione o caminho:
   ```
   C:\Users\MarcosEstevamLinsMor\scoop\apps\ngrok\current\ngrok.exe
   ```
4. Salve a configuração

### Passo 3: Testar
Execute no PowerShell:
```powershell
ngrok http 8000
```

---

## Solução 2: Usar Docker (Sem problemas com antivírus)

Como você já tem Docker instalado, essa é a solução mais simples!

### Passo 1: Iniciar a aplicação com Docker
```bash
cd "c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy"
docker-compose up -d
```

### Passo 2: Usar ngrok via Docker
```bash
docker run -it --rm --net=host ngrok/ngrok:latest http 8000 --authtoken=2ykVqNV9NDKbPZUpQc15omibiZo_84GkwS8QotgKJi8EVLDi1
```

**Vantagens:**
- ✅ Não precisa lidar com antivírus
- ✅ Funciona isolado em container
- ✅ Mais seguro

---

## Solução 3: Download Manual em pasta confiável

### Passo 1: Baixar ngrok
1. Acesse: https://ngrok.com/download
2. Baixe o ZIP para Windows
3. Extraia o `ngrok.exe` para:
   ```
   C:\ngrok\ngrok.exe
   ```

### Passo 2: Adicionar exceção no Sophos
Adicione exceção para: `C:\ngrok\ngrok.exe`

### Passo 3: Configurar authtoken
```bash
C:\ngrok\ngrok.exe config add-authtoken 2ykVqNV9NDKbPZUpQc15omibiZo_84GkwS8QotgKJi8EVLDi1
```

### Passo 4: Executar
```bash
C:\ngrok\ngrok.exe http 8000
```

---

## Solução 4: Contatar TI (Empresas)

Se você está em ambiente corporativo:
1. Contate o departamento de TI
2. Solicite liberação do ngrok
3. Explique que é uma ferramenta legítima de tunneling

**Link oficial:** https://ngrok.com
**Empresa:** ngrok Inc.
**Uso:** Túnel seguro para desenvolvimento e testes

---

## Por que o Sophos bloqueia?

O ngrok cria túneis que podem ser usados maliciosamente. Por isso alguns antivírus são cautelosos. Mas é uma ferramenta 100% legítima usada por milhões de desenvolvedores.

**Alternativas ao ngrok (se não conseguir usar):**
- LocalTunnel: `npx localtunnel --port 8000`
- Cloudflare Tunnel: `cloudflared tunnel`
- Serveo: `ssh -R 80:localhost:8000 serveo.net`

---

## Recomendação

**Use a Solução 2 (Docker)** - É a mais fácil e não tem conflito com antivírus!
