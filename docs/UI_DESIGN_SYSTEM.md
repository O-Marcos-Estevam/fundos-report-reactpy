# 🎨 Design System - Fundos Report ReactPy

Sistema de design moderno, consistente e acessível.

## 📋 Índice

- [Princípios de Design](#princípios-de-design)
- [Design Tokens](#design-tokens)
- [Componentes](#componentes)
- [Padrões de Layout](#padrões-de-layout)
- [Animações](#animações)
- [Dark Mode](#dark-mode)
- [Responsividade](#responsividade)
- [Acessibilidade](#acessibilidade)

---

## 🎯 Princípios de Design

### 1. **Clareza**
- Informação clara e direta
- Hierarquia visual bem definida
- Uso intencional de cor e espaço

### 2. **Consistência**
- Design tokens padronizados
- Componentes reutilizáveis
- Padrões de interação uniformes

### 3. **Eficiência**
- Navegação intuitiva
- Ações rápidas e diretas
- Feedback visual imediato

### 4. **Modernidade**
- Design contemporâneo
- Animações suaves
- Glassmorphism e gradientes

---

## 🎨 Design Tokens

### Cores

#### Cores Primárias
```css
--color-primary: #4F46E5        /* Indigo 600 */
--color-primary-hover: #4338CA   /* Indigo 700 */
--color-primary-light: #6366F1   /* Indigo 500 */
--color-primary-dark: #3730A3    /* Indigo 800 */
```

#### Cores de Status
```css
--color-success: #10B981   /* Green */
--color-warning: #F59E0B   /* Amber */
--color-error: #EF4444     /* Red */
--color-info: #3B82F6      /* Blue */
```

#### Cores de Texto
```css
--color-text-primary: #111827     /* Gray 900 */
--color-text-secondary: #6B7280   /* Gray 500 */
--color-text-tertiary: #9CA3AF    /* Gray 400 */
```

### Tipografia

#### Escala de Tamanhos
```css
--font-size-xs: 0.75rem    /* 12px */
--font-size-sm: 0.875rem   /* 14px */
--font-size-base: 1rem     /* 16px */
--font-size-lg: 1.125rem   /* 18px */
--font-size-xl: 1.25rem    /* 20px */
--font-size-2xl: 1.5rem    /* 24px */
--font-size-3xl: 1.875rem  /* 30px */
--font-size-4xl: 2.25rem   /* 36px */
```

#### Pesos
```css
--font-weight-normal: 400
--font-weight-medium: 500
--font-weight-semibold: 600
--font-weight-bold: 700
```

### Espaçamento

Sistema baseado em múltiplos de 4px:

```css
--space-1: 0.25rem   /* 4px */
--space-2: 0.5rem    /* 8px */
--space-3: 0.75rem   /* 12px */
--space-4: 1rem      /* 16px */
--space-6: 1.5rem    /* 24px */
--space-8: 2rem      /* 32px */
--space-12: 3rem     /* 48px */
```

### Sombras

```css
--shadow-sm: 0 1px 3px rgba(0,0,0,0.1)
--shadow-md: 0 4px 6px rgba(0,0,0,0.1)
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1)
--shadow-xl: 0 20px 25px rgba(0,0,0,0.1)
```

### Border Radius

```css
--radius-sm: 0.25rem   /* 4px */
--radius-md: 0.375rem  /* 6px */
--radius-lg: 0.5rem    /* 8px */
--radius-xl: 0.75rem   /* 12px */
--radius-2xl: 1rem     /* 16px */
--radius-full: 9999px  /* Circle */
```

---

## 🧩 Componentes

### Buttons

#### Variantes

**Primary Button**
```python
from components.cards_modern import metric_card_modern

html.button(
    {"class": "btn btn-primary"},
    "Executar Relatório"
)
```

**Secondary Button**
```python
html.button(
    {"class": "btn btn-secondary"},
    "Cancelar"
)
```

**Outline Button**
```python
html.button(
    {"class": "btn btn-outline"},
    "Ver Detalhes"
)
```

**Ghost Button**
```python
html.button(
    {"class": "btn btn-ghost"},
    "Configurações"
)
```

#### Tamanhos
```python
# Pequeno
html.button({"class": "btn btn-primary btn-sm"}, "Pequeno")

# Normal (padrão)
html.button({"class": "btn btn-primary"}, "Normal")

# Grande
html.button({"class": "btn btn-primary btn-lg"}, "Grande")
```

### Cards

#### Metric Card
```python
from components.cards_modern import metric_card_modern

metric_card_modern(
    titulo="Patrimônio Total",
    valor="R$ 15.3B",
    variacao=5.2,
    icone="💰",
    cor="success"
)
```

#### Info Card
```python
from components.cards_modern import info_card_modern

info_card_modern(
    titulo="Atenção",
    icone="⚠️",
    tipo="warning",
    html.p("Processamento pode levar alguns minutos.")
)
```

#### Fundo Card
```python
from components.cards_modern import fundo_card_modern

fundo_card_modern(
    fundo_data={
        "nome": "Fundo Alpha",
        "tipo": "Multimercado",
        "pl": 1500000000,
        "rentabilidade": 2.5
    },
    on_click=lambda: print("Clicado")
)
```

### Inputs

#### Text Input
```python
html.div(
    {"class": "input-group"},
    html.label({"class": "input-label"}, "Nome do Fundo"),
    html.input({"class": "input", "type": "text", "placeholder": "Digite o nome..."})
)
```

#### Select
```python
html.select(
    {"class": "input select"},
    html.option({"value": "v4"}, "Versão 4"),
    html.option({"value": "v5"}, "Versão 5"),
    html.option({"value": "v6", "selected": True}, "Versão 6")
)
```

#### Checkbox
```python
html.label(
    {"style": {"display": "flex", "align_items": "center", "gap": "0.5rem"}},
    html.input({"type": "checkbox", "class": "checkbox"}),
    html.span("Aceito os termos")
)
```

### Tables

```python
html.div(
    {"class": "table-container"},
    html.table(
        {"class": "table"},
        html.thead(
            html.tr(
                html.th("Fundo"),
                html.th("PL"),
                html.th("Rent. %")
            )
        ),
        html.tbody(
            html.tr(
                html.td("Fundo Alpha"),
                html.td("R$ 1.5B"),
                html.td("+2.5%")
            )
        )
    )
)
```

### Badges

```python
# Success
html.span({"class": "badge badge-success"}, "Ativo")

# Warning
html.span({"class": "badge badge-warning"}, "Pendente")

# Error
html.span({"class": "badge badge-error"}, "Erro")

# Info
html.span({"class": "badge badge-info"}, "Info")
```

### Alerts

```python
html.div(
    {"class": "alert alert-success"},
    "✅ Relatório gerado com sucesso!"
)

html.div(
    {"class": "alert alert-error"},
    "❌ Erro ao processar dados."
)
```

---

## 📐 Padrões de Layout

### Container
```python
from components.layout_modern import modern_container

modern_container(
    max_width="1280px",
    # Conteúdo aqui
)
```

### Grid Responsivo
```python
from components.layout_modern import modern_grid

modern_grid(
    cols=3,
    gap="1.5rem",
    card1,
    card2,
    card3
)
```

### Page Container
```python
from components.layout_modern import page_container

page_container(
    titulo="Dashboard",
    descricao="Visão geral dos fundos",
    # Conteúdo da página
)
```

### Section Card
```python
from components.layout_modern import section_card

section_card(
    titulo="Métricas Principais",
    icone="📊",
    # Conteúdo da seção
)
```

---

## ✨ Animações

### Classes de Animação

#### Fade In
```python
html.div({"class": "animate-fade-in"}, "Conteúdo")
```

#### Slide In Up
```python
html.div({"class": "animate-slide-in-up"}, "Conteúdo")
```

#### Slide In Down
```python
html.div({"class": "animate-slide-in-down"}, "Conteúdo")
```

### Transições

```python
# Fast (150ms)
html.div({"class": "transition-fast"}, "Conteúdo")

# Base (200ms)
html.div({"class": "transition"}, "Conteúdo")

# Slow (300ms)
html.div({"class": "transition-slow"}, "Conteúdo")
```

---

## 🌙 Dark Mode

### Ativação

```python
# Adicionar atributo no body ou root
html.body({"data-theme": "dark"})
```

### Cores no Dark Mode

O sistema automaticamente ajusta:
- Backgrounds: Cinzas escuros
- Texto: Cores claras
- Bordas: Mais sutis
- Sombras: Mais intensas

### Exemplo de Componente com Dark Mode

```python
html.div(
    {
        "style": {
            "background": "var(--color-bg-primary)",
            "color": "var(--color-text-primary)",
        }
    },
    "Conteúdo"
)
```

---

## 📱 Responsividade

### Breakpoints

```css
/* Mobile: < 640px */
/* Tablet: 640px - 1024px */
/* Desktop: > 1024px */
```

### Classes Responsivas

```python
# Grid responsivo
html.div(
    {"class": "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4"},
    # Itens
)
```

### Mobile-First

Sempre começar com mobile e adicionar melhorias para telas maiores:

```python
html.div(
    {
        "style": {
            "padding": "1rem",           # Mobile
            "@media (min-width: 768px)": {
                "padding": "2rem"         # Desktop
            }
        }
    }
)
```

---

## ♿ Acessibilidade

### Contraste

- Texto principal: Mínimo 4.5:1
- Texto grande: Mínimo 3:1
- UI Components: Mínimo 3:1

### Foco

Todos os elementos interativos têm foco visível:

```css
.btn:focus {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}
```

### Semântica HTML

```python
# Usar elementos semânticos corretos
html.button()  # Para ações
html.a()       # Para navegação
html.nav()     # Para navegação
html.main()    # Para conteúdo principal
html.article() # Para artigos/cards
```

### ARIA Labels

```python
html.button(
    {"aria-label": "Fechar modal"},
    "×"
)
```

---

## 🎨 Exemplos Práticos

### Dashboard Card com Gradiente

```python
metric_card_modern(
    titulo="Total de Fundos",
    valor="47",
    variacao=12.5,
    icone="🏦",
    cor="primary"
)
```

### Formulário de Busca

```python
html.form(
    {"class": "flex gap-4"},
    html.div(
        {"class": "input-group flex-1"},
        html.input({
            "class": "input",
            "type": "search",
            "placeholder": "Buscar fundo..."
        })
    ),
    html.button(
        {"class": "btn btn-primary"},
        "🔍 Buscar"
    )
)
```

### Lista de Fundos

```python
modern_grid(
    cols=3,
    gap="1.5rem",
    *[fundo_card_modern(fundo) for fundo in fundos]
)
```

---

## 📚 Recursos

### Arquivos CSS

- `static/css/design-system.css` - Design tokens e utilidades
- `static/css/components.css` - Componentes específicos

### Componentes Python

- `src/components/layout_modern.py` - Layouts modernos
- `src/components/cards_modern.py` - Cards modernos

### Ferramentas

- [Coolors](https://coolors.co/) - Paletas de cores
- [Hero Patterns](https://heropatterns.com/) - Padrões SVG
- [CSS Gradient](https://cssgradient.io/) - Gradientes

---

## 🚀 Começando

### 1. Importar CSS

```python
# Em main.py
html.link({"rel": "stylesheet", "href": "/static/css/design-system.css"})
html.link({"rel": "stylesheet", "href": "/static/css/components.css"})
```

### 2. Usar Componentes

```python
from components.layout_modern import modern_header, modern_navigation
from components.cards_modern import metric_card_modern

modern_header(titulo="Meu App")
modern_navigation(pagina_atual="dashboard", on_change=mudar_pagina)
metric_card_modern(titulo="Métricas", valor="100")
```

### 3. Aplicar Classes Utilitárias

```python
html.div(
    {"class": "flex items-center gap-4 p-4 rounded-lg shadow-md"},
    # Conteúdo
)
```

---

**Design System v1.0** - Fundos Report ReactPy
