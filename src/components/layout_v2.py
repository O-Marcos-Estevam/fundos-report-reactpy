"""
Layout V2 inspirado em dashboard moderno
"""

from reactpy import component, html
from reactpy.html import make_vdom_constructor
from typing import Callable, List, Tuple

from app.config import AppConfig

# Criar construtor para elemento SVG path
path = make_vdom_constructor("path")


MENU_ITEMS: List[Tuple[str, str, str]] = [
    ("dashboard", "Dashboard", "📊"),
    ("executar", "Executar", "🚀"),
    ("lamina", "Lâmina", "📄"),
    ("historico", "Histórico", "🕑"),
    ("configuracoes", "Configurações", "⚙️"),
]


def _sidebar_item(key: str, label: str, icon: str, active: bool, on_change: Callable[[str], None]):
    classes = ["sidebar-item"]
    if active:
        classes.append("sidebar-item-active")

    return html.button(
        {
            "class": " ".join(classes),
            "onClick": lambda e: on_change(key),
        },
        html.span(icon),
        html.span(label)
    )


@component
def sidebar_v2(pagina_atual: str, on_change: Callable[[str], None]):
    """Sidebar vertical com identidade azul"""
    return html.aside(
        {"class": "app-sidebar animate-slide-in"},
        html.div(
            {"class": "sidebar-logo"},
            html.span({"class": "badge"}, ["✨", "  ReactPy Dashboard"]),
            html.h1("Relatório de Fundos")
        ),
        html.nav(
            {"class": "sidebar-nav"},
            *[
                _sidebar_item(key, label, icon, pagina_atual == key, on_change)
                for key, label, icon in MENU_ITEMS
            ]
        ),
        html.div(
            {"class": "sidebar-footer"},
            f"Versão {AppConfig.APP_VERSION} · {AppConfig.APP_TITLE}"
        )
    )


@component
def topbar_v2(usuario: str = "Administrador"):
    """Topbar com barra de pesquisa e informações do usuário"""
    return html.div(
        {"class": "app-topbar animate-fade-in"},
        html.div(
            {"class": "topbar-title"},
            html.h2("Dashboard"),
            html.span("Resumo geral das operações e relatórios")
        ),
        html.div(
            {"class": "topbar-actions"},
            html.div(
                {"class": "search-bar"},
                html.svg(
                    {
                        "xmlns": "http://www.w3.org/2000/svg",
                        "fill": "none",
                        "viewBox": "0 0 24 24",
                        "stroke_width": "1.5",
                        "stroke": "currentColor",
                    },
                    path({
                        "stroke_linecap": "round",
                        "stroke_linejoin": "round",
                        "d": "M21 21l-4.35-4.35m1.35-4.65a6 6 0 11-12 0 6 6 0 0112 0z"
                    })
                ),
                html.input({"type": "search", "placeholder": "Pesquisar fundos, relatórios..."})
            ),
            html.div(
                {"class": "user-pill"},
                html.span({"class": "user-avatar"}, usuario[0] if usuario else "U"),
                html.div(
                    {"style": {"display": "flex", "flexDirection": "column", "gap": "0.2rem"}},
                    html.span({"style": {"fontWeight": "600", "fontSize": "0.9rem"}}, usuario or "Usuário"),
                    html.span({"style": {"fontSize": "0.75rem", "color": "#6B7280"}}, "Administrador")
                )
            )
        )
    )


@component
def environment_banner():
    """Banner indicando modo de operação (DEMO vs PRODUCTION)"""
    if AppConfig.USE_MOCK_DATA:
        return html.div(
            {
                "class": "alert alert-info",
                "style": {
                    "margin": "0",
                    "borderRadius": "0",
                    "borderLeft": "none",
                    "borderRight": "none",
                    "borderTop": "none",
                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "color": "white",
                    "padding": "0.75rem 1.5rem",
                    "textAlign": "center",
                    "fontWeight": "500",
                    "fontSize": "0.9rem",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
                }
            },
            "🎭 MODO DEMONSTRAÇÃO - ",
            html.span({"style": {"fontWeight": "600"}}, "Dados de exemplo"),
            " • Para executar com dados reais, configure o banco Access localmente"
        )
    elif AppConfig.HAS_ACCESS:
        return html.div(
            {
                "class": "alert alert-success",
                "style": {
                    "margin": "0",
                    "borderRadius": "0",
                    "borderLeft": "none",
                    "borderRight": "none",
                    "borderTop": "none",
                    "background": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
                    "color": "white",
                    "padding": "0.75rem 1.5rem",
                    "textAlign": "center",
                    "fontWeight": "500",
                    "fontSize": "0.9rem",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
                }
            },
            "✅ MODO PRODUÇÃO - ",
            html.span({"style": {"fontWeight": "600"}}, "Banco Access conectado"),
            " • Pronto para executar relatórios reais"
        )
    else:
        return html.div({"style": {"display": "none"}})


@component
def app_shell_v2(pagina_atual: str, on_change: Callable[[str], None], *children):
    """Estrutura principal do dashboard"""
    return html.div(
        {"class": "app-shell"},
        sidebar_v2(pagina_atual, on_change),
        html.div(
            {"class": "app-main"},
            environment_banner(),  # Banner de modo
            topbar_v2(),
            html.div({"class": "main-content"}, *children)
        )
    )

