# Arquitetura do Sistema

## Visão Geral

O **Relatório Diário de Fundos** é um sistema modular construído com **ReactPy** e **FastAPI** para geração e visualização de relatórios de fundos de investimento.

## Estrutura de Diretórios

```
fundos_report_reactpy/
├── src/                          # Código fonte principal
│   ├── app/                      # Aplicação e configurações
│   │   ├── main.py              # Aplicação FastAPI + ReactPy
│   │   └── config.py            # Configurações centralizadas
│   │
│   ├── models/                   # Modelos de dados
│   │   ├── fundo.py             # FundoData
│   │   ├── execucao.py          # ExecucaoInfo
│   │   └── historico.py         # HistoricoEntry
│   │
│   ├── services/                 # Lógica de negócio
│   │   ├── state_manager.py     # Gerenciamento de estado (Singleton)
│   │   ├── report_executor.py   # Executor de relatórios V4/V5/V6
│   │   └── historico_service.py # Persistência de histórico
│   │
│   ├── components/               # Componentes UI reutilizáveis
│   │   ├── layout.py            # Header, navegação, containers
│   │   ├── cards.py             # 5 tipos de cards
│   │   ├── charts.py            # 5 tipos de gráficos (Plotly)
│   │   ├── forms.py             # 6 componentes de formulário
│   │   └── tables.py            # 4 tipos de tabelas
│   │
│   ├── pages/                    # Páginas da aplicação
│   │   ├── executar.py          # Execução de relatórios
│   │   ├── dashboard.py         # Dashboard com métricas
│   │   ├── lamina_fundos.py     # Detalhes de fundos
│   │   └── historico.py         # Histórico de execuções
│   │
│   └── modules/                  # Módulos de relatório
│       ├── v4/                   # Versão 4 (Legacy)
│       ├── v5/                   # Versão 5 (Enhanced)
│       └── v6/                   # Versão 6 (Optimized) ⭐ Recomendado
│
├── config/                       # Configurações
│   ├── config_v6.json           # Configuração V6
│   └── .env.example             # Variáveis de ambiente
│
├── tests/                        # Testes automatizados
│   ├── unit/                    # Testes unitários
│   └── integration/             # Testes de integração
│
├── docs/                         # Documentação
├── scripts/                      # Scripts de automação (.bat)
├── static/                       # Assets estáticos (CSS, imagens)
└── data/                         # Dados persistidos (histórico.json)
```

## Arquitetura em Camadas

### Camada 1: Models (Dados)

**Responsabilidade**: Representação de dados do domínio

- **FundoData**: 12+ atributos, propriedades calculadas, métodos de alerta
- **ExecucaoInfo**: Informações de uma execução de relatório
- **HistoricoEntry**: Entrada no histórico de execuções

### Camada 2: Services (Lógica de Negócio)

**Responsabilidade**: Lógica de negócio e orquestração

- **StateManager**: Singleton thread-safe para gerenciamento centralizado de estado
- **ReportExecutor**: Importação dinâmica e execução de módulos V4/V5/V6
- **HistoricoService**: Persistência em JSON do histórico

### Camada 3: Components (UI Reutilizável)

**Responsabilidade**: Componentes UI reutilizáveis

**24 componentes** organizados em 5 categorias:
- **Layout** (4): header, sidebar, navegação, containers
- **Cards** (5): métrica, status, info, fundo, estatística
- **Charts** (5): pizza, barras, linha, evolução, timeline
- **Forms** (6): data, versão, fundo, botão, texto, checkbox
- **Tables** (4): fundos, histórico, detalhes, simples

### Camada 4: Pages (Aplicação)

**Responsabilidade**: Páginas principais da aplicação

1. **Executar**: Seleção de data/versão e execução de relatórios
2. **Dashboard**: Métricas agregadas, gráficos e tabelas
3. **Lâmina de Fundos**: Detalhes de um fundo específico
4. **Histórico**: Lista de execuções anteriores
5. **Configurações**: Preferências do usuário

## Fluxo de Dados

```
[Usuário] → [FastAPI/ReactPy] → [Pages] → [Components]
                                     ↓
                               [Services]
                                     ↓
                                 [Models]
                                     ↓
                          [MS Access Database]
```

## Módulos de Relatório

### Comparação de Versões

| Aspecto | V4 | V5 Enhanced | V6 Optimized ⭐ |
|---------|----|-----------:|----------------:|
| Performance | 40-65s | 40-65s | **7-15s** (70% mais rápido) |
| Arquitetura | Monolítica | Monolítica | **Modular** (3 arquivos) |
| Abas Excel | 1 | 3 | **4** |
| Análise | Nenhuma | Básica | **Preditiva + Health Score** |
| Queries SQL | Sequenciais | Sequenciais | **Otimizadas + Paralelas** |
| Cache | Não | Não | **Sim** (TTL configurável) |
| Pool conexões | Não | Não | **Sim** (3 conexões) |

### V6 - Arquitetura Modular

```
Relatório_Fundos_V6_Optimized.py  # Classe principal
├── database_manager_v6.py         # DatabaseManager com pool
└── analytics_engine_v6.py         # Motor de análise e alertas
```

**Recursos V6**:
- ✅ Performance 70% superior
- ✅ Queries SQL otimizadas com JOINs
- ✅ Pool de 3 conexões simultâneas
- ✅ Cache inteligente (TTL configurável)
- ✅ Queries paralelas para MAPS e QORE
- ✅ Motor de análise com 6 regras de alerta
- ✅ Health Score (0-100) por fundo
- ✅ Detecção de anomalias (z-scores)

## Tecnologias Utilizadas

### Backend
- **Python 3.10+**
- **FastAPI**: Framework web assíncrono
- **ReactPy**: Componentes reativos em Python
- **pyodbc**: Conexão com MS Access

### Frontend
- **ReactPy**: Componentes reativos
- **Plotly**: Gráficos interativos
- **HTML/CSS**: Estilos inline

### Dados
- **MS Access**: Banco de dados principal
- **pandas**: Processamento de dados
- **numpy**: Cálculos numéricos
- **openpyxl**: Geração de Excel

## Padrões de Design

### Singleton Pattern
- **StateManager**: Instância única compartilhada

### Composite Pattern
- **Componentes ReactPy**: Composição de componentes

### Strategy Pattern
- **ReportExecutor**: Seleção dinâmica de versão de módulo (V4/V5/V6)

### Observer Pattern
- **ReactPy hooks**: `use_state` para reatividade

## Configuração

### Variáveis de Ambiente (.env)

```env
APP_HOST=0.0.0.0
APP_PORT=8000
DB_PATH=C:\path\to\Base Fundos_V2.accdb
DEFAULT_MODULE_VERSION=v6
```

### Configuração V6 (config/config_v6.json)

```json
{
  "database": {
    "pool_size": 3,
    "timeout": 30
  },
  "cache": {
    "enabled": true,
    "ttl_seconds": 300
  },
  "performance": {
    "parallel_queries": true,
    "max_workers": 3
  }
}
```

## Segurança

- ✅ Conexão segura com banco de dados
- ✅ Validação de inputs
- ✅ Logs estruturados
- ⚠️ Autenticação: A implementar (futuro)
- ⚠️ Autorização: A implementar (futuro)

## Escalabilidade

### Vertical
- Pool de conexões (3 conexões)
- Cache com TTL
- Queries otimizadas

### Horizontal (Futuro)
- Container Docker
- Deploy em cloud (Railway, Render, Heroku)
- Load balancer (nginx)

## Referências

- [ReactPy Documentation](https://reactpy.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Plotly Documentation](https://plotly.com/python/)
