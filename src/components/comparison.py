"""
Componentes de Comparação
Ferramentas para comparar múltiplos fundos lado a lado
"""

from reactpy import component, html, use_state
from typing import List, Optional
from models.fundo import FundoData
from utils.analytics import calcular_metricas_fundo, get_health_score_color, get_health_score_label


def _format_currency(valor: float) -> str:
    """Formata valor monetário"""
    if valor >= 1_000_000_000:
        return f"R$ {valor / 1_000_000_000:.2f}B"
    if valor >= 1_000_000:
        return f"R$ {valor / 1_000_000:.1f}M"
    if valor >= 1_000:
        return f"R$ {valor / 1_000:.1f}K"
    return f"R$ {valor:,.0f}".replace(",", ".")


def _format_percent(valor: float) -> str:
    """Formata percentual com sinal"""
    sinal = "+" if valor > 0 else ""
    return f"{sinal}{valor:.2f}%"


def _get_winner_style(valor: float, valores: List[float], reverse: bool = False) -> dict:
    """Retorna estilo para o vencedor (maior ou menor valor)"""
    if not valores:
        return {}

    if reverse:
        is_winner = valor == min(valores)
    else:
        is_winner = valor == max(valores)

    if is_winner:
        return {
            "background": "#d1fae5",
            "color": "#065f46",
            "fontWeight": "700",
            "borderLeft": "4px solid #10b981"
        }
    return {}


@component
def comparison_selector(
    fundos_disponiveis: List[FundoData],
    fundos_selecionados: List[FundoData],
    on_selection_change: callable,
    max_fundos: int = 4
):
    """
    Seletor de fundos para comparação

    Args:
        fundos_disponiveis: Lista de todos os fundos
        fundos_selecionados: Fundos já selecionados
        on_selection_change: Callback(novos_selecionados)
        max_fundos: Máximo de fundos para comparar
    """

    def toggle_fundo(fundo: FundoData):
        """Toggle seleção de um fundo"""
        if fundo in fundos_selecionados:
            novos = [f for f in fundos_selecionados if f.nome != fundo.nome]
        else:
            if len(fundos_selecionados) < max_fundos:
                novos = fundos_selecionados + [fundo]
            else:
                return  # Já no máximo

        on_selection_change(novos)

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "1rem",
                "padding": "1.5rem",
                "marginBottom": "1.5rem",
                "border": "1px solid #e5e7eb"
            }
        },
        # Header
        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "1rem"
                }
            },
            html.h3(
                {"style": {"margin": "0", "fontSize": "1.125rem", "fontWeight": "600"}},
                "🔄 Selecione Fundos para Comparar"
            ),
            html.span(
                {
                    "style": {
                        "fontSize": "0.875rem",
                        "color": "#6b7280",
                        "padding": "0.25rem 0.75rem",
                        "background": "#f3f4f6",
                        "borderRadius": "9999px"
                    }
                },
                f"{len(fundos_selecionados)}/{max_fundos} selecionados"
            )
        ),

        # Lista de fundos
        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fill, minmax(300px, 1fr))",
                    "gap": "0.75rem",
                    "maxHeight": "400px",
                    "overflow": "auto"
                }
            },
            *[
                html.div(
                    {
                        "key": fundo.nome,
                        "onClick": lambda e, f=fundo: toggle_fundo(f),
                        "style": {
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "0.75rem",
                            "padding": "0.875rem",
                            "borderRadius": "0.5rem",
                            "border": "2px solid" + (" #1e40af" if fundo in fundos_selecionados else " #e5e7eb"),
                            "background": "#eff6ff" if fundo in fundos_selecionados else "white",
                            "cursor": "pointer" if len(fundos_selecionados) < max_fundos or fundo in fundos_selecionados else "not-allowed",
                            "opacity": "1" if len(fundos_selecionados) < max_fundos or fundo in fundos_selecionados else "0.5",
                            "transition": "all 0.2s"
                        }
                    },
                    html.input({
                        "type": "checkbox",
                        "checked": fundo in fundos_selecionados,
                        "style": {
                            "width": "1.25rem",
                            "height": "1.25rem",
                            "cursor": "pointer"
                        }
                    }),
                    html.div(
                        {"style": {"flex": "1"}},
                        html.div(
                            {"style": {"fontSize": "0.875rem", "fontWeight": "600", "marginBottom": "0.25rem"}},
                            fundo.nome[:40] + ("..." if len(fundo.nome) > 40 else "")
                        ),
                        html.div(
                            {"style": {"fontSize": "0.75rem", "color": "#6b7280"}},
                            f"{fundo.tipo} • {_format_currency(fundo.pl)}"
                        )
                    )
                )
                for fundo in sorted(fundos_disponiveis, key=lambda f: f.pl, reverse=True)[:50]  # Top 50
            ]
        )
    )


@component
def comparison_table(fundos: List[FundoData]):
    """
    Tabela de comparação lado a lado

    Args:
        fundos: Lista de fundos para comparar (max 4)
    """
    if not fundos:
        return html.div(
            {
                "style": {
                    "textAlign": "center",
                    "padding": "4rem 2rem",
                    "color": "#9ca3af"
                }
            },
            html.div({"style": {"fontSize": "3rem", "marginBottom": "1rem"}}, "📊"),
            html.h3("Selecione fundos para comparar"),
            html.p("Escolha até 4 fundos para análise lado a lado")
        )

    # Calcular métricas para todos os fundos
    metricas_fundos = [calcular_metricas_fundo(f) for f in fundos]

    # Preparar dados para comparação
    rows = [
        ("📁 Tipo", [f.tipo for f in fundos], False, None),
        ("💰 Patrimônio Líquido", [f.pl for f in fundos], False, _format_currency),
        ("🏦 Caixa Total", [f.caixa_total for f in fundos], False, _format_currency),
        ("📊 % Caixa/PL", [f.perc_caixa_pl for f in fundos], False, lambda v: f"{v:.2f}%"),
        ("📈 Variação D-1", [f.variacao_d1 for f in fundos], False, _format_percent),
        ("📈 Variação D-7", [f.variacao_d7 for f in fundos], False, _format_percent),
        ("📈 Variação D-30", [f.variacao_d30 for f in fundos], False, _format_percent),
        ("⚡ Sharpe Ratio", [m['sharpe_ratio'] for m in metricas_fundos], False, lambda v: f"{v:.2f}"),
        ("📉 Volatilidade", [m['volatilidade'] for m in metricas_fundos], True, lambda v: f"{v:.2f}%"),
        ("📊 Sortino Ratio", [m['sortino_ratio'] for m in metricas_fundos], False, lambda v: f"{v:.2f}"),
        ("⬇️ Max Drawdown", [m['max_drawdown'] for m in metricas_fundos], True, lambda v: f"{v:.2f}%"),
        ("⚠️ VaR 95%", [m['var_95'] for m in metricas_fundos], True, lambda v: f"{v:.2f}%"),
        ("🎯 CVaR 95%", [m['cvar_95'] for m in metricas_fundos], True, lambda v: f"{v:.2f}%"),
    ]

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "1rem",
                "padding": "1.5rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
                "border": "1px solid #e5e7eb",
                "overflow": "auto"
            }
        },
        html.h3(
            {"style": {"margin": "0 0 1.5rem 0", "fontSize": "1.25rem", "fontWeight": "600"}},
            "📊 Comparação Detalhada"
        ),

        # Tabela
        html.table(
            {"style": {"width": "100%", "borderCollapse": "collapse"}},
            # Header
            html.thead(
                html.tr(
                    {"style": {"borderBottom": "2px solid #e5e7eb"}},
                    html.th(
                        {
                            "style": {
                                "padding": "1rem",
                                "textAlign": "left",
                                "fontWeight": "600",
                                "color": "#374151",
                                "position": "sticky",
                                "left": "0",
                                "background": "white",
                                "zIndex": "10"
                            }
                        },
                        "Métrica"
                    ),
                    *[
                        html.th(
                            {
                                "key": f.nome,
                                "style": {
                                    "padding": "1rem",
                                    "textAlign": "center",
                                    "fontWeight": "600",
                                    "color": "#374151",
                                    "minWidth": "200px"
                                }
                            },
                            html.div(
                                html.div(
                                    {"style": {"fontSize": "0.875rem", "marginBottom": "0.25rem"}},
                                    f.nome[:30] + ("..." if len(f.nome) > 30 else "")
                                ),
                                html.div(
                                    {"style": {"fontSize": "0.75rem", "color": "#9ca3af", "fontWeight": "400"}},
                                    f.tipo
                                )
                            )
                        )
                        for f in fundos
                    ]
                )
            ),
            # Body
            html.tbody(
                *[
                    html.tr(
                        {
                            "key": label,
                            "style": {"borderBottom": "1px solid #f3f4f6"}
                        },
                        html.td(
                            {
                                "style": {
                                    "padding": "1rem",
                                    "fontWeight": "500",
                                    "color": "#6b7280",
                                    "position": "sticky",
                                    "left": "0",
                                    "background": "white",
                                    "zIndex": "5"
                                }
                            },
                            label
                        ),
                        *[
                            html.td(
                                {
                                    "key": f"{label}-{i}",
                                    "style": {
                                        "padding": "1rem",
                                        "textAlign": "center",
                                        **(_get_winner_style(valores[i], valores, reverse) if isinstance(valores[i], (int, float)) and formatter else {})
                                    }
                                },
                                formatter(valores[i]) if formatter and valores[i] is not None else str(valores[i])
                            )
                            for i in range(len(fundos))
                        ]
                    )
                    for label, valores, reverse, formatter in rows
                ]
            )
        ),

        # Legenda
        html.div(
            {
                "style": {
                    "marginTop": "1rem",
                    "padding": "0.75rem",
                    "background": "#f9fafb",
                    "borderRadius": "0.5rem",
                    "fontSize": "0.75rem",
                    "color": "#6b7280"
                }
            },
            html.span({"style": {"marginRight": "1rem"}}, "💡 Dica:"),
            html.span("Células destacadas indicam o melhor valor em cada métrica")
        )
    )


@component
def comparison_charts(fundos: List[FundoData]):
    """
    Gráficos de comparação

    Args:
        fundos: Lista de fundos para comparar
    """
    from components.charts_advanced import grafico_evolucao_temporal

    if not fundos:
        return html.div()

    return html.div(
        {
            "style": {
                "display": "grid",
                "gridTemplateColumns": "1fr",
                "gap": "1.5rem",
                "marginTop": "1.5rem"
            }
        },
        grafico_evolucao_temporal(
            fundos,
            "Evolução Comparativa do Patrimônio Líquido",
            500,
            True
        )
    )


@component
def comparison_summary_cards(fundos: List[FundoData]):
    """
    Cards resumo para comparação rápida

    Args:
        fundos: Lista de fundos para comparar
    """
    if not fundos:
        return html.div()

    from utils.analytics import calcular_health_score, get_health_score_label, get_health_score_color

    return html.div(
        {
            "style": {
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                "gap": "1rem",
                "marginBottom": "1.5rem"
            }
        },
        *[
            html.div(
                {
                    "key": f.nome,
                    "style": {
                        "background": "white",
                        "borderRadius": "0.75rem",
                        "padding": "1.25rem",
                        "border": "2px solid #e5e7eb",
                        "transition": "all 0.2s"
                    }
                },
                # Header
                html.div(
                    {
                        "style": {
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "start",
                            "marginBottom": "0.75rem"
                        }
                    },
                    html.div(
                        html.div(
                            {"style": {"fontSize": "0.875rem", "fontWeight": "600", "marginBottom": "0.25rem"}},
                            f.nome[:30] + ("..." if len(f.nome) > 30 else "")
                        ),
                        html.div(
                            {"style": {"fontSize": "0.75rem", "color": "#9ca3af"}},
                            f.tipo
                        )
                    ),
                    html.div(
                        {
                            "style": {
                                "padding": "0.25rem 0.625rem",
                                "borderRadius": "9999px",
                                "fontSize": "0.75rem",
                                "fontWeight": "600",
                                "background": get_health_score_color(calcular_health_score(f)) + "22",
                                "color": get_health_score_color(calcular_health_score(f))
                            }
                        },
                        get_health_score_label(calcular_health_score(f))
                    )
                ),
                # Métricas principais
                html.div(
                    {"style": {"fontSize": "1.5rem", "fontWeight": "700", "marginBottom": "0.5rem"}},
                    _format_currency(f.pl)
                ),
                html.div(
                    {
                        "style": {
                            "display": "flex",
                            "justifyContent": "space-between",
                            "fontSize": "0.75rem",
                            "color": "#6b7280"
                        }
                    },
                    html.span(f"Caixa: {f.perc_caixa_pl:.1f}%"),
                    html.span(
                        {
                            "style": {
                                "color": "#10b981" if f.variacao_d1 > 0 else "#ef4444" if f.variacao_d1 < 0 else "#6b7280",
                                "fontWeight": "600"
                            }
                        },
                        _format_percent(f.variacao_d1)
                    )
                )
            )
            for f in fundos
        ]
    )
