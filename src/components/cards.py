"""
Componentes de Cards
Cards para métricas, status e informações
"""

from reactpy import component, html
from typing import Optional

from app.config import AppConfig


@component
def card_metrica(
    titulo: str,
    valor: str,
    variacao: Optional[float] = None,
    cor: str = "primary",
    icone: str = "📊"
):
    """
    Card com métrica e variação opcional

    Args:
        titulo: Título da métrica
        valor: Valor principal
        variacao: Variação percentual (opcional)
        cor: Cor do tema
        icone: Ícone do card
    """
    # Determinar cor da variação
    if variacao is not None:
        if variacao > 0:
            cor_variacao = AppConfig.get_color('success')
            sinal = "+"
        elif variacao < 0:
            cor_variacao = AppConfig.get_color('error')
            sinal = ""
        else:
            cor_variacao = "#999"
            sinal = ""
    else:
        cor_variacao = "#999"
        sinal = ""

    return html.div(
        {
            "style": {
                "background": "white",
                "padding": "1.5rem",
                "borderRadius": "12px",
                "border_left": f"5px solid {AppConfig.get_color(cor)}",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.07)",
                "transition": "transform 0.2s, box-shadow 0.2s",
                "minWidth": "200px",
            }
        },
        # Ícone + Título
        html.div(
            {"style": {"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}},
            html.span(
                {"style": {"fontSize": "1.5rem", "marginRight": "0.5rem"}},
                icone
            ),
            html.div(
                {"style": {"color": "#666", "fontSize": "0.9rem", "fontWeight": "500"}},
                titulo
            )
        ),
        # Valor
        html.div(
            {
                "style": {
                    "fontSize": "2rem",
                    "fontWeight": "700",
                    "color": AppConfig.get_color(cor),
                    "marginBottom": "0.5rem",
                }
            },
            valor
        ),
        # Variação (se houver)
        html.div(
            {"style": {"color": cor_variacao, "fontSize": "0.9rem", "fontWeight": "600"}},
            f"{sinal}{variacao:.2f}%" if variacao is not None else ""
        ) if variacao is not None else None
    )


@component
def card_status(
    titulo: str,
    mensagem: str,
    tipo: str = "info",
    icone: Optional[str] = None
):
    """
    Card colorido com status/mensagem

    Args:
        titulo: Título do card
        mensagem: Mensagem/conteúdo
        tipo: Tipo (success, warning, error, info)
        icone: Ícone customizado (opcional)
    """
    # Mapear tipo para cor e ícone padrão
    config_tipo = {
        "success": {"cor": AppConfig.get_color('success'), "bg": "#d4edda", "icone": "✅"},
        "warning": {"cor": AppConfig.get_color('warning'), "bg": "#fff3cd", "icone": "⚠️"},
        "error": {"cor": AppConfig.get_color('error'), "bg": "#f8d7da", "icone": "❌"},
        "info": {"cor": AppConfig.get_color('info'), "bg": "#d1ecf1", "icone": "ℹ️"},
    }

    config = config_tipo.get(tipo, config_tipo["info"])
    icone_final = icone or config["icone"]

    return html.div(
        {
            "style": {
                "background": config["bg"],
                "border": f"1px solid {config['cor']}",
                "borderRadius": "12px",
                "padding": "1.5rem",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.07)",
            }
        },
        html.div(
            {
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "0.5rem",
                }
            },
            html.span(
                {"style": {"fontSize": "1.5rem", "marginRight": "0.5rem"}},
                icone_final
            ),
            html.h4(
                {"style": {"margin": "0", "color": config["cor"], "fontSize": "1.1rem"}},
                titulo
            )
        ),
        html.p(
            {"style": {"margin": "0", "color": "#333", "lineHeight": "1.5"}},
            mensagem
        )
    )


@component
def card_info(titulo: str, *children, icone: str = "📋"):
    """
    Card informativo genérico

    Args:
        titulo: Título do card
        *children: Conteúdo do card
        icone: Ícone do card
    """
    return html.div(
        {
            "style": {
                "background": "#f8f9fa",
                "padding": "1.5rem",
                "borderRadius": "12px",
                "border": "1px solid #e0e0e0",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
            }
        },
        html.div(
            {
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "1rem",
                    "paddingBottom": "0.5rem",
                    "border_bottom": "2px solid #e0e0e0",
                }
            },
            html.span(
                {"style": {"fontSize": "1.5rem", "marginRight": "0.5rem"}},
                icone
            ),
            html.h4(
                {"style": {"margin": "0", "color": "#333"}},
                titulo
            )
        ),
        html.div(
            {"style": {"color": "#555"}},
            *children
        )
    )


@component
def card_fundo(nome: str, pl: float, tipo: str, variacao: Optional[float] = None):
    """
    Card específico para exibir dados de um fundo

    Args:
        nome: Nome do fundo
        pl: Patrimônio líquido
        tipo: Tipo do fundo
        variacao: Variação percentual
    """
    cor_variacao = AppConfig.get_color('success') if variacao and variacao > 0 else AppConfig.get_color('error') if variacao and variacao < 0 else "#999"

    return html.div(
        {
            "style": {
                "background": "white",
                "padding": "1.5rem",
                "borderRadius": "12px",
                "border": "1px solid #e0e0e0",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
                "transition": "transform 0.2s, box-shadow 0.2s",
                "cursor": "pointer",
            }
        },
        # Nome do fundo
        html.h3(
            {
                "style": {
                    "margin": "0 0 0.5rem 0",
                    "color": "#333",
                    "fontSize": "1.1rem",
                    "fontWeight": "600",
                }
            },
            nome
        ),
        # Tipo
        html.div(
            {
                "style": {
                    "display": "inline-block",
                    "background": AppConfig.get_color('primary'),
                    "color": "white",
                    "padding": "0.25rem 0.75rem",
                    "borderRadius": "12px",
                    "fontSize": "0.8rem",
                    "fontWeight": "600",
                    "marginBottom": "1rem",
                }
            },
            tipo
        ),
        # PL
        html.div(
            {"style": {"marginBottom": "0.5rem"}},
            html.span(
                {"style": {"color": "#666", "fontSize": "0.85rem"}},
                "PL: "
            ),
            html.span(
                {"style": {"color": "#333", "fontWeight": "600", "fontSize": "1rem"}},
                f"R$ {pl:,.2f}"
            )
        ),
        # Variação
        html.div(
            {"style": {"color": cor_variacao, "fontWeight": "600", "fontSize": "0.9rem"}},
            f"{'↑' if variacao and variacao > 0 else '↓' if variacao and variacao < 0 else '→'} {variacao:+.2f}%"
        ) if variacao is not None else None
    )


@component
def card_estatistica(label: str, valor: str, sublabel: Optional[str] = None):
    """
    Card simples para estatística

    Args:
        label: Label da estatística
        valor: Valor
        sublabel: Label secundário (opcional)
    """
    return html.div(
        {
            "style": {
                "textAlign": "center",
                "padding": "1rem",
                "background": "#f8f9fa",
                "borderRadius": "8px",
            }
        },
        html.div(
            {"style": {"fontSize": "0.85rem", "color": "#666", "marginBottom": "0.5rem"}},
            label
        ),
        html.div(
            {"style": {"fontSize": "1.8rem", "fontWeight": "700", "color": "#333"}},
            valor
        ),
        html.div(
            {"style": {"fontSize": "0.75rem", "color": "#999", "marginTop": "0.25rem"}},
            sublabel
        ) if sublabel else None
    )
