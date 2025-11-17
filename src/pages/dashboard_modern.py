"""
Dashboard V2 inspirado em layout premium
"""

from __future__ import annotations

from typing import Dict, List

from reactpy import component, html
from reactpy.html import make_vdom_constructor

from services.state_manager import get_state_manager
from models.fundo import FundoData

# Criar construtor para elemento SVG path
path = make_vdom_constructor("path")


def _format_currency(valor: float) -> str:
    if valor >= 1_000_000_000:
        return f"R$ {valor / 1_000_000_000:.2f}B"
    if valor >= 1_000_000:
        return f"R$ {valor / 1_000_000:.1f}M"
    return f"R$ {valor:,.0f}".replace(",", ".")


def _build_sparkline_path(values: List[float], width: int = 320, height: int = 160) -> str:
    if not values:
        return ""

    max_val = max(values)
    min_val = min(values)
    span = max(max_val - min_val, 1)

    step = width / (len(values) - 1 or 1)
    points = []

    for idx, value in enumerate(values):
        x = idx * step
        normalized = (value - min_val) / span
        y = height - (normalized * height)
        points.append((round(x, 2), round(y, 2)))

    path = " ".join(f"L{x} {y}" for x, y in points[1:])
    return f"M{points[0][0]} {points[0][1]} {path}"


def _empty_state(on_change):
    return html.div(
        {"class": "page-section animate-fade-in", "style": {"textAlign": "center"}},
        html.span({"class": "pill pill-orange"}, "Nenhum relatório executado"),
        html.h2(
            {"style": {"margin": "1.5rem 0 0.5rem", "fontSize": "1.75rem"}},
            "Execute o primeiro relatório"
        ),
        html.p(
            {"class": "text-muted", "style": {"marginBottom": "2rem"}},
            "Quando o relatório terminar, o dashboard mostrará os indicadores automaticamente."
        ),
        html.button(
            {
                "class": "btn-primary",
                "onClick": lambda e: on_change("executar")
            },
            "Gerar Relatório Agora"
        )
    )


@component
def pagina_dashboard_moderna():
    """Nova versão do dashboard com tema azul"""
    from reactpy import use_state

    state_manager = get_state_manager()

    # Usar use_state para forçar re-render quando dados mudarem
    refresh_key, set_refresh_key = use_state(0)

    def atualizar_dados():
        """Força atualização dos dados"""
        set_refresh_key(lambda k: k + 1)

    # Buscar dados atualizados do state manager
    ultima_exec = state_manager.ultima_execucao

    if not ultima_exec or not ultima_exec.fundos:
        return _empty_state(state_manager.set_pagina)

    fundos = list(ultima_exec.fundos.values())
    total_pl = sum(f.pl for f in fundos)
    total_caixa = sum(f.caixa_total for f in fundos)
    total_fundos = len(fundos)
    perc_caixa_pl = (total_caixa / total_pl * 100) if total_pl else 0

    fundos_por_tipo: Dict[str, List[FundoData]] = {}
    for fundo in fundos:
        fundos_por_tipo.setdefault(fundo.tipo or "-", []).append(fundo)

    top_fundos = sorted(fundos, key=lambda f: f.pl, reverse=True)[:4]
    top_caixa = sorted(fundos, key=lambda f: f.caixa_total, reverse=True)[:4]

    spark_values = [
        total_pl * fator for fator in [0.86, 0.88, 0.9, 0.95, 1.02, 1.05, 1.08]
    ]
    spark_path = _build_sparkline_path(spark_values)

    return html.div(
        {"class": "grid grid-2 animate-fade-in", "style": {"gap": "2.2rem"}},
        html.div(
            {"class": "card animate-pop", "style": {"gridColumn": "1 / 3"}},
            html.div(
                {"class": "card-header"},
                html.div(
                    {"style": {"display": "flex", "flexDirection": "column", "gap": "0.4rem"}},
                    html.span({"class": "pill"}, "Report · Hoje"),
                    html.h3({"class": "card-title", "style": {"fontSize": "1.45rem"}}, "Resumo Financeiro")
                ),
                html.div(
                    {"style": {"display": "flex", "gap": "0.5rem"}},
                    html.button(
                        {
                            "class": "btn btn-outline btn-sm",
                            "onClick": lambda e: atualizar_dados(),
                            "title": "Atualizar dados"
                        },
                        "🔄 Atualizar"
                    ),
                    html.button({"class": "btn btn-secondary btn-sm"}, "Exportar")
                )
            ),
            html.div(
                {"style": {"display": "grid", "gridTemplateColumns": "repeat(2, minmax(0, 1fr))", "gap": "1.75rem"}},
                html.div(
                    {"style": {"display": "flex", "flexDirection": "column", "gap": "1.2rem"}},
                    html.div(
                        {"style": {"display": "flex", "alignItems": "center", "gap": "1.5rem"}},
                        html.div(
                            {"style": {"display": "flex", "flexDirection": "column", "gap": "0.35rem"}},
                            html.span({"class": "text-muted"}, "Patrimônio total"),
                            html.span({"class": "metric-value"}, _format_currency(total_pl)),
                            html.span({"class": "badge-soft"}, ["⬆", " +5.2% versus período anterior"])
                        )
                    ),
                    html.div(
                        {"class": "mini-chart"},
                        html.svg(
                            {
                                "viewBox": "0 0 320 160",
                                "fill": "none",
                                "xmlns": "http://www.w3.org/2000/svg",
                            },
                            path({
                                "d": spark_path,
                                "stroke": "#005D90",
                                "stroke_width": "4",
                                "stroke_linecap": "round",
                                "stroke_linejoin": "round",
                                "fill": "transparent"
                            }),
                            path({
                                "d": f"{spark_path} L320 160 L0 160 Z",
                                "fill": "rgba(0, 93, 144, 0.12)"
                            })
                        )
                    )
                ),
                html.div(
                    {
                        "style": {
                            "background": "linear-gradient(145deg, rgba(0, 93, 144, 0.12), rgba(19, 115, 183, 0.18))",
                            "borderRadius": "18px",
                            "padding": "2rem",
                            "display": "flex",
                            "flexDirection": "column",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "gap": "1.25rem",
                            "boxShadow": "inset 0 16px 40px -32px rgba(0, 93, 144, 0.55)"
                        }
                    },
                    html.div({"class": "progress-circle"}, html.span(f"{perc_caixa_pl:.0f}%")),
                    html.div(
                        {"style": {"textAlign": "center"}},
                        html.h4({"style": {"margin": "0 0 0.4rem", "fontSize": "1rem"}}, "Meta de Caixa / PL"),
                        html.p({"class": "text-muted"}, "Nível saudável mantendo liquidez prevista")
                    )
                )
            )
        ),
        html.div(
            {"class": "card animate-pop"},
            html.div({"class": "card-header"},
                html.h3({"class": "card-title"}, "Caixa disponível"),
                html.span({"class": "badge-soft"}, _format_currency(total_caixa))
            ),
            html.p({"class": "text-muted"}, "Distribuição entre os fundos com maior caixa disponível."),
            html.div(
                {"class": "table-list"},
                *[
                    html.div(
                        {"class": "table-row"},
                        html.span(f"{idx+1}. {fundo.nome}"),
                        html.span(_format_currency(fundo.caixa_total))
                    )
                    for idx, fundo in enumerate(top_caixa)
                ]
            )
        ),
        html.div(
            {"class": "card animate-pop"},
            html.div({"class": "card-header"},
                html.h3({"class": "card-title"}, "Fundos em destaque"),
                html.span({"class": "badge-soft pill-green"}, ["⬆", " performance positiva"])
            ),
            html.div(
                {"class": "table-list"},
                *[
                    html.div(
                        {"class": "table-row"},
                        html.span(f"{f.nome}"),
                        html.span(_format_currency(f.pl))
                    )
                    for f in top_fundos
                ]
            )
        ),
        html.div(
            {"class": "card animate-pop"},
            html.div(
                {"class": "card-header"},
                html.h3({"class": "card-title"}, "Resumo por tipo"),
                html.span({"class": "badge-soft pill-purple"}, f"{len(fundos_por_tipo)} categorias")
            ),
            html.div(
                {"class": "table-list"},
                *[
                    html.div(
                        {"class": "table-row"},
                        html.span(tipo),
                        html.span(_format_currency(sum(f.pl for f in lista)))
                    )
                    for tipo, lista in sorted(fundos_por_tipo.items(), key=lambda item: sum(f.pl for f in item[1]), reverse=True)
                ]
            )
        ),
        html.div(
            {"class": "card animate-pop", "style": {"gridColumn": "1 / 3"}},
            html.div(
                {"class": "card-header"},
                html.div(
                    {"style": {"display": "flex", "flexDirection": "column", "gap": "0.35rem"}},
                    html.h3({"class": "card-title"}, "Alertas & recomendações"),
                    html.span({"class": "text-muted"}, "Analise pontos de atenção antes da abertura do mercado")
                ),
                html.span({"class": "badge-soft pill-orange"}, f"{len([f for f in fundos if f.tem_alertas()])} fundos monitorados")
            ),
            html.div(
                {"class": "chip-list"},
                *[
                    html.span({"class": "chip-item"}, alerta[1])
                    for fundo in fundos
                    for alerta in fundo.get_alertas()
                ][:12] or [html.span({"class": "chip-item"}, "Sem alertas críticos no momento")]
            )
        )
    )
