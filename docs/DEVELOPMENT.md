# Guia de Desenvolvimento

## Setup do Ambiente

### 1. Pré-requisitos

- Python 3.10 ou superior
- Git
- MS Access Database Engine (Windows)
- Editor de código (VS Code recomendado)

### 2. Instalação

```bash
# Clone o repositório
git clone <repository-url>
cd fundos_report_reactpy

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale dependências de produção
pip install -r requirements.txt

# Instale dependências de desenvolvimento
pip install -r requirements-dev.txt

# Configure variáveis de ambiente
cp config\.env.example .env
# Edite .env conforme necessário
```

### 3. Estrutura do Projeto

```
fundos_report_reactpy/
├── src/              # Código fonte
├── tests/            # Testes automatizados
├── config/           # Configurações
├── docs/             # Documentação
├── scripts/          # Scripts auxiliares
├── data/             # Dados persistidos
└── static/           # Assets estáticos
```

---

## Executando a Aplicação

### Modo Desenvolvimento

```bash
# Executar aplicação
python src/app/main.py

# A aplicação estará disponível em:
# http://localhost:8000
```

### Modo Debug

```python
# Em src/app/main.py, ajuste:
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Hot reload
        log_level="debug"
    )
```

---

## Desenvolvimento de Componentes

### Anatomia de um Componente ReactPy

```python
from reactpy import component, html, use_state

@component
def meu_componente(titulo: str, valor: float):
    """Documentação do componente"""

    # Estado reativo
    contador, set_contador = use_state(0)

    # Handler de evento
    def incrementar():
        set_contador(contador + 1)

    # Render
    return html.div(
        {"style": {"padding": "1rem"}},
        html.h2(titulo),
        html.p(f"Valor: {valor}"),
        html.button(
            {"on_click": lambda event: incrementar()},
            f"Cliques: {contador}"
        )
    )
```

### Boas Práticas

1. **Type Hints**: Use sempre type hints
   ```python
   def processar_fundo(fundo: FundoData) -> Dict[str, Any]:
       ...
   ```

2. **Docstrings**: Documente funções e componentes
   ```python
   def calcular_pl(fundos: List[FundoData]) -> float:
       """
       Calcula PL total de fundos

       Args:
           fundos: Lista de fundos

       Returns:
           PL total em reais
       """
       ...
   ```

3. **Componentes Pequenos**: Quebre componentes grandes
   ```python
   # Ruim
   @component
   def dashboard_completo():
       return html.div(...)  # 500 linhas

   # Bom
   @component
   def dashboard():
       return html.div(
           header(),
           metricas(),
           graficos(),
           tabelas()
       )
   ```

---

## Testes

### Executando Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/unit/test_models.py

# Testes de integração (requer DB)
pytest tests/integration/ -m integration
```

### Escrevendo Testes Unitários

```python
# tests/unit/test_meu_modulo.py

import pytest
from src.models.fundo import FundoData

def test_criacao_fundo():
    """Testa criação de FundoData"""
    fundo = FundoData(
        nome="Teste",
        tipo="Multimercado",
        cnpj="00.000.000/0001-00",
        pl=1000000.0
    )

    assert fundo.nome == "Teste"
    assert fundo.pl == 1000000.0

def test_pl_negativo_levanta_excecao():
    """Testa que PL negativo levanta exceção"""
    with pytest.raises(ValueError):
        FundoData(
            nome="Teste",
            tipo="Multimercado",
            cnpj="00.000.000/0001-00",
            pl=-1000000.0
        )
```

### Testes de Integração

```python
# tests/integration/test_report_executor.py

import pytest
from src.services.report_executor import ReportExecutor

@pytest.mark.integration
def test_executar_relatorio_v6(tmp_path):
    """Testa execução completa de relatório V6"""
    executor = ReportExecutor()

    resultado = executor.executar(
        versao="v6",
        data_base="01/01/2024",
        output_dir=str(tmp_path)
    )

    assert resultado.sucesso is True
    assert resultado.arquivo_gerado.exists()
    assert resultado.num_fundos > 0
```

---

## Linting e Formatação

### Ruff (Linter + Formatter)

```bash
# Verificar erros
ruff check src/

# Aplicar correções automáticas
ruff check --fix src/

# Formatar código
ruff format src/
```

### Black (Formatação)

```bash
# Formatar código
black src/ tests/

# Verificar sem modificar
black --check src/
```

### isort (Organizar imports)

```bash
# Organizar imports
isort src/ tests/

# Verificar sem modificar
isort --check src/
```

### mypy (Type Checking)

```bash
# Verificar tipos
mypy src/

# Ignorar erros de bibliotecas externas
mypy --ignore-missing-imports src/
```

---

## Convenções de Código

### Nomenclatura

```python
# Classes: PascalCase
class RelatorioFundos:
    pass

# Funções/variáveis: snake_case
def calcular_rentabilidade():
    patrimonio_liquido = 1000000.0

# Constantes: UPPER_CASE
MAX_RETRIES = 3
DB_CONNECTION_STRING = "..."

# Componentes ReactPy: snake_case
@component
def card_metrica():
    pass
```

### Organização de Imports

```python
# 1. Biblioteca padrão
import sys
from pathlib import Path
from typing import List, Dict

# 2. Bibliotecas third-party
from reactpy import component, html
import pandas as pd

# 3. Imports locais
from app.config import AppConfig
from models.fundo import FundoData
```

### Docstrings (Google Style)

```python
def processar_relatorio(
    data_base: str,
    versao: str = "v6",
    output_dir: str = "./output"
) -> Dict[str, Any]:
    """
    Processa relatório de fundos

    Args:
        data_base: Data base no formato DD/MM/YYYY
        versao: Versão do módulo (v4, v5, v6)
        output_dir: Diretório de saída

    Returns:
        Dicionário com resultado da execução:
            - sucesso: bool
            - arquivo: Path
            - metricas: Dict

    Raises:
        ValueError: Se data_base inválida
        FileNotFoundError: Se módulo não encontrado

    Examples:
        >>> processar_relatorio("01/01/2024", "v6")
        {'sucesso': True, 'arquivo': Path(...), 'metricas': {...}}
    """
    ...
```

---

## Debugging

### VS Code Launch Configuration

Crie `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.app.main:app",
                "--reload",
                "--host", "0.0.0.0",
                "--port", "8000"
            ],
            "jinja": true,
            "justMyCode": false
        },
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "-v",
                "tests/"
            ]
        }
    ]
}
```

### Print Debugging

```python
# Usar logging ao invés de print
import logging

logger = logging.getLogger(__name__)

def processar():
    logger.debug("Iniciando processamento")
    logger.info(f"Processando {len(fundos)} fundos")
    logger.warning("Cache desabilitado")
    logger.error("Erro ao conectar banco")
```

### IPython Debugger

```python
# Adicionar breakpoint
import ipdb; ipdb.set_trace()

# Comandos úteis:
# n - next line
# s - step into
# c - continue
# p var - print variable
# l - list code
```

---

## Git Workflow

### Branches

```bash
# Feature
git checkout -b feature/nova-funcionalidade

# Bugfix
git checkout -b fix/corrigir-bug

# Hotfix
git checkout -b hotfix/corrigir-urgente
```

### Commits

Use **Conventional Commits**:

```bash
# Feat: Nova funcionalidade
git commit -m "feat: adicionar gráfico de barras"

# Fix: Correção de bug
git commit -m "fix: corrigir cálculo de PL"

# Docs: Documentação
git commit -m "docs: atualizar README"

# Refactor: Refatoração
git commit -m "refactor: reorganizar estrutura de pastas"

# Test: Testes
git commit -m "test: adicionar testes para StateManager"

# Style: Formatação
git commit -m "style: formatar código com black"

# Perf: Performance
git commit -m "perf: otimizar queries SQL"

# Chore: Manutenção
git commit -m "chore: atualizar dependências"
```

---

## Contribuindo

### Pull Requests

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/minha-feature`)
3. Commit suas mudanças (`git commit -m 'feat: adicionar feature X'`)
4. Push para a branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request

### Checklist do PR

- [ ] Código segue as convenções do projeto
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Linter e formatter executados
- [ ] Todos os testes passando
- [ ] Type hints adicionados

---

## Recursos

### Documentação

- [ReactPy Docs](https://reactpy.dev/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Plotly Docs](https://plotly.com/python/)
- [pytest Docs](https://docs.pytest.org/)

### Ferramentas

- [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Ruff](https://docs.astral.sh/ruff/)
- [Black](https://black.readthedocs.io/)
- [mypy](https://mypy.readthedocs.io/)

---

## Perguntas Frequentes

**P: Como adicionar uma nova página?**

R: Crie arquivo em `src/pages/`, adicione componente, registre em `main.py`.

**P: Como adicionar novo gráfico?**

R: Adicione componente em `src/components/charts.py` usando Plotly.

**P: Como adicionar nova versão de módulo?**

R: Crie pasta `src/modules/vX/`, adicione lógica, registre em `ReportExecutor`.

**P: Como debugar erro de conexão com banco?**

R: Verifique driver ODBC instalado, caminho do banco em `.env`, permissões.
