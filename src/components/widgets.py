"""
Widgets Modulares para Dashboard
Sistema de widgets reutilizáveis e customizáveis
"""

from typing import List, Dict, Any, Optional, Callable
from reactpy import component, html, use_state

from models.fundo import FundoData
from components.charts import grafico_pizza, grafico_barras, grafico_linha
from utils.analytics import calcular_health_score, calcular_metricas_fundo


# ============================================================================
# WIDGET BASE
# ============================================================================

@component
def widget_container(
    titulo: str,
    icone: str = "📊",
    children: Any = None,
    acoes: Optional[List[Dict[str, Any]]] = None,
    tamanho: str = "medium",  # small, medium, large, xlarge
    collapsible: bool = False
):
    """
    Container base para widgets

    Args:
        titulo: Título do widget
        icone: Emoji ou ícone
        children: Conteúdo do widget
        acoes: Lista de ações (botões) no header
        tamanho: Tamanho do widget (small, medium, large, xlarge)
        collapsible: Se pode ser recolhido
    """
    is_collapsed, set_is_collapsed = use_state(False)

    # Mapeamento de tamanhos
    size_map = {
        "small": "minmax(300px, 1fr)",
        "medium": "minmax(400px, 1fr)",
        "large": "minmax(600px, 1fr)",
        "xlarge": "minmax(800px, 1fr)"
    }

    def toggle_collapse():
        set_is_collapsed(not is_collapsed)

    return html.div(
        {
            "class": "widget-container card animate-pop",
            "data-size": tamanho,
            "style": {
                "gridColumn": "span 1",
                "minWidth": "300px"
            }
        },
        # Header
        html.div(
            {
                "class": "card-header",
                "style": {
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center"
                }
            },
            html.div(
                {"style": {"display": "flex", "alignItems": "center", "gap": "0.5rem"}},
                html.span({"style": {"fontSize": "1.25rem"}}, icone),
                html.h3({"class": "card-title"}, titulo)
            ),
            html.div(
                {"style": {"display": "flex", "gap": "0.5rem"}},
                # Ações customizadas
                *[
                    html.button(
                        {
                            "onClick": acao.get("onClick"),
                            "class": "btn-icon",
                            "title": acao.get("title", ""),
                            "style": {
                                "padding": "0.25rem 0.5rem",
                                "border": "none",
                                "background": "transparent",
                                "cursor": "pointer",
                                "fontSize": "1rem"
                            }
                        },
                        acao.get("icon", "⚙️")
                    )
                    for acao in (acoes or [])
                ],
                # Botão de colapsar
                html.button(
                    {
                        "onClick": lambda e: toggle_collapse(),
                        "class": "btn-icon",
                        "style": {
                            "padding": "0.25rem 0.5rem",
                            "border": "none",
                            "background": "transparent",
                            "cursor": "pointer",
                            "fontSize": "1rem",
                            "display": "block" if collapsible else "none"
                        }
                    },
                    "▼" if not is_collapsed else "▶"
                ) if collapsible else html.div()
            )
        ),
        # Conteúdo
        html.div(
            {
                "class": "card-body",
                "style": {
                    "display": "none" if is_collapsed else "block",
                    "padding": "1.5rem"
                }
            },
            children
        )
    )


# ============================================================================
# WIDGET: KPI CARD
# ============================================================================

@component
def widget_kpi(
    titulo: str,
    valor: str,
    icone: str = "📊",
    variacao: Optional[float] = None,
    tamanho: str = "small",
    on_click: Optional[Callable] = None
):
    """Widget de KPI simples"""

    trend_color = "#10b981" if (variacao or 0) > 0 else "#ef4444" if (variacao or 0) < 0 else "#6b7280"
    trend_arrow = "↑" if (variacao or 0) > 0 else "↓" if (variacao or 0) < 0 else "→"

    return widget_container(
        titulo=titulo,
        icone=icone,
        tamanho=tamanho,
        children=html.div(
            {
                "onClick": on_click if on_click else None,
                "style": {
                    "cursor": "pointer" if on_click else "default",
                    "textAlign": "center"
                }
            },
            html.div(
                {"style": {"fontSize": "2rem", "fontWeight": "700", "marginBottom": "0.5rem"}},
                valor
            ),
            html.div(
                {
                    "style": {
                        "fontSize": "1.25rem",
                        "color": trend_color,
                        "display": "block" if variacao is not None else "none"
                    }
                },
                f"{trend_arrow} {variacao:+.2f}%" if variacao is not None else ""
            ) if variacao is not None else html.div()
        )
    )


# ============================================================================
# WIDGET: LISTA DE ALERTAS
# ============================================================================

@component
def widget_alertas(fundos: List[FundoData], limite: int = 5, tamanho: str = "medium"):
    """Widget de lista de alertas"""

    # Coletar todos os alertas
    todos_alertas = []
    for fundo in fundos:
        if fundo.tem_alertas():
            alertas = fundo.get_alertas()
            for nivel, mensagem in alertas:
                todos_alertas.append({
                    "fundo": fundo.nome,
                    "nivel": nivel,
                    "mensagem": mensagem
                })

    # Limitar quantidade
    alertas_exibir = todos_alertas[:limite]

    # Mapa de cores
    color_map = {
        "error": {"bg": "#fef2f2", "text": "#991b1b", "icon": "🔴"},
        "warning": {"bg": "#fffbeb", "text": "#92400e", "icon": "⚠️"},
        "info": {"bg": "#eff6ff", "text": "#1e40af", "icon": "ℹ️"}
    }

    return widget_container(
        titulo="Alertas Recentes",
        icone="🚨",
        tamanho=tamanho,
        collapsible=True,
        children=html.div(
            {"style": {"display": "flex", "flexDirection": "column", "gap": "0.75rem"}},

            # Mostrar alertas
            *[
                html.div(
                    {
                        "style": {
                            "padding": "0.75rem",
                            "borderRadius": "0.5rem",
                            "background": color_map.get(alerta["nivel"], color_map["info"])["bg"],
                            "borderLeft": f"4px solid {color_map.get(alerta['nivel'], color_map['info'])['text']}"
                        }
                    },
                    html.div(
                        {"style": {"display": "flex", "alignItems": "flex-start", "gap": "0.5rem"}},
                        html.span(
                            {"style": {"fontSize": "1rem"}},
                            color_map.get(alerta["nivel"], color_map["info"])["icon"]
                        ),
                        html.div(
                            {"style": {"flex": "1"}},
                            html.div(
                                {"style": {"fontWeight": "600", "marginBottom": "0.25rem", "fontSize": "0.875rem"}},
                                alerta["fundo"]
                            ),
                            html.div(
                                {"style": {"fontSize": "0.875rem", "color": "#374151"}},
                                alerta["mensagem"]
                            )
                        )
                    )
                )
                for alerta in alertas_exibir
            ] if alertas_exibir else [
                html.div(
                    {
                        "style": {
                            "textAlign": "center",
                            "padding": "2rem",
                            "color": "#9ca3af"
                        }
                    },
                    html.div({"style": {"fontSize": "2rem", "marginBottom": "0.5rem"}}, "✓"),
                    html.div("Nenhum alerta no momento")
                )
            ],

            # Ver todos
            html.div(
                {
                    "style": {
                        "textAlign": "center",
                        "marginTop": "0.5rem",
                        "display": "block" if len(todos_alertas) > limite else "none"
                    }
                },
                html.a(
                    {
                        "href": "#",
                        "style": {
                            "color": "#005D90",
                            "fontSize": "0.875rem",
                            "textDecoration": "none",
                            "fontWeight": "500"
                        }
                    },
                    f"Ver todos ({len(todos_alertas)} alertas)"
                )
            )
        )
    )


# ============================================================================
# WIDGET: TOP FUNDOS
# ============================================================================

@component
def widget_top_fundos(
    fundos: List[FundoData],
    criterio: str = "pl",  # pl, caixa, variacao_d1
    limite: int = 5,
    tamanho: str = "medium",
    on_fund_click: Optional[Callable] = None
):
    """Widget de top fundos por critério"""

    # Mapear critérios
    criterio_map = {
        "pl": {"label": "Patrimônio Líquido", "key": lambda f: f.pl, "format": lambda v: f"R$ {v/1_000_000_000:.2f}B"},
        "caixa": {"label": "Caixa Total", "key": lambda f: f.caixa_total, "format": lambda v: f"R$ {v/1_000_000_000:.2f}B"},
        "variacao_d1": {"label": "Variação D-1", "key": lambda f: f.variacao_d1, "format": lambda v: f"{v:+.2f}%"}
    }

    config = criterio_map.get(criterio, criterio_map["pl"])
    fundos_ordenados = sorted(fundos, key=config["key"], reverse=True)[:limite]

    return widget_container(
        titulo=f"Top {limite} - {config['label']}",
        icone="🏆",
        tamanho=tamanho,
        collapsible=True,
        children=html.div(
            {"style": {"display": "flex", "flexDirection": "column", "gap": "0.75rem"}},

            *[
                html.div(
                    {
                        "onClick": lambda e, f=fundo: on_fund_click(f) if on_fund_click else None,
                        "style": {
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "center",
                            "padding": "0.75rem",
                            "borderRadius": "0.5rem",
                            "background": "#f9fafb",
                            "cursor": "pointer" if on_fund_click else "default",
                            "transition": "all 0.2s"
                        },
                        "onMouseEnter": lambda e: e["currentTarget"].update({"style": {**e["currentTarget"]["style"], "background": "#f3f4f6"}}) if on_fund_click else None,
                        "onMouseLeave": lambda e: e["currentTarget"].update({"style": {**e["currentTarget"]["style"], "background": "#f9fafb"}}) if on_fund_click else None
                    },
                    html.div(
                        {"style": {"display": "flex", "alignItems": "center", "gap": "0.75rem"}},
                        html.div(
                            {
                                "style": {
                                    "width": "2rem",
                                    "height": "2rem",
                                    "borderRadius": "50%",
                                    "background": "#005D90" if idx == 0 else "#10b981" if idx == 1 else "#f59e0b" if idx == 2 else "#6b7280",
                                    "color": "white",
                                    "display": "flex",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "fontWeight": "700",
                                    "fontSize": "0.875rem"
                                }
                            },
                            str(idx + 1)
                        ),
                        html.div(
                            {"style": {"flex": "1"}},
                            html.div(
                                {"style": {"fontWeight": "600", "fontSize": "0.875rem", "marginBottom": "0.125rem"}},
                                fundo.nome[:40] + "..." if len(fundo.nome) > 40 else fundo.nome
                            ),
                            html.div(
                                {"style": {"fontSize": "0.75rem", "color": "#6b7280"}},
                                fundo.tipo
                            )
                        )
                    ),
                    html.div(
                        {"style": {"fontWeight": "700", "fontSize": "0.875rem"}},
                        config["format"](config["key"](fundo))
                    )
                )
                for idx, fundo in enumerate(fundos_ordenados)
            ]
        )
    )


# ============================================================================
# WIDGET: GRÁFICO PIZZA
# ============================================================================

@component
def widget_grafico_pizza(
    fundos: List[FundoData],
    agrupar_por: str = "tipo",  # tipo
    titulo: str = "Distribuição por Tipo",
    tamanho: str = "medium"
):
    """Widget de gráfico de pizza"""

    # Agrupar fundos
    if agrupar_por == "tipo":
        grupos = {}
        for fundo in fundos:
            tipo = fundo.tipo or "Outros"
            if tipo not in grupos:
                grupos[tipo] = 0
            grupos[tipo] += fundo.pl

        labels = list(grupos.keys())
        valores = list(grupos.values())
    else:
        labels = []
        valores = []

    return widget_container(
        titulo=titulo,
        icone="📊",
        tamanho=tamanho,
        collapsible=True,
        children=html.div(
            grafico_pizza(valores, labels, titulo, altura=350)
        )
    )


# ============================================================================
# WIDGET: GRÁFICO DE BARRAS
# ============================================================================

@component
def widget_grafico_barras(
    fundos: List[FundoData],
    criterio: str = "pl",
    limite: int = 10,
    titulo: str = "Top Fundos",
    tamanho: str = "large"
):
    """Widget de gráfico de barras"""

    criterio_map = {
        "pl": lambda f: f.pl,
        "caixa": lambda f: f.caixa_total,
        "variacao_d1": lambda f: f.variacao_d1
    }

    key_func = criterio_map.get(criterio, criterio_map["pl"])
    fundos_ordenados = sorted(fundos, key=key_func, reverse=True)[:limite]

    valores = [key_func(f) for f in fundos_ordenados]
    labels = [f.nome[:30] + "..." if len(f.nome) > 30 else f.nome for f in fundos_ordenados]

    return widget_container(
        titulo=titulo,
        icone="📊",
        tamanho=tamanho,
        collapsible=True,
        children=html.div(
            grafico_barras(valores, labels, titulo, horizontal=True, altura=400)
        )
    )


# ============================================================================
# WIDGET: HEALTH SCORE
# ============================================================================

@component
def widget_health_score(
    fundos: List[FundoData],
    limite: int = 5,
    ordem: str = "desc",  # desc (melhores) ou asc (piores)
    tamanho: str = "medium"
):
    """Widget de health score dos fundos"""

    # Calcular health scores
    fundos_com_score = []
    for fundo in fundos:
        score = calcular_health_score(fundo)
        fundos_com_score.append((fundo, score))

    # Ordenar
    reverse = (ordem == "desc")
    fundos_ordenados = sorted(fundos_com_score, key=lambda x: x[1], reverse=reverse)[:limite]

    titulo = f"Top {limite} Fundos Saudáveis" if ordem == "desc" else f"Top {limite} Fundos em Alerta"

    return widget_container(
        titulo=titulo,
        icone="💚" if ordem == "desc" else "⚠️",
        tamanho=tamanho,
        collapsible=True,
        children=html.div(
            {"style": {"display": "flex", "flexDirection": "column", "gap": "1rem"}},

            *[
                html.div(
                    {"style": {"display": "flex", "flexDirection": "column", "gap": "0.5rem"}},
                    html.div(
                        {"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center"}},
                        html.div(
                            {"style": {"fontWeight": "600", "fontSize": "0.875rem"}},
                            fundo.nome[:35] + "..." if len(fundo.nome) > 35 else fundo.nome
                        ),
                        html.div(
                            {
                                "style": {
                                    "fontWeight": "700",
                                    "fontSize": "1rem",
                                    "color": "#10b981" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
                                }
                            },
                            f"{score:.0f}"
                        )
                    ),
                    # Barra de progresso
                    html.div(
                        {
                            "style": {
                                "width": "100%",
                                "height": "0.5rem",
                                "background": "#e5e7eb",
                                "borderRadius": "0.25rem",
                                "overflow": "hidden"
                            }
                        },
                        html.div(
                            {
                                "style": {
                                    "width": f"{score}%",
                                    "height": "100%",
                                    "background": "#10b981" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444",
                                    "transition": "width 0.3s ease"
                                }
                            }
                        )
                    )
                )
                for fundo, score in fundos_ordenados
            ]
        )
    )


# ============================================================================
# WIDGET: RESUMO EXECUTIVO
# ============================================================================

@component
def widget_resumo_executivo(fundos: List[FundoData], tamanho: str = "xlarge"):
    """Widget de resumo executivo com métricas principais"""

    total_pl = sum(f.pl for f in fundos)
    total_caixa = sum(f.caixa_total for f in fundos)
    total_fundos = len(fundos)
    perc_caixa_pl = (total_caixa / total_pl * 100) if total_pl > 0 else 0

    # Variação média
    var_d1_media = sum(f.variacao_d1 for f in fundos if f.variacao_d1) / len([f for f in fundos if f.variacao_d1]) if fundos else 0

    return widget_container(
        titulo="Resumo Executivo",
        icone="📈",
        tamanho=tamanho,
        children=html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                    "gap": "1.5rem"
                }
            },
            # Card 1: PL Total
            _metric_card("Patrimônio Total", f"R$ {total_pl/1_000_000_000:.2f}B", "💰", var_d1_media),
            # Card 2: Caixa Total
            _metric_card("Caixa Total", f"R$ {total_caixa/1_000_000_000:.2f}B", "🏦", None),
            # Card 3: Total Fundos
            _metric_card("Total de Fundos", str(total_fundos), "📁", None),
            # Card 4: % Caixa/PL
            _metric_card("% Caixa/PL", f"{perc_caixa_pl:.2f}%", "📊", None)
        )
    )


def _metric_card(label: str, valor: str, icone: str, variacao: Optional[float]):
    """Card de métrica interna"""
    trend_color = "#10b981" if (variacao or 0) > 0 else "#ef4444" if (variacao or 0) < 0 else "#6b7280"
    trend_arrow = "↑" if (variacao or 0) > 0 else "↓" if (variacao or 0) < 0 else "→"

    return html.div(
        {
            "style": {
                "padding": "1.5rem",
                "background": "#f9fafb",
                "borderRadius": "0.75rem",
                "textAlign": "center"
            }
        },
        html.div({"style": {"fontSize": "2rem", "marginBottom": "0.5rem"}}, icone),
        html.div(
            {"style": {"fontSize": "0.875rem", "color": "#6b7280", "marginBottom": "0.5rem"}},
            label
        ),
        html.div(
            {"style": {"fontSize": "1.75rem", "fontWeight": "700", "marginBottom": "0.25rem"}},
            valor
        ),
        html.div(
            {
                "style": {
                    "fontSize": "1rem",
                    "color": trend_color,
                    "display": "block" if variacao is not None else "none"
                }
            },
            f"{trend_arrow} {variacao:+.2f}%" if variacao is not None else ""
        ) if variacao is not None else html.div()
    )
