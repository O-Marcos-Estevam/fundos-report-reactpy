"""
Componentes Avançados
Modals, Dropdowns, Tabs, Accordion, Toast Notifications
"""

from reactpy import component, html, use_state
from typing import List, Callable, Optional


@component
def modal(titulo: str, show: bool, on_close: Callable, *children, size: str = "medium"):
    """
    Modal/Dialog moderno com overlay

    Args:
        titulo: Título do modal
        show: Se o modal está visível
        on_close: Callback ao fechar
        children: Conteúdo do modal
        size: Tamanho (small, medium, large, full)
    """
    if not show:
        return html.div()

    sizes = {
        "small": "400px",
        "medium": "600px",
        "large": "800px",
        "full": "95vw"
    }

    return html.div(
        {
            "class": "modal-overlay",
            "style": {
                "position": "fixed",
                "top": "0",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "background": "rgba(0, 0, 0, 0.5)",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "zIndex": "var(--z-modal)",
                "backdrop_filter": "blur(4px)",
                "animation": "fadeIn 0.2s ease-out",
            },
            "onClick": lambda e: on_close() if e.get("target") == e.get("currentTarget") else None
        },

        # Modal Content
        html.div(
            {
                "class": "modal-content",
                "style": {
                    "background": "white",
                    "borderRadius": "1rem",
                    "boxShadow": "var(--shadow-2xl)",
                    "maxWidth": sizes.get(size, sizes["medium"]),
                    "width": "100%",
                    "maxHeight": "90vh",
                    "overflow": "hidden",
                    "display": "flex",
                    "flexDirection": "column",
                    "animation": "slideInUp 0.3s ease-out",
                }
            },

            # Header
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "justifyContent": "space_between",
                        "alignItems": "center",
                        "padding": "1.5rem",
                        "border_bottom": "2px solid var(--color-border-light)",
                    }
                },
                html.h3(
                    {
                        "style": {
                            "margin": "0",
                            "fontSize": "1.5rem",
                            "fontWeight": "700",
                            "color": "var(--color-text-primary)",
                        }
                    },
                    titulo
                ),
                html.button(
                    {
                        "onClick": lambda e: on_close(),
                        "class": "btn-ghost",
                        "style": {
                            "border": "none",
                            "background": "transparent",
                            "fontSize": "1.5rem",
                            "cursor": "pointer",
                            "width": "2.5rem",
                            "height": "2.5rem",
                            "borderRadius": "0.5rem",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "transition": "all 0.2s",
                        }
                    },
                    "×"
                )
            ),

            # Body
            html.div(
                {
                    "style": {
                        "padding": "1.5rem",
                        "overflowY": "auto",
                        "flex": "1",
                    }
                },
                *children
            )
        )
    )


@component
def dropdown(label: str, items: List[dict], on_select: Callable):
    """
    Dropdown menu moderno

    Args:
        label: Label do botão
        items: Lista de items [{"label": "...", "value": "...", "icon": "..."}]
        on_select: Callback ao selecionar (recebe value)
    """
    is_open, set_is_open = use_state(False)

    def toggle():
        set_is_open(not is_open)

    def select_item(value):
        on_select(value)
        set_is_open(False)

    return html.div(
        {
            "style": {
                "position": "relative",
                "display": "inline-block",
            }
        },

        # Trigger Button
        html.button(
            {
                "onClick": lambda e: toggle(),
                "class": "btn btn-outline",
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "0.5rem",
                }
            },
            html.span(label),
            html.span(
                {"style": {"transform": "rotate(90deg)" if is_open else "rotate(0deg)", "transition": "transform 0.2s"}},
                "▶"
            )
        ),

        # Dropdown Menu
        html.div(
            {
                "style": {
                    "position": "absolute",
                    "top": "calc(100% + 0.5rem)",
                    "left": "0",
                    "background": "white",
                    "borderRadius": "0.75rem",
                    "boxShadow": "var(--shadow-lg)",
                    "minWidth": "200px",
                    "zIndex": "var(--z-dropdown)",
                    "display": "block" if is_open else "none",
                    "animation": "slideInDown 0.2s ease-out",
                    "border": "1px solid var(--color-border-light)",
                }
            },
            *[
                html.button(
                    {
                        "key": item["value"],
                        "onClick": lambda e, v=item["value"]: select_item(v),
                        "style": {
                            "width": "100%",
                            "textAlign": "left",
                            "padding": "0.75rem 1rem",
                            "border": "none",
                            "background": "transparent",
                            "cursor": "pointer",
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "0.75rem",
                            "transition": "background 0.2s",
                            "fontSize": "0.875rem",
                        }
                    },
                    html.span({"style": {"fontSize": "1.25rem"}}, item.get("icon", "")),
                    html.span(item["label"])
                )
                for item in items
            ]
        ) if is_open else None
    )


@component
def tabs(tabs_data: List[dict], default_tab: str = None):
    """
    Tabs navegáveis

    Args:
        tabs_data: Lista de tabs [{"id": "...", "label": "...", "icon": "...", "content": component}]
        default_tab: Tab ativo por padrão
    """
    active_tab, set_active_tab = use_state(default_tab or tabs_data[0]["id"])

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-sm)",
                "overflow": "hidden",
            }
        },

        # Tab Headers
        html.div(
            {
                "style": {
                    "display": "flex",
                    "border_bottom": "2px solid var(--color-border-light)",
                    "background": "var(--color-bg-secondary)",
                }
            },
            *[
                html.button(
                    {
                        "key": tab["id"],
                        "onClick": lambda e, tid=tab["id"]: set_active_tab(tid),
                        "style": {
                            "flex": "1",
                            "padding": "1rem 1.5rem",
                            "border": "none",
                            "background": "transparent",
                            "cursor": "pointer",
                            "fontWeight": "600" if active_tab == tab["id"] else "500",
                            "color": "var(--color-primary)" if active_tab == tab["id"] else "var(--color-text-secondary)",
                            "border_bottom": f"3px solid var(--color-primary)" if active_tab == tab["id"] else "3px solid transparent",
                            "transition": "all 0.2s",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "gap": "0.5rem",
                        }
                    },
                    html.span({"style": {"fontSize": "1.25rem"}}, tab.get("icon", "")),
                    html.span(tab["label"])
                )
                for tab in tabs_data
            ]
        ),

        # Tab Content
        html.div(
            {
                "class": "animate-fade-in",
                "style": {
                    "padding": "1.5rem",
                }
            },
            *[tab["content"] for tab in tabs_data if tab["id"] == active_tab]
        )
    )


@component
def accordion(items: List[dict]):
    """
    Accordion/Collapse moderno

    Args:
        items: Lista de items [{"title": "...", "content": "...", "icon": "..."}]
    """
    open_index, set_open_index = use_state(None)

    def toggle(index):
        set_open_index(None if open_index == index else index)

    return html.div(
        {
            "style": {
                "display": "flex",
                "flexDirection": "column",
                "gap": "0.5rem",
            }
        },
        *[
            html.div(
                {
                    "key": str(idx),
                    "style": {
                        "background": "white",
                        "borderRadius": "0.75rem",
                        "border": "2px solid var(--color-border-light)",
                        "overflow": "hidden",
                        "transition": "all 0.2s",
                    }
                },

                # Header
                html.button(
                    {
                        "onClick": lambda e, i=idx: toggle(i),
                        "style": {
                            "width": "100%",
                            "padding": "1rem 1.5rem",
                            "border": "none",
                            "background": "var(--color-bg-secondary)" if open_index == idx else "transparent",
                            "cursor": "pointer",
                            "display": "flex",
                            "justifyContent": "space_between",
                            "alignItems": "center",
                            "fontWeight": "600",
                            "textAlign": "left",
                            "transition": "all 0.2s",
                        }
                    },
                    html.div(
                        {
                            "style": {
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "0.75rem",
                            }
                        },
                        html.span({"style": {"fontSize": "1.25rem"}}, item.get("icon", "📋")),
                        html.span(item["title"])
                    ),
                    html.span(
                        {
                            "style": {
                                "transform": f"rotate({180 if open_index == idx else 0}deg)",
                                "transition": "transform 0.2s",
                            }
                        },
                        "▼"
                    )
                ),

                # Content
                html.div(
                    {
                        "style": {
                            "maxHeight": "500px" if open_index == idx else "0",
                            "overflow": "hidden",
                            "transition": "max-height 0.3s ease-out",
                        }
                    },
                    html.div(
                        {
                            "style": {
                                "padding": "1rem 1.5rem",
                                "color": "var(--color-text-secondary)",
                            }
                        },
                        item["content"]
                    )
                ) if open_index == idx else None
            )
            for idx, item in enumerate(items)
        ]
    )


@component
def toast_notification(message: str, tipo: str = "info", show: bool = True, duration: int = 3000):
    """
    Toast notification (notificação temporária)

    Args:
        message: Mensagem
        tipo: Tipo (success, error, warning, info)
        show: Se está visível
        duration: Duração em ms
    """
    if not show:
        return html.div()

    cores = {
        "success": {"bg": "#10B981", "icon": "✅"},
        "error": {"bg": "#EF4444", "icon": "❌"},
        "warning": {"bg": "#F59E0B", "icon": "⚠️"},
        "info": {"bg": "#3B82F6", "icon": "ℹ️"},
    }

    cor = cores.get(tipo, cores["info"])

    return html.div(
        {
            "class": "toast animate-slide-in-up",
            "style": {
                "position": "fixed",
                "bottom": "2rem",
                "right": "2rem",
                "background": cor["bg"],
                "color": "white",
                "padding": "1rem 1.5rem",
                "borderRadius": "0.75rem",
                "boxShadow": "var(--shadow-xl)",
                "display": "flex",
                "alignItems": "center",
                "gap": "0.75rem",
                "zIndex": "var(--z-tooltip)",
                "minWidth": "300px",
                "animation": "slideInUp 0.3s ease-out",
            }
        },
        html.span({"style": {"fontSize": "1.5rem"}}, cor["icon"]),
        html.span({"style": {"fontWeight": "500"}}, message)
    )


@component
def breadcrumbs(items: List[dict]):
    """
    Breadcrumbs de navegação

    Args:
        items: [{"label": "Home", "href": "/", "icon": "🏠"}]
    """
    return html.nav(
        {
            "style": {
                "display": "flex",
                "alignItems": "center",
                "gap": "0.5rem",
                "padding": "0.75rem 0",
                "fontSize": "0.875rem",
            }
        },
        *[
            html.div(
                {
                    "key": str(idx),
                    "style": {"display": "flex", "alignItems": "center", "gap": "0.5rem"}
                },
                html.a(
                    {
                        "href": item.get("href", "#"),
                        "style": {
                            "color": "var(--color-primary)" if idx == len(items) - 1 else "var(--color-text-secondary)",
                            "textDecoration": "none",
                            "fontWeight": "600" if idx == len(items) - 1 else "400",
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "0.25rem",
                            "transition": "color 0.2s",
                        }
                    },
                    html.span(item.get("icon", "")),
                    html.span(item["label"])
                ),
                html.span(
                    {"style": {"color": "var(--color-text-tertiary)"}},
                    "›"
                ) if idx < len(items) - 1 else None
            )
            for idx, item in enumerate(items)
        ]
    )


@component
def pagination(current_page: int, total_pages: int, on_page_change: Callable):
    """
    Paginação

    Args:
        current_page: Página atual (1-indexed)
        total_pages: Total de páginas
        on_page_change: Callback ao mudar página
    """
    def create_page_button(page: int, is_current: bool = False):
        return html.button(
            {
                "key": str(page),
                "onClick": lambda e: on_page_change(page),
                "disabled": is_current,
                "style": {
                    "padding": "0.5rem 0.75rem",
                    "border": "2px solid var(--color-border-light)",
                    "background": "var(--color-primary)" if is_current else "white",
                    "color": "white" if is_current else "var(--color-text-primary)",
                    "borderRadius": "0.5rem",
                    "cursor": "pointer" if not is_current else "default",
                    "fontWeight": "600" if is_current else "500",
                    "transition": "all 0.2s",
                    "minWidth": "2.5rem",
                }
            },
            str(page)
        )

    return html.div(
        {
            "style": {
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "gap": "0.5rem",
                "padding": "1rem 0",
            }
        },

        # Previous
        html.button(
            {
                "onClick": lambda e: on_page_change(current_page - 1),
                "disabled": current_page == 1,
                "class": "btn btn-outline btn-sm",
                "style": {"opacity": "0.5" if current_page == 1 else "1"}
            },
            "← Anterior"
        ),

        # Pages
        *[create_page_button(p, p == current_page) for p in range(1, total_pages + 1)],

        # Next
        html.button(
            {
                "onClick": lambda e: on_page_change(current_page + 1),
                "disabled": current_page == total_pages,
                "class": "btn btn-outline btn-sm",
                "style": {"opacity": "0.5" if current_page == total_pages else "1"}
            },
            "Próximo →"
        )
    )
