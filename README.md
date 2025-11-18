# 📊 Relatório Diário de Fundos - ReactPy

Sistema modular de geração e análise de relatórios de fundos de investimento, construído com **ReactPy** e **FastAPI**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)](https://fastapi.tiangolo.com/)
[![ReactPy](https://img.shields.io/badge/ReactPy-1.0%2B-purple)](https://reactpy.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🎯 Sobre o Projeto

Sistema profissional de geração e visualização de relatórios de fundos de investimento com arquitetura modular, escalável e otimizada.

### ✨ Principais Características

- ✅ **UI/UX Moderna** 🎨 - Design system profissional com gradientes, animações e dark mode
- ✅ **Arquitetura Modular** - Código organizado em camadas (models, services, components, pages)
- ✅ **30+ Componentes Reutilizáveis** - Biblioteca completa de UI components modernos
- ✅ **Type Hints Completos** - Código totalmente tipado para melhor manutenção
- ✅ **Gerenciamento de Estado** - StateManager centralizado e thread-safe
- ✅ **3 Versões de Relatório** - Suporte a V4, V5 e V6 Optimized (70% mais rápido)
- ✅ **Testes Automatizados** - Suite completa de testes unitários e integração
- ✅ **Performance Otimizada** - Cache inteligente e queries paralelas
- ✅ **Gráficos Interativos** - Visualizações com Plotly
- ✅ **Responsivo** - Mobile-first design
- ✅ **Deploy Flexível** - Suporte para Docker, Railway, Render, Heroku

## 🆕 Novidades v7.2 - Suporte SQLite

**Deploy em Cloud simplificado!** Agora o sistema suporta SQLite além de Microsoft Access:

- ✅ **Multiplataforma** - Funciona em Windows, Linux e Mac
- ✅ **Railway/Render/Heroku** - Deploy direto sem configuração especial
- ✅ **Zero Dependências** - SQLite é built-in no Python
- ✅ **Migração Automática** - Script de conversão Access → SQLite incluído
- ✅ **Performance** - 20-30% mais rápido que Access
- ✅ **Detecção Automática** - Sistema detecta tipo de banco pela extensão

**Migrar de Access para SQLite:**
```bash
python scripts/convert_access_to_sqlite.py
```

Veja [docs/SQLITE_MIGRATION.md](docs/SQLITE_MIGRATION.md) para detalhes completos.

## 📁 Estrutura do Projeto

```
fundos_report_reactpy/
├── src/                          # Código fonte principal
│   ├── app/                      # Aplicação e configurações
│   │   ├── main.py              # FastAPI + ReactPy (refatorado ✨)
│   │   ├── config.py            # Configurações centralizadas
│   │   └── init_data.py         # Inicialização de dados (novo ✨)
│   ├── models/                   # Modelos de dados
│   │   ├── fundo.py             # FundoData
│   │   ├── execucao.py          # ExecucaoInfo
│   │   └── historico.py         # HistoricoEntry
│   ├── services/                 # Lógica de negócio
│   │   ├── state_manager.py     # StateManager Singleton
│   │   ├── report_executor.py   # Executor de relatórios
│   │   ├── historico_service.py # Persistência de histórico
│   │   ├── cache_manager.py     # Gerenciamento de cache
│   │   └── preferences_manager.py # Preferências do usuário
│   ├── components/               # 30+ componentes UI reutilizáveis
│   │   ├── layout_v2.py         # Layout moderno V2 ⭐
│   │   ├── cards_modern.py      # Cards com gradiente
│   │   ├── charts.py            # 5 tipos de gráficos (Plotly)
│   │   ├── forms.py             # 6 componentes de formulário
│   │   └── tables.py            # 4 tipos de tabelas
│   ├── pages/                    # Páginas da aplicação
│   │   ├── executar_modern.py   # Execução (moderna) ⭐
│   │   ├── dashboard_ultra.py   # Dashboard Ultra ⭐
│   │   ├── dashboard_customizavel.py # Dashboard customizável
│   │   ├── lamina_fundos_modern.py  # Detalhes de fundos
│   │   └── historico_modern.py  # Histórico modernizado
│   ├── modules/                  # Módulos de relatório
│   │   ├── v4/                   # Versão 4 (legado)
│   │   ├── v5/                   # Versão 5 Enhanced
│   │   └── v6/                   # Versão 6 Optimized ⭐
│   └── utils/                    # Utilitários
│       ├── server_utils.py      # Utilitários do servidor
│       ├── performance.py       # Monitoramento de performance
│       └── analytics.py         # Analytics
├── config/                       # Configurações
│   └── config_v6.json           # Configuração V6
├── tests/                        # Testes automatizados
│   ├── unit/                    # Testes unitários
│   └── integration/             # Testes de integração
├── docs/                         # Documentação completa ✨
│   ├── ARCHITECTURE.md          # Arquitetura detalhada
│   ├── DEPLOYMENT.md            # Guia de deploy
│   ├── DEVELOPMENT.md           # Guia de desenvolvimento
│   ├── MELHORIAS.md             # Melhorias implementadas ✨
│   └── UI_DESIGN_SYSTEM.md      # Design System
├── scripts/                      # Scripts utilitários ✨
│   ├── debug_app.py             # Debug da aplicação
│   ├── populate_sample_data.py  # Popular dados de teste
│   └── fix_modern_grid.py       # Correções de layout
├── static/                       # Assets estáticos (CSS consolidado ✨)
│   └── css/
│       ├── design-system.css    # Design tokens
│       ├── components.css       # Componentes
│       └── dashboard-ultra.css  # Dashboard ultra
├── data/                         # Dados persistidos
│   ├── historico.json           # Histórico de execuções
│   └── user_preferences.json    # Preferências do usuário
├── requirements.txt              # Dependências
├── .gitignore                    # Git ignore (completo ✨)
└── README.md                     # Este arquivo
```

## 🚀 Instalação Rápida

### Pré-requisitos

- Python 3.10 ou superior
- MS Access Database Engine (Windows)
- Git

### Passos

```bash
# 1. Clone ou navegue até o diretório
cd fundos_report_reactpy

# 2. Crie ambiente virtual
python -m venv venv

# 3. Ative o ambiente
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Configure variáveis de ambiente
copy config\.env.example .env
# Edite .env conforme necessário

# 6. Execute a aplicação
python src/app/main.py
```

Acesse: **http://localhost:8000**

## 💻 Uso

### Páginas Disponíveis

1. **📝 Executar** - Selecione data e versão para gerar relatórios
2. **📊 Dashboard** - Visualize métricas agregadas e gráficos interativos
3. **📄 Lâmina de Fundos** - Detalhes completos de cada fundo
4. **📚 Histórico** - Consulte execuções anteriores
5. **⚙️ Configurações** - Ajuste preferências da aplicação

### Versões de Relatório

| Versão | Performance | Recursos | Recomendação |
|--------|------------|----------|--------------|
| **V6 Optimized** ⭐ | 7-15s | Cache, Queries Paralelas, Analytics | **Produção** |
| **V5 Enhanced** | 40-65s | 3 Abas, Formatação Avançada | Legado |
| **V4 Legacy** | 40-65s | 1 Aba, Básico | Compatibilidade |

## 🐳 Docker

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🧪 Testes

```bash
# Instalar dependências de dev
pip install -r requirements-dev.txt

# Executar todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Apenas testes unitários
pytest tests/unit/

# Apenas testes de integração
pytest tests/integration/ -m integration
```

## 🔧 Desenvolvimento

```bash
# Linting e formatação
ruff check --fix src/
ruff format src/

# Type checking
mypy src/

# Organizar imports
isort src/
```

Consulte [DEVELOPMENT.md](docs/DEVELOPMENT.md) para detalhes completos.

## 📚 Documentação

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Arquitetura detalhada do sistema
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Guias de deploy (Local, Docker, Cloud)
- [DEVELOPMENT.md](docs/DEVELOPMENT.md) - Guia de desenvolvimento e contribuição
- [UI_DESIGN_SYSTEM.md](docs/UI_DESIGN_SYSTEM.md) - 🎨 **Design System completo** (NOVO!)
- [UI_IMPROVEMENTS.md](UI_IMPROVEMENTS.md) - Resumo das melhorias de UI

## 🎨 Design System

O projeto agora conta com um **Design System profissional** completo:

### Componentes Modernos
- 🎯 **15+ Componentes CSS** - Buttons, cards, inputs, tables, badges, alerts
- 🚀 **10+ Componentes React** - Layout moderno, cards com gradiente, glassmorphism
- 🌈 **50+ Design Tokens** - Cores, tipografia, espaçamento, sombras
- ✨ **Animações Suaves** - Fade in, slide up/down, hover effects
- 🌙 **Dark Mode** - Tema escuro completo
- 📱 **Responsivo** - Mobile-first design

### Exemplos

```python
from components.layout_modern import modern_header, modern_navigation
from components.cards_modern import metric_card_modern

# Header moderno com gradiente
modern_header(titulo="Dashboard", subtitulo="v7.1")

# Card de métrica com animações
metric_card_modern(
    titulo="Patrimônio Total",
    valor="R$ 15.3B",
    variacao=5.2,
    icone="💰",
    cor="success"
)
```

Consulte [UI_DESIGN_SYSTEM.md](docs/UI_DESIGN_SYSTEM.md) para guia completo.

## 🌐 Deploy em Nuvem

### Railway

```bash
railway init
railway up
```

### Render

Conecte repositório GitHub e configure `render.yaml`.

### Heroku

```bash
heroku create fundos-report
git push heroku main
```

Consulte [DEPLOYMENT.md](docs/DEPLOYMENT.md) para instruções completas.

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.10+**
- **FastAPI** - Framework web assíncrono
- **ReactPy** - Componentes reativos em Python
- **pyodbc** - Conexão com MS Access

### Frontend
- **ReactPy** - UI declarativa
- **Plotly** - Gráficos interativos
- **HTML/CSS** - Estilização

### Dados
- **MS Access** - Banco de dados
- **pandas** - Processamento de dados
- **numpy** - Cálculos numéricos
- **openpyxl** - Geração de Excel

### Dev Tools
- **pytest** - Framework de testes
- **ruff** - Linter e formatter
- **mypy** - Type checking
- **black** - Code formatter

## 📊 Performance

| Métrica | V4/V5 | V6 Optimized |
|---------|-------|--------------|
| **Tempo de execução** | 40-65s | **7-15s** (70% mais rápido) |
| **Queries SQL** | Sequenciais | **Paralelas** |
| **Cache** | Não | **Sim** (TTL 300s) |
| **Pool conexões** | Não | **Sim** (3 conexões) |
| **Analytics** | Não | **Sim** (Health Score + Alertas) |

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: adicionar nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

Consulte [DEVELOPMENT.md](docs/DEVELOPMENT.md) para convenções de código.

## 📝 Changelog

### Versão 7.2.1 (Atual) 🚀
- ✅ **Modo DEMO funcional** - Execução de relatórios no Railway sem Access
- ✅ **Simulação realista** - Feedback visual com progresso e logs
- ✅ **Detecção inteligente** - Sistema auto-detecta ambiente (cloud vs local)
- ✅ **Validação adaptativa** - Valida ambiente apenas quando necessário
- ✅ **Documentação Railway** - Guia completo do modo DEMO ([docs/RAILWAY_DEMO_MODE.md](docs/RAILWAY_DEMO_MODE.md))

### Versão 7.2 🚀
- ✅ **Suporte SQLite** - Deploy em Linux/Cloud sem Access
- ✅ **Script de migração** - Conversão automática Access → SQLite
- ✅ **Database adapters** - Arquitetura flexível para múltiplos bancos
- ✅ **Banner de modo** - Indicador visual DEMO/PRODUCTION
- ✅ **Mock data aprimorado** - 5 fundos com dados realistas
- ✅ **Detecção automática** - Sistema detecta tipo de banco pela extensão
- ✅ **Documentação completa** - Guia de migração SQLite

### Versão 7.1 ✨
- ✅ **Código refatorado** - Sistema de roteamento otimizado
- ✅ **Logging estruturado** - Logs profissionais com níveis de severidade
- ✅ **Validação de entrada** - Segurança aprimorada
- ✅ **Error handling** - Tratamento robusto de erros
- ✅ **Módulo init_data.py** - Inicialização de dados separada
- ✅ **Configuração via ambiente** - `LOAD_SAMPLE_DATA` variável
- ✅ **Estrutura organizada** - Pastas docs/, scripts/ consolidadas
- ✅ **.gitignore completo** - Ignorar arquivos desnecessários

### Versão 7.0
- ✅ Arquitetura modular completa
- ✅ 30+ componentes reutilizáveis
- ✅ Estrutura de testes
- ✅ Documentação consolidada
- ✅ Configurações separadas
- ✅ Suporte a linting/formatting

### Versão 6.0
- ✨ Módulo V6 Optimized (70% mais rápido)
- ✨ Cache inteligente
- ✨ Queries paralelas
- ✨ Analytics engine

### Versão 5.0
- ✨ Formatação avançada Excel
- ✨ 3 abas de relatório
- ✨ Gráficos integrados

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

**Equipe de Desenvolvimento** - Relatório Diário de Fundos

## 🔗 Links Úteis

- [ReactPy Documentation](https://reactpy.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Plotly Documentation](https://plotly.com/python/)
- [pytest Documentation](https://docs.pytest.org/)

## 💡 Suporte

Para dúvidas ou problemas, abra uma issue no GitHub ou consulte a documentação em [docs/](docs/).

---

**Desenvolvido com ❤️ usando ReactPy e FastAPI**
