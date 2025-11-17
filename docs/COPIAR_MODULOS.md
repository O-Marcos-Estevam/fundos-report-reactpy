# 📁 Copiar Módulos V4/V5/V6

## 🎯 Objetivo

Copiar os módulos de relatório originais para o projeto ReactPy.

---

## 📋 Passo a Passo (2 minutos)

### 1️⃣ Abrir o Windows Explorer

Pressione `Win + E`

### 2️⃣ Ir para a pasta de ORIGEM

Cole este caminho na barra de endereços:
```
c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\0. Python
```

### 3️⃣ Selecionar os arquivos

Selecione estes 3 arquivos (Ctrl + Clique):
- ✅ `Relatório_Fundos_V4.py`
- ✅ `Relatório_Fundos_V5_Enhanced.py`
- ✅ `Relatório_Fundos_V6_Optimized.py`

### 4️⃣ Copiar

Pressione `Ctrl + C`

### 5️⃣ Ir para a pasta de DESTINO

Cole este caminho na barra de endereços:
```
c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy\modules
```

**Nota:** A pasta `modules` já foi criada.

### 6️⃣ Colar

Pressione `Ctrl + V`

### 7️⃣ Fazer Commit e Push

Abra o PowerShell na pasta do projeto e execute:

```powershell
cd "c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy"

git add modules/

git commit -m "Add V4/V5/V6 report modules"

git push
```

---

## ✅ Verificar

Após fazer push, o Railway vai fazer redeploy automaticamente e os módulos estarão disponíveis!

---

## ⚠️ Atenção

Os módulos usam MS Access (`.mdb`), que **não funciona em Linux**.

Mesmo copiando os módulos, a execução de relatórios **não vai funcionar no Railway** porque:
- ❌ Access só funciona no Windows
- ❌ Arquivos `.mdb` não existem no servidor

**Solução:** A execução funcionará apenas **localmente no Windows**.

No Railway, as outras páginas (Dashboard, Lâmina, Histórico) funcionarão perfeitamente com dados mock! ✅

---

**Tempo estimado:** 2 minutos ⏱️
