"""
Componentes de Cards Modernos
Cards com design system, animações e glassmorphism
"""

from reactpy import component, html
from typing import Optional


@component
def metric_card_modern(
    titulo: str,
    valor: str,
    variacao: Optional[float] = None,
    icone: str = "📊",
    cor: str = "primary"
):
    """
    Card de métrica moderno com gradiente e animação

    Args:
        titulo: Título da métrica
        valor: Valor principal
        variacao: Variação percentual (opcional)
        icone: Ícone emoji
        cor: Cor do tema (primary, success, warning, error)
    """
    # Gradientes por cor (tema azul #005D90)
    gradientes = {
        "primary": "linear-gradient(135deg, #005D90 0%, #1373B7 100%)",
        "success": "linear-gradient(135deg, #1DB954 0%, #17A84A 100%)",
        "warning": "linear-gradient(135deg, #FFB545 0%, #FF9F1C 100%)",
        "error": "linear-gradient(135deg, #E04F63 0%, #D93A4F 100%)",
        "info": "linear-gradient(135deg, #1E90FF 0%, #1373B7 100%)",
    }

    cor_variacao = "#10B981" if variacao and variacao > 0 else "#EF4444" if variacao and variacao < 0 else "#6B7280"
    sinal = "↑" if variacao and variacao > 0 else "↓" if variacao and variacao < 0 else "→"

    return html.div(
        {
            "class": "card animate-slide-in-up",
            "style": {
                "background": gradientes.get(cor, gradientes["primary"]),
                "color": "white",
                "padding": "1.5rem",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-lg)",
                "position": "relative",
                "overflow": "hidden",
                "transition": "all 0.3s",
            },
            "onMouseEnter": lambda e: None,  # Pode adicionar hover effects
        },

        # Background pattern
        html.div({
            "style": {
                "position": "absolute",
                "top": "-50%",
                "right": "-20%",
                "width": "200px",
                "height": "200px",
                "background": "rgba(255, 255, 255, 0.1)",
                "borderRadius": "50%",
                "filter": "blur(40px)",
            }
        }),

        # Content
        html.div(
            {"style": {"position": "relative", "zIndex": "1"}},

            # Header with icon
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "justifyContent": "space_between",
                        "alignItems": "flex_start",
                        "marginBottom": "1rem",
                    }
                },
                html.span(
                    {
                        "style": {
                            "fontSize": "0.875rem",
                            "fontWeight": "500",
                            "textTransform": "uppercase",
                            "letterSpacing": "0.05em",
                            "opacity": "0.9",
                        }
                    },
                    titulo
                ),
                html.div(
                    {
                        "style": {
                            "width": "2.5rem",
                            "height": "2.5rem",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "background": "rgba(255, 255, 255, 0.2)",
                            "borderRadius": "0.75rem",
                            "fontSize": "1.25rem",
                        }
                    },
                    icone
                )
            ),

            # Valor principal
            html.div(
                {
                    "style": {
                        "fontSize": "2.25rem",
                        "fontWeight": "700",
                        "lineHeight": "1",
                        "marginBottom": "0.75rem",
                    }
                },
                valor
            ),

            # Variação
            html.div(
                {
                    "style": {
                        "display": "inline-flex",
                        "alignItems": "center",
                        "gap": "0.25rem",
                        "padding": "0.25rem 0.75rem",
                        "background": "rgba(255, 255, 255, 0.2)",
                        "borderRadius": "9999px",
                        "fontSize": "0.875rem",
                        "fontWeight": "600",
                    }
                },
                html.span(sinal),
                html.span(f"{abs(variacao):.1f}%" if variacao else "0%")
            ) if variacao is not None else html.div(
                {"style": {"height": "2rem"}}  # Spacer
            )
        )
    )


@component
def info_card_modern(titulo: str, *children, icone: str = "ℹ️", tipo: str = "info"):
    """
    Card de informação moderno

    Args:
        titulo: Título do card
        children: Conteúdo do card
        icone: Ícone
        tipo: Tipo (info, success, warning, error)
    """
    cores = {
        "info": {"bg": "#DBEAFE", "border": "#3B82F6", "text": "#1E40AF"},
        "success": {"bg": "#D1FAE5", "border": "#10B981", "text": "#065F46"},
        "warning": {"bg": "#FEF3C7", "border": "#F59E0B", "text": "#92400E"},
        "error": {"bg": "#FEE2E2", "border": "#EF4444", "text": "#991B1B"},
    }

    cor = cores.get(tipo, cores["info"])

    return html.div(
        {
            "class": "card animate-fade-in",
            "style": {
                "background": cor["bg"],
                "border_left": f"4px solid {cor['border']}",
                "padding": "1.25rem",
                "borderRadius": "0.75rem",
                "color": cor["text"],
            }
        },

        html.div(
            {
                "style": {
                    "display": "flex",
                    "gap": "1rem",
                    "alignItems": "flex_start",
                }
            },

            # Ícone
            html.div(
                {
                    "style": {
                        "fontSize": "1.5rem",
                        "flexShrink": "0",
                    }
                },
                icone
            ),

            # Conteúdo
            html.div(
                {"style": {"flex": "1"}},
                html.h4(
                    {
                        "style": {
                            "margin": "0 0 0.5rem",
                            "fontSize": "1rem",
                            "fontWeight": "600",
                        }
                    },
                    titulo
                ),
                html.div(*children)
            )
        )
    )


@component
def fundo_card_modern(fundo_data, on_click=None):
    """
    Card de fundo com design moderno

    Args:
        fundo_data: Dados do fundo (dict ou FundoData)
        on_click: Callback ao clicar
    """
    nome = fundo_data.get("nome", "N/A") if isinstance(fundo_data, dict) else getattr(fundo_data, "nome", "N/A")
    tipo = fundo_data.get("tipo", "N/A") if isinstance(fundo_data, dict) else getattr(fundo_data, "tipo", "N/A")
    pl = fundo_data.get("pl", 0) if isinstance(fundo_data, dict) else getattr(fundo_data, "pl", 0)
    rentabilidade = fundo_data.get("rentabilidade", 0) if isinstance(fundo_data, dict) else getattr(fundo_data, "rentabilidade_mes", 0)

    # Formatar valores
    pl_formatado = f"R$ {pl/1_000_000:.1f}M" if pl > 1_000_000 else f"R$ {pl/1_000:.1f}K"
    rent_cor = "#10B981" if rentabilidade > 0 else "#EF4444" if rentabilidade < 0 else "#6B7280"

    return html.div(
        {
            "class": "card",
            "onClick": on_click,
            "style": {
                "background": "white",
                "padding": "1.5rem",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-sm)",
                "cursor": "pointer" if on_click else "default",
                "transition": "all 0.2s",
                "border": "2px solid transparent",
            },
            "onMouseEnter": lambda e: None,
        },

        # Header
        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space_between",
                    "alignItems": "flex_start",
                    "marginBottom": "1rem",
                }
            },
            html.h3(
                {
                    "style": {
                        "margin": "0",
                        "fontSize": "1.125rem",
                        "fontWeight": "600",
                        "color": "var(--color-text-primary)",
                    }
                },
                nome
            ),
            html.span(
                {
                    "class": "badge badge-primary",
                    "style": {
                        "padding": "0.25rem 0.75rem",
                        "fontSize": "0.75rem",
                        "borderRadius": "9999px",
                    }
                },
                tipo
            )
        ),

        # Métricas
        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "1fr 1fr",
                    "gap": "1rem",
                }
            },

            # PL
            html.div(
                html.div(
                    {"style": {"fontSize": "0.75rem", "color": "var(--color-text-tertiary)", "marginBottom": "0.25rem"}},
                    "Patrimônio Líquido"
                ),
                html.div(
                    {"style": {"fontSize": "1.25rem", "fontWeight": "700", "color": "var(--color-text-primary)"}},
                    pl_formatado
                )
            ),

            # Rentabilidade
            html.div(
                html.div(
                    {"style": {"fontSize": "0.75rem", "color": "var(--color-text-tertiary)", "marginBottom": "0.25rem"}},
                    "Rentabilidade"
                ),
                html.div(
                    {
                        "style": {
                            "fontSize": "1.25rem",
                            "fontWeight": "700",
                            "color": rent_cor,
                        }
                    },
                    f"{rentabilidade:+.2f}%"
                )
            ),
        )
    )


@component
def stats_card_modern(stats: list):
    """
    Card de estatísticas em grade

    Args:
        stats: Lista de tuplas (label, valor, icone)
    """
    return html.div(
        {
            "class": "card",
            "style": {
                "background": "white",
                "padding": "1.5rem",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-sm)",
            }
        },

        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(150px, 1fr))",
                    "gap": "1.5rem",
                }
            },

            *[
                html.div(
                    {
                        "style": {
                            "display": "flex",
                            "flexDirection": "column",
                            "gap": "0.5rem",
                            "alignItems": "center",
                            "textAlign": "center",
                        }
                    },
                    html.div(
                        {
                            "style": {
                                "width": "3rem",
                                "height": "3rem",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "background": "var(--color-primary-50)",
                                "borderRadius": "50%",
                                "fontSize": "1.5rem",
                            }
                        },
                        icone
                    ),
                    html.div(
                        {"style": {"fontSize": "1.75rem", "fontWeight": "700", "color": "var(--color-text-primary)"}},
                        valor
                    ),
                    html.div(
                        {"style": {"fontSize": "0.875rem", "color": "var(--color-text-secondary)"}},
                        label
                    )
                )
                for label, valor, icone in stats
            ]
        )
    )


@component
def loading_card():
    """Card de loading com skeleton"""
    return html.div(
        {
            "class": "card",
            "style": {
                "background": "white",
                "padding": "1.5rem",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-sm)",
            }
        },

        # Title skeleton
        html.div(
            {
                "class": "skeleton",
                "style": {
                    "height": "1.5rem",
                    "width": "60%",
                    "marginBottom": "1rem",
                }
            }
        ),

        # Content skeleton
        html.div(
            {
                "class": "skeleton",
                "style": {
                    "height": "4rem",
                    "width": "100%",
                    "marginBottom": "0.75rem",
                }
            }
        ),

        # Footer skeleton
        html.div(
            {
                "class": "skeleton",
                "style": {
                    "height": "1rem",
                    "width": "40%",
                }
            }
        )
    )


@component
def empty_state_card(mensagem: str = "Nenhum dado disponível", icone: str = "📭"):
    """Card de estado vazio"""
    return html.div(
        {
            "class": "card",
            "style": {
                "background": "white",
                "padding": "3rem",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-sm)",
                "textAlign": "center",
            }
        },

        html.div(
            {"style": {"fontSize": "4rem", "marginBottom": "1rem", "opacity": "0.5"}},
            icone
        ),
        html.p(
            {
                "style": {
                    "margin": "0",
                    "fontSize": "1.125rem",
                    "color": "var(--color-text-secondary)",
                }
            },
            mensagem
        )
    )
