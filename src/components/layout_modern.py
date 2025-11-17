"""
Componentes de Layout Modernos
Header, Sidebar, Navegação e Containers com Design System
"""

from reactpy import component, html
from datetime import datetime
from typing import Optional, List, Tuple

from app.config import AppConfig


@component
def modern_header(titulo: str = None, subtitulo: str = None, show_theme_toggle: bool = True):
    """
    Cabeçalho moderno com gradiente e animações

    Args:
        titulo: Título customizado
        subtitulo: Subtítulo customizado
        show_theme_toggle: Mostrar toggle de tema dark/light
    """
    titulo = titulo or AppConfig.APP_TITLE
    subtitulo = subtitulo or f"Versão {AppConfig.APP_VERSION}"

    return html.header(
        {
            "class": "animate-slide-in-down",
            "style": {
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "color": "white",
                "padding": "3rem 2rem",
                "borderRadius": "1.5rem",
                "marginBottom": "2rem",
                "boxShadow": "var(--shadow-xl)",
                "position": "relative",
                "overflow": "hidden",
            }
        },
        # Background pattern
        html.div({
            "style": {
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "background": "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")",
                "opacity": "0.1",
            }
        }),

        # Content
        html.div(
            {"style": {"position": "relative", "zIndex": "1", "textAlign": "center"}},

            # Icon/Logo
            html.div(
                {
                    "style": {
                        "width": "4rem",
                        "height": "4rem",
                        "margin": "0 auto 1rem",
                        "background": "rgba(255,255,255,0.2)",
                        "borderRadius": "1rem",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "fontSize": "2rem",
                        "backdrop_filter": "blur(10px)",
                    }
                },
                "📊"
            ),

            # Title
            html.h1(
                {
                    "style": {
                        "margin": "0",
                        "fontSize": "2.5rem",
                        "fontWeight": "700",
                        "letterSpacing": "-0.025em",
                    }
                },
                titulo
            ),

            # Subtitle
            html.p(
                {
                    "style": {
                        "margin": "0.75rem 0 0",
                        "fontSize": "1.125rem",
                        "opacity": "0.9",
                        "fontWeight": "300",
                    }
                },
                subtitulo
            ),

            # Timestamp
            html.div(
                {
                    "style": {
                        "marginTop": "1.5rem",
                        "display": "inline-flex",
                        "alignItems": "center",
                        "gap": "0.5rem",
                        "padding": "0.5rem 1rem",
                        "background": "rgba(255,255,255,0.15)",
                        "borderRadius": "9999px",
                        "fontSize": "0.875rem",
                        "backdrop_filter": "blur(10px)",
                    }
                },
                html.span("⏰"),
                html.span(f"Atualizado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
            ),
        )
    )


@component
def modern_navigation(pagina_atual: str, on_change):
    """
    Navegação moderna com pills e animações

    Args:
        pagina_atual: Página atualmente ativa
        on_change: Callback quando página muda
    """
    paginas: List[Tuple[str, str, str]] = [
        ("executar", "Executar", "🚀"),
        ("dashboard", "Dashboard", "📊"),
        ("lamina", "Lâmina", "📄"),
        ("historico", "Histórico", "📜"),
        ("configuracoes", "Configurações", "⚙️"),
    ]

    def criar_nav_item(key: str, nome: str, icone: str):
        """Cria item de navegação moderno"""
        ativo = key == pagina_atual

        return html.button(
            {
                "key": key,
                "onClick": lambda e: on_change(key),
                "class": "nav-item" + (" nav-item-active" if ativo else ""),
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "0.5rem",
                    "padding": "0.75rem 1.5rem",
                    "border": "none",
                    "borderRadius": "0.75rem",
                    "fontSize": "0.875rem",
                    "fontWeight": "600" if ativo else "500",
                    "cursor": "pointer",
                    "transition": "all 0.2s",
                    "background": "#667eea" if ativo else "transparent",
                    "color": "white" if ativo else "#6B7280",
                    "boxShadow": "0 4px 6px -1px rgba(0,0,0,0.1)" if ativo else "none",
                    "transform": "scale(1.05)" if ativo else "scale(1)",
                }
            },
            html.span({"style": {"fontSize": "1.25rem"}}, icone),
            html.span(nome)
        )

    return html.nav(
        {
            "class": "nav animate-fade-in",
            "style": {
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "0.5rem",
                "padding": "1rem",
                "background": "white",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-sm)",
                "marginBottom": "2rem",
                "justifyContent": "center",
            }
        },
        *[criar_nav_item(key, nome, icone) for key, nome, icone in paginas]
    )


@component
def modern_container(*children, max_width: str = "1280px"):
    """
    Container moderno responsivo

    Args:
        children: Conteúdo do container
        max_width: Largura máxima
    """
    return html.div(
        {
            "class": "container animate-fade-in",
            "style": {
                "maxWidth": max_width,
                "margin": "0 auto",
                "padding": "0 1rem",
            }
        },
        *children
    )


@component
def modern_grid(*children, cols: int = 3, gap: str = "1.5rem"):
    """
    Grid moderno responsivo

    Args:
        children: Itens do grid
        cols: Número de colunas (padrão: 3)
        gap: Espaço entre itens
    """
    return html.div(
        {
            "style": {
                "display": "grid",
                "gridTemplateColumns": f"repeat(auto-fit, minmax(min(100%, {300}px), 1fr))",
                "gap": gap,
            }
        },
        *children
    )


@component
def modern_sidebar(state_manager):
    """
    Sidebar moderna com glassmorphism

    Args:
        state_manager: Instância do StateManager
    """
    stats = state_manager.get_estatisticas_rapidas() if hasattr(state_manager, 'get_estatisticas_rapidas') else {}

    return html.aside(
        {
            "class": "animate-slide-in-up",
            "style": {
                "background": "rgba(255, 255, 255, 0.8)",
                "backdrop_filter": "blur(10px)",
                "padding": "1.5rem",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-lg)",
                "border": "1px solid rgba(255, 255, 255, 0.3)",
                "minWidth": "280px",
                "position": "sticky",
                "top": "2rem",
            }
        },

        # Header
        html.div(
            {"style": {"marginBottom": "1.5rem", "paddingBottom": "1rem", "border_bottom": "2px solid var(--color-border-light)"}},
            html.h3(
                {"style": {"margin": "0", "fontSize": "1.25rem", "fontWeight": "700", "color": "var(--color-text-primary)"}},
                "🔧 Sistema"
            )
        ),

        # Stats
        html.div(
            {"style": {"display": "flex", "flexDirection": "column", "gap": "1rem"}},

            stat_item("📍 Versão", state_manager.versao_modulo),
            stat_item("📄 Página", state_manager.pagina_atual.capitalize()),
            stat_item("🕐 Hora", datetime.now().strftime("%H:%M:%S")),
        ),

        # Quick Actions
        html.div(
            {"style": {"marginTop": "1.5rem", "paddingTop": "1.5rem", "border_top": "2px solid var(--color-border-light)"}},
            html.h4(
                {"style": {"margin": "0 0 1rem", "fontSize": "1rem", "fontWeight": "600"}},
                "⚡ Ações Rápidas"
            ),
            html.div(
                {"style": {"display": "flex", "flexDirection": "column", "gap": "0.5rem"}},
                quick_action_button("🔄 Atualizar", "refresh"),
                quick_action_button("📥 Exportar", "export"),
                quick_action_button("⚙️ Config", "settings"),
            )
        )
    )


@component
def stat_item(label: str, value: str):
    """Item de estatística para sidebar"""
    return html.div(
        {
            "style": {
                "display": "flex",
                "justifyContent": "space_between",
                "alignItems": "center",
                "padding": "0.75rem",
                "background": "var(--color-bg-secondary)",
                "borderRadius": "0.5rem",
            }
        },
        html.span(
            {"style": {"fontSize": "0.875rem", "color": "var(--color-text-secondary)"}},
            label
        ),
        html.span(
            {"style": {"fontSize": "0.875rem", "fontWeight": "600", "color": "var(--color-text-primary)"}},
            value
        )
    )


@component
def quick_action_button(label: str, action: str):
    """Botão de ação rápida"""
    return html.button(
        {
            "class": "btn btn-ghost btn-sm",
            "style": {
                "width": "100%",
                "justifyContent": "flex_start",
                "textAlign": "left",
                "padding": "0.75rem 1rem",
                "border": "none",
                "background": "transparent",
                "cursor": "pointer",
                "borderRadius": "0.5rem",
                "fontSize": "0.875rem",
                "fontWeight": "500",
                "transition": "all 0.2s",
                "color": "var(--color-text-primary)",
            }
        },
        label
    )


@component
def page_container(*children, titulo: str = "", descricao: str = ""):
    """
    Container de página com título e descrição

    Args:
        children: Conteúdo da página
        titulo: Título da página
        descricao: Descrição da página
    """
    return html.div(
        {"class": "animate-slide-in-up"},

        # Header da página
        html.div(
            {"style": {"marginBottom": "2rem"}},
            html.h2(
                {
                    "style": {
                        "margin": "0",
                        "fontSize": "2rem",
                        "fontWeight": "700",
                        "color": "var(--color-text-primary)",
                    }
                },
                titulo
            ),
            html.p(
                {
                    "style": {
                        "margin": "0.5rem 0 0",
                        "fontSize": "1rem",
                        "color": "var(--color-text-secondary)",
                    }
                },
                descricao
            ) if descricao else None
        ),

        # Content
        html.div(
            {"style": {"display": "flex", "flexDirection": "column", "gap": "1.5rem"}},
            *children
        )
    )


@component
def section_card(titulo: str, *children, icone: str = "📦"):
    """
    Card de seção com título

    Args:
        titulo: Título da seção
        children: Conteúdo da seção
        icone: Ícone da seção
    """
    return html.div(
        {
            "class": "card",
            "style": {
                "background": "white",
                "padding": "1.5rem",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-sm)",
                "transition": "all 0.2s",
            }
        },

        # Header
        html.div(
            {
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "0.75rem",
                    "marginBottom": "1.5rem",
                    "paddingBottom": "1rem",
                    "border_bottom": "2px solid var(--color-border-light)",
                }
            },
            html.span({"style": {"fontSize": "1.5rem"}}, icone),
            html.h3(
                {
                    "style": {
                        "margin": "0",
                        "fontSize": "1.25rem",
                        "fontWeight": "600",
                        "color": "var(--color-text-primary)",
                    }
                },
                titulo
            )
        ),

        # Content
        html.div(*children)
    )
