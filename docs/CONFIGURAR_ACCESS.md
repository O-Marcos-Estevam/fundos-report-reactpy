# Configurar Execução com Banco Access

Este guia explica como configurar o sistema para executar relatórios consultando o banco Access real.

## Pré-requisitos

- Windows com Microsoft Access Driver instalado
- Arquivo Base Fundos_V2.accdb acessível
- Python 3.10+ com pyodbc instalado

## Passo a Passo

### 1. Configurar arquivo .env

Crie o arquivo `.env` na raiz do projeto:

```env
# Servidor
PORT=8000
HOST=0.0.0.0

# Modo de Operação
USE_MOCK_DATA=false
LOAD_SAMPLE_DATA=false

# Debug
DEBUG=true
PYTHONUNBUFFERED=1
```

### 2. Completar config/config_v6.json

O arquivo `config/config_v6.json` precisa ter:

```json
{
  "database": {
    "connection_string": "Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=<CAMINHO_COMPLETO>;",
    "path": "<CAMINHO_COMPLETO_DO_BANCO>",
    "pool_size": 3,
    "timeout": 30
  },
  "output": {
    "main_path": "<CAMINHO_DO_EXCEL_PRINCIPAL>",
    "reports_dir": "<DIRETORIO_DE_BACKUPS>",
    "logs_dir": "<DIRETORIO_DE_LOGS>",
    "backup_enabled": true,
    "backup_format": "%Y%m%d_%H%M%S"
  },
  "cache": {
    "enabled": true,
    "ttl_seconds": 300,
    "max_size_mb": 100,
    "cache_dir": "logs/cache"
  }
  // ... resto da configuração
}
```

**Exemplo de paths:**

```json
{
  "database": {
    "path": "C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\03. Arquivos Rotina\09. Base_de_Dados\Base Fundos_V2.accdb"
  },
  "output": {
    "main_path": "C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\Report Diário\Fundos - Report Diário.xlsx",
    "reports_dir": "C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\Report Diário\REPORTS",
    "logs_dir": "C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy\logs"
  }
}
```

### 3. Criar diretórios necessários

```bash
mkdir -p logs/cache
```

### 4. Validar configuração

Execute o script de validação:

```python
python -c "
import json
from pathlib import Path

config = json.load(open('config/config_v6.json'))
db_path = Path(config['database']['path'])
print(f'Banco: {db_path.exists() and \"OK\" or \"ERRO\"}')
print(f'Output configurado: {\"output\" in config and \"OK\" or \"ERRO\"}')
"
```

### 5. Executar aplicação

```bash
python src/app/main.py
```

Acesse: http://localhost:8000

## Executando Relatórios

1. Abra a página "Executar"
2. Selecione a data desejada
3. Escolha a versão:
   - **V6** (recomendado): 70% mais rápido, queries otimizadas
   - **V5**: Versão enhanced com 3 abas
   - **V4**: Versão básica legacy
4. Clique em "Executar Relatório"

## Versões Disponíveis

### V6 Optimized (Recomendado)

- **Performance**: 7-15 segundos
- **Recursos**:
  - Pool de 3 conexões
  - Queries paralelas
  - Cache inteligente (TTL 300s)
  - Analytics engine
  - Alertas automáticos

### V5 Enhanced

- **Performance**: 40-65 segundos
- **Recursos**:
  - 3 abas no Excel
  - Formatação avançada
  - Gráficos integrados

### V4 Legacy

- **Performance**: 40-65 segundos
- **Recursos**:
  - 1 aba básica
  - Compatibilidade

## Troubleshooting

### Erro: "No module named pyodbc"

```bash
pip install pyodbc
```

### Erro: "Database not found"

Verifique o caminho em `config_v6.json > database.path`

### Erro: "Timeout"

Aumente o timeout em `config_v6.json > database.timeout`

### Queries lentas

Use V6 ao invés de V4/V5. V6 tem queries otimizadas sem subqueries.

### Cache desatualizado

Delete a pasta `logs/cache/` para forçar atualização.

## Logs

Os logs são salvos em:

- V6: `logs/fundos_v6.log`
- V5: `report_diario_v5.log`
- V4: `report_diario_v4.log`

## Arquivos Gerados

Após execução bem-sucedida:

1. **Excel principal**: `output.main_path`
2. **Backup**: `output.reports_dir/Fundos_Report_<timestamp>.xlsx`
3. **Logs**: `output.logs_dir/`

---

**Data**: 2025-11-17
**Versão**: 7.1
