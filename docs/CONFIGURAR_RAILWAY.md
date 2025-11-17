# ⚙️ Configurar Variáveis de Ambiente no Railway

## 🎯 O Que Fazer Agora

O código foi atualizado para funcionar **sem banco de dados Access** usando dados simulados (mock).

Para que funcione no Railway, você precisa configurar uma variável de ambiente.

---

## 📋 Passo a Passo

### 1️⃣ Acesse seu Projeto no Railway

1. Vá em: https://railway.app/dashboard
2. Clique no seu projeto: **fundos-report-reactpy**

### 2️⃣ Adicionar Variável de Ambiente

1. No dashboard do projeto, clique na aba **"Variables"** (ou "Environment Variables")
2. Clique em **"+ New Variable"** ou **"RAW Editor"**
3. Adicione a seguinte variável:

```
USE_MOCK_DATA=true
```

4. Clique em **"Add"** ou **"Deploy"**

### 3️⃣ Aguarde o Redeploy

O Railway vai automaticamente fazer um novo deploy com a variável configurada.

Aguarde ~2 minutos.

---

## 🎯 Variáveis Configuradas

Com isso, seu app terá:

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `USE_MOCK_DATA` | `true` | Usa dados simulados (sem Access) |
| `PYTHONUNBUFFERED` | `1` | Logs em tempo real |
| `PORT` | (automático) | Railway define automaticamente |

---

## ✅ Como Saber se Funcionou?

Após o deploy:

1. Vá em **"Deployments"** → Clique no deployment mais recente
2. Veja os logs
3. Deve aparecer:
   ```
   INFO:     Started server process
   INFO:     Uvicorn running on http://0.0.0.0:XXXX
   ```

4. Sem erros de banco de dados! ✅

---

## 🌐 Gerar URL Pública

Depois que o app estiver rodando:

1. Vá em **"Settings"**
2. Seção **"Networking"** ou **"Domains"**
3. Clique em **"Generate Domain"**
4. Pronto! URL: `https://fundos-report-reactpy.up.railway.app`

---

## 📊 O que Você Verá na Aplicação

Com `USE_MOCK_DATA=true`, a aplicação mostrará:

✅ **Dashboard** - Métricas e gráficos com dados simulados
✅ **Lâmina de Fundos** - Detalhes de fundos fictícios
✅ **Histórico** - Execuções simuladas
✅ **Executar** - Interface funcional (gera relatórios mock)

**Nota:** Como não há banco Access, os dados são fixos e não mudam. Perfeito para demonstração!

---

## 🔄 Para Usar Dados Reais Futuramente

Quando quiser usar dados reais, você tem opções:

### Opção A: Migrar para PostgreSQL
Railway oferece PostgreSQL gratuito. Posso criar script de migração.

### Opção B: SQLite
Mais simples, funciona em Linux. Também posso criar script.

### Opção C: API Local
Access no seu PC, app em nuvem consome via API.

---

## 🆘 Problemas?

### ❌ App ainda não inicia

**Verifique:**
1. Variável `USE_MOCK_DATA=true` está configurada?
2. Logs mostram algum erro específico?

### ❌ "Module not found"

**Solução:**
- Veja se `requirements.txt` tem todas as dependências
- Rebuild do projeto

### ❌ Porta incorreta

**Já resolvido!** O código usa `PORT` do ambiente automaticamente.

---

## ✅ Checklist Final

- [ ] Variável `USE_MOCK_DATA=true` adicionada no Railway
- [ ] Novo deploy iniciado automaticamente
- [ ] Deploy concluído sem erros
- [ ] App rodando (veja logs)
- [ ] Domain gerado
- [ ] URL testada e funcionando! 🎉

---

**Tempo estimado:** 2 minutos ⚡
**Dificuldade:** Muito Fácil 😊
