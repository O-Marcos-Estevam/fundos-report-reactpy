## 🎨 Componentes Avançados - Guia Completo

Este guia documenta todos os componentes avançados criados para o sistema.

---

## 📚 Índice

- [Modals](#modals)
- [Dropdowns](#dropdowns)
- [Tabs](#tabs)
- [Accordion](#accordion)
- [Toast Notifications](#toast-notifications)
- [Breadcrumbs](#breadcrumbs)
- [Pagination](#pagination)
- [Theme Selector](#theme-selector)
- [SVG Illustrations](#svg-illustrations)

---

## Modals

### Descrição
Modal/Dialog moderno com overlay e animações.

### Uso

```python
from components.advanced_components import modal
from reactpy import use_state

show_modal, set_show_modal = use_state(False)

modal(
    titulo="Confirmar Ação",
    show=show_modal,
    on_close=lambda: set_show_modal(False),
    size="medium",  # small, medium, large, full
    html.p("Tem certeza que deseja continuar?"),
    html.div(
        {"style": {"display": "flex", "gap": "1rem", "margin_top": "1rem"}},
        html.button(
            {"class": "btn btn-primary", "onClick": lambda e: confirmar()},
            "Confirmar"
        ),
        html.button(
            {"class": "btn btn-outline", "onClick": lambda e: set_show_modal(False)},
            "Cancelar"
        )
    )
)
```

### Props
- `titulo` (str): Título do modal
- `show` (bool): Controla visibilidade
- `on_close` (Callable): Callback ao fechar
- `size` (str): "small", "medium", "large", "full"
- `children`: Conteúdo do modal

---

## Dropdowns

### Descrição
Menu dropdown com animações.

### Uso

```python
from components.advanced_components import dropdown

dropdown(
    label="Opções",
    items=[
        {"label": "Editar", "value": "edit", "icon": "✏️"},
        {"label": "Excluir", "value": "delete", "icon": "🗑️"},
        {"label": "Compartilhar", "value": "share", "icon": "🔗"}
    ],
    on_select=lambda value: print(f"Selecionado: {value}")
)
```

### Props
- `label` (str): Texto do botão
- `items` (List[dict]): Items do menu
  - `label` (str): Texto do item
  - `value` (str): Valor retornado
  - `icon` (str): Emoji/ícone
- `on_select` (Callable): Callback ao selecionar

---

## Tabs

### Descrição
Sistema de tabs navegáveis.

### Uso

```python
from components.advanced_components import tabs

tabs(
    tabs_data=[
        {
            "id": "overview",
            "label": "Visão Geral",
            "icon": "📊",
            "content": html.div("Conteúdo da visão geral...")
        },
        {
            "id": "details",
            "label": "Detalhes",
            "icon": "📄",
            "content": html.div("Conteúdo dos detalhes...")
        },
        {
            "id": "history",
            "label": "Histórico",
            "icon": "📜",
            "content": html.div("Conteúdo do histórico...")
        }
    ],
    default_tab="overview"
)
```

### Props
- `tabs_data` (List[dict]): Dados das tabs
  - `id` (str): ID único
  - `label` (str): Label da tab
  - `icon` (str): Ícone
  - `content` (Component): Conteúdo da tab
- `default_tab` (str): Tab ativa por padrão

---

## Accordion

### Descrição
Accordion/Collapse com múltiplos itens.

### Uso

```python
from components.advanced_components import accordion

accordion(
    items=[
        {
            "title": "O que são fundos de investimento?",
            "icon": "❓",
            "content": html.p("Fundos de investimento são...")
        },
        {
            "title": "Como investir?",
            "icon": "💰",
            "content": html.p("Para investir você deve...")
        },
        {
            "title": "Quais os riscos?",
            "icon": "⚠️",
            "content": html.p("Os principais riscos são...")
        }
    ]
)
```

### Props
- `items` (List[dict]): Itens do accordion
  - `title` (str): Título do item
  - `icon` (str): Ícone
  - `content` (Component): Conteúdo (oculto/visível)

---

## Toast Notifications

### Descrição
Notificações temporárias (toast).

### Uso

```python
from components.advanced_components import toast_notification

toast_notification(
    message="Relatório gerado com sucesso!",
    tipo="success",  # success, error, warning, info
    show=True,
    duration=3000  # ms
)
```

### Props
- `message` (str): Mensagem
- `tipo` (str): "success", "error", "warning", "info"
- `show` (bool): Controla visibilidade
- `duration` (int): Duração em milissegundos

### Tipos

| Tipo | Cor | Ícone | Uso |
|------|-----|-------|-----|
| success | Verde | ✅ | Ações bem-sucedidas |
| error | Vermelho | ❌ | Erros |
| warning | Amarelo | ⚠️ | Avisos |
| info | Azul | ℹ️ | Informações |

---

## Breadcrumbs

### Descrição
Navegação breadcrumb.

### Uso

```python
from components.advanced_components import breadcrumbs

breadcrumbs(
    items=[
        {"label": "Home", "href": "/", "icon": "🏠"},
        {"label": "Dashboard", "href": "/dashboard", "icon": "📊"},
        {"label": "Fundos", "href": "/fundos", "icon": "💼"},
        {"label": "Fundo Alpha", "icon": "📄"}
    ]
)
```

### Props
- `items` (List[dict]): Itens do breadcrumb
  - `label` (str): Texto
  - `href` (str): Link (opcional)
  - `icon` (str): Ícone (opcional)

---

## Pagination

### Descrição
Paginação de lista/tabela.

### Uso

```python
from components.advanced_components import pagination
from reactpy import use_state

current_page, set_current_page = use_state(1)

pagination(
    current_page=current_page,
    total_pages=10,
    on_page_change=lambda page: set_current_page(page)
)
```

### Props
- `current_page` (int): Página atual (1-indexed)
- `total_pages` (int): Total de páginas
- `on_page_change` (Callable): Callback ao mudar página

---

## Theme Selector

### Descrição
Seletor de temas com preview visual.

### Temas Disponíveis

1. **Light** ☀️ - Tema claro padrão
2. **Dark** 🌙 - Tema escuro
3. **Purple Dream** 💜 - Tema roxo moderno
4. **Ocean Blue** 🌊 - Tema azul oceano
5. **Forest Green** 🌲 - Tema verde floresta
6. **Sunset Orange** 🌅 - Tema laranja pôr do sol

### Uso

#### Seletor Completo

```python
from components.theme_selector import theme_selector

theme_selector(
    on_theme_change=lambda theme: print(f"Tema mudou para: {theme}")
)
```

#### Toggle Dark/Light

```python
from components.theme_selector import theme_toggle_button

theme_toggle_button(
    on_theme_change=lambda theme: print(f"Tema: {theme}")
)
```

#### Preview do Tema

```python
from components.theme_selector import theme_preview_card

theme_preview_card()
```

### Theme Manager

```python
from utils.theme_manager import get_theme_manager

theme_manager = get_theme_manager()

# Obter tema atual
current = theme_manager.get_current_theme()

# Mudar tema
theme_manager.set_theme("dark")

# Obter todos os temas
all_themes = theme_manager.get_all_themes()

# Gerar CSS variables
css = theme_manager.generate_css_variables("purple")

# Obter estilos inline
styles = theme_manager.get_inline_styles("ocean")
```

### Criando Tema Customizado

```python
from utils.theme_manager import Theme, get_theme_manager

# Definir tema
custom_theme = Theme(
    name="custom",
    display_name="Meu Tema",
    icon="🎨",
    colors={
        "primary": "#FF6B6B",
        "primary_hover": "#EE5A6F",
        "bg_primary": "#FFFFFF",
        "text_primary": "#2D3748",
        # ... outras cores
    }
)

# Adicionar ao gerenciador
theme_manager = get_theme_manager()
theme_manager.THEMES["custom"] = custom_theme
```

---

## SVG Illustrations

### Descrição
Ilustrações e ícones SVG customizados.

### Ilustrações Disponíveis

#### Empty State

```python
from components.svg_illustrations import empty_state_illustration

empty_state_illustration(width="200px", height="200px")
```

#### Loading

```python
from components.svg_illustrations import loading_illustration

loading_illustration(width="100px", height="100px")
```

#### Success

```python
from components.svg_illustrations import success_illustration

success_illustration(width="150px", height="150px")
```

#### Error

```python
from components.svg_illustrations import error_illustration

error_illustration(width="150px", height="150px")
```

#### Chart

```python
from components.svg_illustrations import chart_illustration

chart_illustration(width="200px", height="200px")
```

### Ícones Disponíveis

#### Fund Icon

```python
from components.svg_illustrations import fund_icon

fund_icon(width="60px", height="60px", color="#4F46E5")
```

#### Money Icon

```python
from components.svg_illustrations import money_icon

money_icon(width="60px", height="60px", color="#10B981")
```

#### Trending Up

```python
from components.svg_illustrations import trending_up_icon

trending_up_icon(width="60px", height="60px", color="#10B981")
```

#### Trending Down

```python
from components.svg_illustrations import trending_down_icon

trending_down_icon(width="60px", height="60px", color="#EF4444")
```

#### Document

```python
from components.svg_illustrations import document_icon

document_icon(width="60px", height="60px", color="#3B82F6")
```

#### Settings

```python
from components.svg_illustrations import settings_icon

settings_icon(width="60px", height="60px", color="#6B7280")
```

### Background Pattern

```python
from components.svg_illustrations import decorative_background_pattern

# Adicionar padrão decorativo de fundo
html.div(
    {"style": {"position": "relative"}},
    decorative_background_pattern(),
    # Conteúdo aqui
)
```

---

## Exemplos Práticos

### Página com Modal de Confirmação

```python
@component
def pagina_com_modal():
    show_modal, set_show_modal = use_state(False)

    def excluir_fundo():
        # Lógica de exclusão
        set_show_modal(False)

    return html.div(
        html.button(
            {
                "class": "btn btn-error",
                "onClick": lambda e: set_show_modal(True)
            },
            "Excluir Fundo"
        ),

        modal(
            titulo="Confirmar Exclusão",
            show=show_modal,
            on_close=lambda: set_show_modal(False),
            html.div(
                error_illustration(width="100px", height="100px"),
                html.p("Tem certeza que deseja excluir este fundo?"),
                html.p({"style": {"color": "var(--color-text-secondary)"}},
                       "Esta ação não pode ser desfeita."),
                html.div(
                    {"style": {"display": "flex", "gap": "1rem", "margin_top": "1.5rem"}},
                    html.button(
                        {"class": "btn btn-error", "onClick": lambda e: excluir_fundo()},
                        "Excluir"
                    ),
                    html.button(
                        {"class": "btn btn-outline", "onClick": lambda e: set_show_modal(False)},
                        "Cancelar"
                    )
                )
            )
        )
    )
```

### Página com Tabs e Accordion

```python
@component
def pagina_documentacao():
    return tabs(
        tabs_data=[
            {
                "id": "faq",
                "label": "FAQ",
                "icon": "❓",
                "content": accordion(
                    items=[
                        {
                            "title": "Como funciona?",
                            "icon": "❓",
                            "content": html.p("Explicação detalhada...")
                        },
                        {
                            "title": "Quanto custa?",
                            "icon": "💰",
                            "content": html.p("Informações de preço...")
                        }
                    ]
                )
            },
            {
                "id": "guide",
                "label": "Guia",
                "icon": "📖",
                "content": html.div("Conteúdo do guia...")
            }
        ]
    )
```

### Página com Tema Customizável

```python
@component
def pagina_configuracoes():
    return html.div(
        breadcrumbs([
            {"label": "Home", "href": "/", "icon": "🏠"},
            {"label": "Configurações", "icon": "⚙️"}
        ]),

        html.h2("Configurações"),

        theme_selector(),

        theme_preview_card()
    )
```

---

## Performance Tips

### Lazy Loading de Modals

```python
# Não renderizar modal até ser necessário
show_modal and modal(...)
```

### Memoização de Tabs

```python
# Usar use_memo para conteúdo pesado
from reactpy import use_memo

heavy_content = use_memo(lambda: processar_dados(), [deps])
```

### SVG Optimization

- Use viewBox para responsividade
- Minimize atributos desnecessários
- Considere usar sprites para múltiplos ícones

---

## Acessibilidade

### ARIA Labels

```python
html.button(
    {"aria-label": "Fechar modal"},
    "×"
)
```

### Keyboard Navigation

Todos os componentes suportam:
- **Tab**: Navegar entre elementos
- **Enter/Space**: Ativar botões
- **Esc**: Fechar modals/dropdowns

### Focus Management

Modals automaticamente:
- Capturam foco ao abrir
- Retornam foco ao fechar
- Prendem foco dentro do modal

---

## Browser Support

✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+

---

**Documentação v1.0** - Componentes Avançados
