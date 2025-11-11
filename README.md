# 📊 Relatório Diário de Fundos - ReactPy

Sistema modular de geração e análise de relatórios de fundos de investimento, construído com **ReactPy** e **FastAPI**.

## 🎯 Sobre o Projeto

Esta aplicação é uma **reimplementação completa** do sistema original em Streamlit, agora com arquitetura modular, escalável e profissional usando ReactPy.

### Principais Melhorias

✅ **Arquitetura Modular** - Código organizado em camadas (models, services, components, pages)
✅ **24 Componentes Reutilizáveis** - Biblioteca completa de UI components
✅ **Type Hints Completos** - Código totalmente tipado para melhor manutenção
✅ **Gerenciamento de Estado** - StateManager centralizado e thread-safe
✅ **Serviços Desacoplados** - Lógica de negócio separada da apresentação
✅ **3 Versões de Relatório** - Suporte a V4, V5 e V6 Optimized
✅ **Performance Otimizada** - Execução assíncrona e caching inteligente

## 📁 Estrutura do Projeto

```
fundos_report_reactpy/
├── app/
│   ├── config.py           # Configurações centralizadas
│   └── main.py             # Aplicação FastAPI + ReactPy
├── models/
│   ├── fundo.py            # Modelo de dados de Fundo
│   ├── execucao.py         # Modelo de Execução
│   └── historico.py        # Modelo de Histórico
├── services/
│   ├── state_manager.py    # Gerenciamento de estado
│   ├── report_executor.py  # Executor de relatórios
│   └── historico_service.py # Serviço de histórico
├── components/
│   ├── layout.py           # Header, sidebar, navegação
│   ├── cards.py            # 5 tipos de cards
│   ├── charts.py           # 5 tipos de gráficos
│   ├── forms.py            # 6 componentes de formulário
│   └── tables.py           # 4 tipos de tabelas
├── pages/
│   ├── executar.py         # Página de execução
│   ├── dashboard.py        # Dashboard com métricas
│   ├── lamina_fundos.py    # Detalhes de fundo
│   └── historico.py        # Histórico de execuções
├── data/
│   └── historico.json      # Persistência de histórico
├── requirements.txt
└── README.md
```

## 🚀 Instalação

### 1. Clone ou navegue até o diretório

```bash
cd fundos_report_reactpy
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Opção 1: Python Direto (Desenvolvimento)

```bash
python app/main.py
```

Acesse: **http://localhost:8000**

### Opção 2: Docker (Recomendado para Produção)

```bash
# Build e iniciar
docker-compose up -d

# Ver logs
docker logs -f fundos-report

# Parar
docker-compose down
```

### Opção 3: Script Automatizado (Windows)

```bash
# Execute o script e escolha a opção desejada
start.bat
```

### Opção 4: Docker + ngrok (Acesso Público)

```bash
# Terminal 1: Iniciar Docker
docker-compose up -d

# Terminal 2: Iniciar ngrok
ngrok http 8000

# Compartilhe a URL https://xxx.ngrok.io gerada!
```

**📖 Guia completo de deploy:** Veja [DEPLOY.md](DEPLOY.md)

## 📚 Funcionalidades

### 1. 🚀 Executar Relatório
- Seleção de data (com quick select ontem/hoje)
- Escolha de versão (V4/V5/V6)
- Execução com progress bar em tempo real
- Visualização de logs
- Download de arquivos gerados

### 2. 📊 Dashboard
- 4 cards de métricas principais
- Gráfico de pizza (PL por tipo)
- Gráfico de barras (Top 10 fundos)
- Análise por tipo de fundo
- Tabela completa com alertas
- Estatísticas adicionais

### 3. 📄 Lâmina de Fundos
- Seletor de fundo
- 4 métricas principais
- Gráfico de evolução de PL
- Gráfico de composição patrimonial
- Detalhes completos
- Sistema de alertas automático

### 4. 📜 Histórico
- Estatísticas gerais
- Gráfico temporal de execuções
- Tabela de execuções (últimas 20)
- Botão para limpar histórico

### 5. ⚙️ Configurações
- Toggle modo escuro
- Configurações de sistema
- Informações de ambiente

## 🏗️ Arquitetura

### Camadas da Aplicação

#### 1. Models (Modelos de Dados)
- **FundoData**: Dados de um fundo com métodos de cálculo
- **ExecucaoInfo**: Informações de uma execução
- **HistoricoEntry**: Entrada no histórico

#### 2. Services (Lógica de Negócio)
- **StateManager**: Gerenciamento centralizado de estado (Singleton, thread-safe)
- **ReportExecutor**: Importação e execução de relatórios V4/V5/V6
- **HistoricoService**: Persistência e manipulação de histórico

#### 3. Components (UI Reutilizáveis)
- **Layout**: header, sidebar, navegação, containers
- **Cards**: 5 tipos (métrica, status, info, fundo, estatística)
- **Charts**: 5 tipos (pizza, barras, linha, evolução, timeline)
- **Forms**: 6 tipos (data, versão, fundo, botão, texto, checkbox)
- **Tables**: 4 tipos (fundos, histórico, detalhes, simples)

#### 4. Pages (Páginas da Aplicação)
- Cada página é um componente ReactPy independente
- Usam componentes reutilizáveis da camada anterior
- Comunicam-se via StateManager

## 🔧 Configuração

### Caminhos e Banco de Dados

Edite o arquivo [app/config.py](app/config.py):

```python
CAMINHO_MODULO = r"C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\0. Python"
DB_PATH = r"C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\03. Arquivos Rotina\09. Base_de_Dados\Base Fundos_V2.accdb"
```

### Porta e Host

```python
class AppConfig:
    HOST = "0.0.0.0"
    PORT = 8000
```

## 🎨 Personalização

### Adicionar Nova Página

1. Crie o arquivo em `pages/nova_pagina.py`:

```python
from reactpy import component, html
from components.layout import container_pagina

@component
def pagina_nova():
    return container_pagina(
        html.h2("Minha Nova Página")
    )
```

2. Adicione no `app/main.py`:

```python
from pages.nova_pagina import pagina_nova

# Na função renderizar_pagina():
elif pagina_atual == "nova":
    return pagina_nova()
```

### Criar Novo Componente

```python
from reactpy import component, html

@component
def meu_componente(titulo: str, valor: str):
    return html.div(
        {"style": {"padding": "1rem"}},
        html.h3(titulo),
        html.p(valor)
    )
```

## 📊 Comparação: Streamlit vs ReactPy

| Aspecto | Streamlit Original | ReactPy Novo |
|---------|-------------------|--------------|
| Linhas de código | 2.118 (monolítico) | ~3.000 (modular) |
| Arquivos | 1 arquivo | 20+ arquivos organizados |
| Componentes | Acoplados | 24 reutilizáveis |
| Estado | st.session_state | StateManager OOP |
| Type hints | Parcial | 100% |
| Testabilidade | Difícil | Fácil |
| Manutenibilidade | Baixa | Alta |
| Escalabilidade | Limitada | Excelente |

## 🐛 Troubleshooting

### Erro: Módulo não encontrado

Verifique se o caminho está correto em `config.py`:

```python
CAMINHO_MODULO = r"C:\seu\caminho\aqui"
```

### Erro: Banco de dados não conecta

1. Verifique se o arquivo `.accdb` existe
2. Instale o driver MS Access (32-bit ou 64-bit correspondente ao Python)
3. Teste a conexão na página "Executar"

### Porta 8000 em uso

Altere a porta em `config.py`:

```python
class AppConfig:
    PORT = 8080  # ou outra porta disponível
```

## 📝 Próximas Melhorias

- [ ] Testes unitários (pytest)
- [ ] Integração com CI/CD
- [ ] Docker containerization
- [ ] API REST para integração externa
- [ ] Exportação de relatórios em PDF
- [ ] Sistema de notificações (email/slack)
- [ ] Dashboard de performance
- [ ] Autenticação de usuários

## 🤝 Contribuindo

Contribuições são bem-vindas! Este projeto foi construído com arquitetura modular pensando em fácil extensão.

## 📄 Licença

Este projeto é de uso interno.

## 👥 Contato

Para dúvidas ou sugestões sobre a arquitetura modular ReactPy, consulte a documentação dos componentes nos respectivos arquivos.

---

**Versão 7.0** - Arquitetura Modular com ReactPy
Reimplementado de Streamlit para ReactPy com melhorias substanciais em organização, manutenibilidade e escalabilidade.
