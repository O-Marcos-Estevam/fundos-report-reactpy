# 🚀 Deploy Rápido - Railway.app (5 minutos)

## ✅ Arquivos Já Criados

Todos os arquivos necessários já foram criados:
- ✅ `runtime.txt` - Versão do Python
- ✅ `Procfile` - Comando de inicialização
- ✅ `railway.json` - Configuração Railway
- ✅ `render.yaml` - Configuração Render (alternativa)
- ✅ `.gitignore` - Arquivos a ignorar
- ✅ `app/config.py` - Atualizado para aceitar PORT do ambiente

---

## 🎯 Passo a Passo (Railway.app)

### 1. Criar Repositório no GitHub

```bash
# No PowerShell, na pasta do projeto:
cd "c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy"

# Inicializar Git (se ainda não fez)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Initial commit - ReactPy Fundos Report"
```

**Agora vá no GitHub:**
1. Acesse: https://github.com/new
2. Nome do repositório: `fundos-report-reactpy`
3. Deixe **Privado** (recomendado para dados internos)
4. **NÃO** marque "Initialize with README" (já temos arquivos)
5. Clique em "Create repository"

**De volta ao PowerShell:**
```bash
# Adicionar o repositório remoto (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/fundos-report-reactpy.git

# Fazer push
git branch -M main
git push -u origin main
```

### 2. Deploy no Railway

1. **Acesse:** https://railway.app
2. **Clique:** "Start a New Project"
3. **Login** com GitHub
4. **Clique:** "Deploy from GitHub repo"
5. **Autorize** Railway a acessar seus repositórios
6. **Selecione:** `fundos-report-reactpy`
7. **Aguarde** ~2-3 minutos (Railway faz build automático)

### 3. Gerar URL Pública

1. No dashboard do Railway, clique no seu projeto
2. Vá em **"Settings"** (aba superior)
3. Clique em **"Generate Domain"**
4. Pronto! URL gerada: `https://fundos-report-reactpy.up.railway.app`

### 4. Teste!

Acesse sua URL e veja a aplicação funcionando! 🎉

---

## ⚠️ IMPORTANTE: Banco de Dados Access

**Problema:** Seu app usa MS Access (`.mdb`), que **NÃO funciona em servidores Linux** (Railway/Render usam Linux).

### Soluções:

#### Opção A: Dados Mock (Para Demo)
A aplicação já tem dados mock que funcionam sem banco. Perfeito para demonstração!

#### Opção B: Migrar para SQLite
SQLite funciona em qualquer lugar. Posso criar um script de migração.

#### Opção C: PostgreSQL (Profissional)
Railway oferece PostgreSQL gratuito. Melhor opção para produção.

#### Opção D: Manter Access Local + API
- Access fica no seu PC Windows
- Aplicação em nuvem consulta via API
- Mais complexo, mas funcional

---

## 📊 Checklist de Deploy

- [ ] Código commitado no Git
- [ ] Repositório criado no GitHub
- [ ] Push feito para GitHub
- [ ] Conta criada no Railway
- [ ] Projeto criado no Railway
- [ ] Deploy iniciado (automático)
- [ ] Domain gerado
- [ ] URL testada
- [ ] Aplicação funcionando! 🎉

---

## 🔄 Updates Futuros

Sempre que fizer mudanças:

```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

Railway faz **deploy automático** a cada push! 🚀

---

## 💰 Custos

**Railway Grátis:**
- ✅ 500 horas/mês
- ✅ 1GB RAM
- ✅ 1GB disco
- ✅ Compartilhado entre projetos

**Para este app:** Sobra muito! 👍

Se precisar de mais, plano pago começa em $5/mês.

---

## 🆘 Problemas Comuns

### ❌ Build falha

**Verifique:**
- `requirements.txt` está correto?
- Todos os imports estão instalados?
- Código tem erros de sintaxe?

### ❌ App não inicia

**Veja logs:**
- No Railway dashboard → aba "Deployments" → "View Logs"

### ❌ Porta errada

**Já resolvido!** `app/config.py` já usa `PORT` do ambiente.

---

## 🎯 Resultado Final

✅ App online 24/7
✅ URL permanente
✅ HTTPS automático
✅ Deploy automático no push
✅ Logs em tempo real
✅ Gratuito (até 500h/mês)

---

## 📞 Precisa de Ajuda?

- **Documentação Railway:** https://docs.railway.app
- **Discord Railway:** https://discord.gg/railway
- **Ou pergunte aqui!** 😊
