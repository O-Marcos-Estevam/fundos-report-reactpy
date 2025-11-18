# 🎭 Modo DEMO no Railway

## Visão Geral

O modo DEMO permite que a aplicação rode perfeitamente no Railway (ou qualquer ambiente cloud Linux) **sem necessidade de banco Access**, executando relatórios com dados de exemplo realistas.

## 🔍 Como Funciona

### Detecção Automática

O sistema detecta automaticamente se está rodando em ambiente cloud e ativa o modo DEMO:

```python
# config.py
IS_CLOUD = is_cloud_environment()  # Detecta Railway, Render, Heroku, etc
USE_MOCK_DATA = os.environ.get("USE_MOCK_DATA", str(IS_CLOUD).lower())
```

### Fluxo de Execução

**Quando usuário clica "Executar Relatório" no Railway:**

1. **executar_modern.py** cria `ReportExecutor(versao_selecionada)`
2. **report_executor.py** verifica se está em modo DEMO:
   ```python
   if AppConfig.USE_MOCK_DATA:
       return self._executar_modo_demo(...)
   ```
3. **_executar_modo_demo()** executa:
   - Simula progresso (10% → 30% → 60% → 90% → 100%)
   - Carrega dados de exemplo do `state_manager`
   - Retorna `ExecucaoInfo` com status sucesso
   - Logs detalhados da execução DEMO

### Dados de Exemplo

Os dados são pré-carregados pelo [init_data.py](../src/app/init_data.py):

- 5 fundos com métricas realistas (Alpha, Beta, Gamma, Delta, Epsilon)
- Patrimônio Líquido: R$ 5B - R$ 22B
- Rentabilidades: 0.29% - 0.65% ao dia
- Sharpe: 1.62 - 2.15
- Volatilidade: 3.5% - 12.1%

## 🚀 Deploy no Railway

### Configuração (railway.json)

```json
{
  "deploy": {
    "startCommand": "python src/app/main.py",
    "env": {
      "USE_MOCK_DATA": "true",
      "LOAD_SAMPLE_DATA": "true",
      "PYTHONUNBUFFERED": "1"
    }
  }
}
```

### Variáveis de Ambiente

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `USE_MOCK_DATA` | `true` | Ativa modo DEMO |
| `LOAD_SAMPLE_DATA` | `true` | Carrega dados de exemplo na inicialização |
| `PYTHONUNBUFFERED` | `1` | Logs em tempo real |

### Deploy

```bash
# Fazer deploy (após git push)
# Railway detecta automaticamente e faz deploy
```

## 🎨 Indicadores Visuais

### Banner de Modo DEMO

O sistema exibe um banner roxo no topo da aplicação:

```
🎭 MODO DEMONSTRAÇÃO - Dados de exemplo • Para executar com dados reais, configure o banco Access localmente
```

**Cores:**
- **Purple gradient** = Modo DEMO (Railway/Cloud)
- **Green gradient** = Modo PRODUÇÃO (Windows com Access)

### Mensagens de Execução

Durante a execução, o usuário vê:

```
🎭 Modo Demonstração - Carregando dados de exemplo...
INFO: Executando em modo DEMO
INFO: Data do relatório: 15/11/2024
INFO: Versão: V6
INFO: 5 fundos carregados
SUCCESS: Execução concluída com sucesso
SUCCESS: Tempo total: 1.2s
```

### Resultado Final

```
✅ Relatório gerado com sucesso!

🎭 MODO DEMONSTRAÇÃO - Relatório gerado com dados de exemplo

Fundos Processados: 5
Tempo de Execução: 1.2s
```

## 🧪 Testando Modo DEMO Localmente

Para testar o modo DEMO no ambiente local (Windows):

```bash
# 1. Ativar modo DEMO via variável de ambiente
set USE_MOCK_DATA=true

# 2. Executar aplicação
python src/app/main.py

# 3. Acessar http://localhost:8000
# Você verá o banner roxo de DEMO

# 4. Clicar em "Executar" e testar execução de relatório
# Deve completar em ~1-2 segundos com dados de exemplo
```

## 🔄 Diferenças: DEMO vs PRODUÇÃO

| Aspecto | Modo DEMO | Modo PRODUÇÃO |
|---------|-----------|---------------|
| **Ambiente** | Railway, Render, Heroku, Cloud | Windows local com Access |
| **Dados** | 5 fundos de exemplo | Dados reais do Access |
| **Execução** | ~1-2 segundos | ~7-15 segundos (V6) |
| **Módulos** | Não importa V4/V5/V6 | Importa módulos reais |
| **Banner** | 🎭 Roxo (DEMO) | ✅ Verde (PRODUÇÃO) |
| **Relatório Excel** | ❌ Não gera arquivo | ✅ Gera .xlsx |
| **Database** | ❌ Não conecta | ✅ Conecta Access/SQLite |

## 🐛 Troubleshooting

### Erro: "Não foi possível importar módulo V6"

**Causa:** Sistema tentando executar em modo produção sem Access

**Solução:**
```bash
# Verificar variável de ambiente
echo $USE_MOCK_DATA  # Deve ser "true"

# Se não estiver definida, adicionar ao railway.json
```

### Banner não aparece

**Causa:** Variável `USE_MOCK_DATA` não está sendo lida

**Solução:**
```python
# Verificar em config.py
print(f"USE_MOCK_DATA: {AppConfig.USE_MOCK_DATA}")
print(f"IS_CLOUD: {AppConfig.IS_CLOUD}")
```

### Dados de exemplo não aparecem

**Causa:** `LOAD_SAMPLE_DATA` está false ou dados não foram carregados

**Solução:**
```bash
# Verificar logs da aplicação
# Deve aparecer:
# INFO - Dados de exemplo carregados com sucesso
# INFO -   - 5 fundos criados
```

### Execução fica travada

**Causa:** Possível problema no callback de progresso

**Solução:**
- Verificar logs de erro
- Recarregar página
- Verificar se `state_manager` tem dados carregados

## 📊 Logs Esperados

### Inicialização

```
INFO - Tipo de ambiente: CLOUD
INFO - Modo mock data: True
INFO - Dados de exemplo carregados com sucesso
INFO -   - 5 fundos criados
INFO -   - Execução: sucesso
```

### Execução de Relatório

```
INFO - Executando em modo DEMO
INFO - Data do relatório: 15/11/2024
INFO - Versão: V6
INFO - 5 fundos carregados
INFO - Calculando indicadores
INFO - Gerando análises
SUCCESS - Execução concluída com sucesso
SUCCESS - Tempo total: 1.23s
```

## ✅ Validação

Para validar que o modo DEMO está funcionando:

1. **Acessar Railway URL** (ex: `https://fundos-report.up.railway.app`)
2. **Verificar banner roxo** no topo da página
3. **Navegar para "Executar"**
4. **Selecionar data e versão V6**
5. **Clicar "Executar Relatório"**
6. **Aguardar ~1-2 segundos**
7. **Verificar mensagem de sucesso:**
   - ✅ Relatório gerado com sucesso!
   - 🎭 MODO DEMONSTRAÇÃO
   - 5 fundos processados

## 🔗 Arquivos Relacionados

- [src/services/report_executor.py](../src/services/report_executor.py) - Lógica de execução DEMO
- [src/app/config.py](../src/app/config.py) - Detecção de ambiente
- [src/app/init_data.py](../src/app/init_data.py) - Dados de exemplo
- [src/components/layout_v2.py](../src/components/layout_v2.py) - Banner de modo
- [railway.json](../railway.json) - Configuração Railway

## 📝 Notas

- Modo DEMO **não gera arquivo Excel** (apenas exibe dados na tela)
- Execução é **simulada** com delays artificiais para feedback visual
- Dados são **estáticos** (não mudam com data selecionada)
- Ideal para **demonstrações** e **testes de UI**
- Para dados reais, usar **ambiente Windows com Access** ou **migrar para SQLite**

---

**Desenvolvido para Fundos Report ReactPy v7.2+**
