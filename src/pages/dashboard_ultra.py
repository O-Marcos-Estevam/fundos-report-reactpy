"""
Dashboard Ultra - Versão Avançada com Performance e Interatividade
Combina o melhor de dashboard.py e dashboard_modern.py com recursos avançados
"""

from __future__ import annotations

from typing import Dict, List, Optional
from datetime import datetime

from reactpy import component, html, use_state, use_effect, use_memo
from reactpy.html import make_vdom_constructor

from services.state_manager import get_state_manager
from models.fundo import FundoData
from components.charts import grafico_pizza, grafico_barras, grafico_linha
from components.advanced_components import modal
from components.filters import filter_panel, quick_filters, search_with_suggestions
from components.comparison import comparison_selector, comparison_table, comparison_charts, comparison_summary_cards
from services.export_service import get_export_service
from utils.performance import filtrar_fundos

# Criar construtor para elemento SVG
path = make_vdom_constructor("path")
svg = make_vdom_constructor("svg")


# ============================================================================
# UTILIDADES E FORMATAÇÃO
# ============================================================================

def _format_currency(valor: float) -> str:
    """Formata valor monetário com sufixos (M, B)"""
    if valor >= 1_000_000_000:
        return f"R$ {valor / 1_000_000_000:.2f}B"
    if valor >= 1_000_000:
        return f"R$ {valor / 1_000_000:.1f}M"
    if valor >= 1_000:
        return f"R$ {valor / 1_000:.1f}K"
    return f"R$ {valor:,.0f}".replace(",", ".")


def _format_percent(valor: float, decimals: int = 2) -> str:
    """Formata percentual com sinal"""
    sinal = "+" if valor > 0 else ""
    return f"{sinal}{valor:.{decimals}f}%"


def _get_trend_arrow(valor: float) -> str:
    """Retorna emoji de tendência baseado no valor"""
    if valor > 0.5:
        return "↑"
    elif valor < -0.5:
        return "↓"
    return "→"


def _get_trend_color(valor: float) -> str:
    """Retorna cor baseada na tendência"""
    if valor > 0:
        return "#10b981"  # green
    elif valor < 0:
        return "#ef4444"  # red
    return "#6b7280"  # gray


def _build_sparkline_path(values: List[float], width: int = 320, height: int = 160) -> str:
    """Constrói path SVG para sparkline"""
    if not values or len(values) < 2:
        return ""

    max_val = max(values)
    min_val = min(values)
    span = max(max_val - min_val, 1)

    step = width / (len(values) - 1)
    points = []

    for idx, value in enumerate(values):
        x = idx * step
        normalized = (value - min_val) / span
        y = height - (normalized * height)
        points.append((round(x, 2), round(y, 2)))

    path_str = " ".join(f"L{x} {y}" for x, y in points[1:])
    return f"M{points[0][0]} {points[0][1]} {path_str}"


# ============================================================================
# FUNÇÕES DE AGREGAÇÃO E CÁLCULO
# ============================================================================

def _calcular_metricas_agregadas(fundos: List[FundoData]) -> Dict:
    """Calcula métricas agregadas"""

    total_pl = sum(f.pl for f in fundos)
    total_caixa = sum(f.caixa_total for f in fundos)
    total_fundos = len(fundos)
    perc_caixa_pl = (total_caixa / total_pl * 100) if total_pl > 0 else 0

    # Calcular variações médias
    var_d1_media = sum(f.variacao_d1 for f in fundos) / total_fundos if total_fundos > 0 else 0
    var_d7_media = sum(f.variacao_d7 for f in fundos) / total_fundos if total_fundos > 0 else 0
    var_d30_media = sum(f.variacao_d30 for f in fundos) / total_fundos if total_fundos > 0 else 0

    # PLs históricos para sparkline
    total_pl_d1 = sum(f.pl_d1 for f in fundos if f.pl_d1 > 0)
    total_pl_d7 = sum(f.pl_d7 for f in fundos if f.pl_d7 > 0)
    total_pl_d30 = sum(f.pl_d30 for f in fundos if f.pl_d30 > 0)

    return {
        'total_pl': total_pl,
        'total_caixa': total_caixa,
        'total_fundos': total_fundos,
        'perc_caixa_pl': perc_caixa_pl,
        'var_d1_media': var_d1_media,
        'var_d7_media': var_d7_media,
        'var_d30_media': var_d30_media,
        'total_pl_d1': total_pl_d1,
        'total_pl_d7': total_pl_d7,
        'total_pl_d30': total_pl_d30,
    }


def _agrupar_por_tipo(fundos: List[FundoData]) -> Dict[str, List[FundoData]]:
    """Agrupa fundos por tipo"""
    fundos_por_tipo: Dict[str, List[FundoData]] = {}

    for fundo in fundos:
        tipo = fundo.tipo or "-"
        if tipo not in fundos_por_tipo:
            fundos_por_tipo[tipo] = []
        fundos_por_tipo[tipo].append(fundo)

    return fundos_por_tipo


# ============================================================================
# COMPONENTES DE UI
# ============================================================================

@component
def skeleton_card():
    """Skeleton loader para cards"""
    return html.div(
        {
            "class": "card animate-pulse",
            "style": {
                "background": "#f3f4f6",
                "borderRadius": "1rem",
                "padding": "1.5rem",
                "minHeight": "120px",
            }
        },
        html.div({
            "style": {
                "background": "#e5e7eb",
                "height": "20px",
                "borderRadius": "4px",
                "marginBottom": "1rem",
                "width": "60%"
            }
        }),
        html.div({
            "style": {
                "background": "#e5e7eb",
                "height": "32px",
                "borderRadius": "4px",
                "width": "40%"
            }
        })
    )


@component
def card_metrica_ultra(titulo: str, valor: str, variacao: Optional[float] = None,
                       sparkline_values: Optional[List[float]] = None, icone: str = "📊"):
    """Card de métrica avançado com sparkline"""

    trend_arrow = _get_trend_arrow(variacao) if variacao is not None else ""
    trend_color = _get_trend_color(variacao) if variacao is not None else "#6b7280"

    return html.div(
        {
            "class": "card animate-pop",
            "style": {
                "background": "linear-gradient(135deg, #ffffff 0%, #f9fafb 100%)",
                "borderRadius": "1rem",
                "padding": "1.5rem",
                "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                "border": "1px solid #e5e7eb",
                "transition": "all 0.3s ease",
            }
        },
        # Header
        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "0.75rem"
                }
            },
            html.span(
                {"style": {"fontSize": "0.875rem", "color": "#6b7280", "fontWeight": "500"}},
                titulo
            ),
            html.span({"style": {"fontSize": "1.5rem"}}, icone)
        ),

        # Valor principal
        html.div(
            {
                "style": {
                    "fontSize": "1.875rem",
                    "fontWeight": "700",
                    "color": "#111827",
                    "marginBottom": "0.5rem"
                }
            },
            valor
        ),

        # Variação e sparkline
        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                }
            },
            # Variação
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "0.25rem",
                        "fontSize": "0.875rem",
                        "fontWeight": "600",
                        "color": trend_color
                    }
                },
                html.span(trend_arrow),
                html.span(_format_percent(variacao) if variacao is not None else "N/A")
            ) if variacao is not None else html.div(),

            # Mini sparkline
            _render_mini_sparkline(sparkline_values) if sparkline_values else html.div()
        )
    )


def _render_mini_sparkline(values: List[float]):
    """Renderiza mini sparkline SVG"""
    if not values or len(values) < 2:
        return html.div()

    spark_path = _build_sparkline_path(values, width=60, height=20)

    return svg(
        {
            "viewBox": "0 0 60 20",
            "style": {
                "width": "60px",
                "height": "20px",
            }
        },
        path({
            "d": spark_path,
            "stroke": "#005D90",
            "strokeWidth": "2",
            "strokeLinecap": "round",
            "fill": "none"
        })
    )


# Componentes de filtro e busca movidos para components/filters.py

@component
def fund_detail_modal_ultra(fundo: Optional[FundoData], show: bool, on_close: callable):
    """Modal detalhado de informações do fundo"""

    if not show or not fundo:
        return html.div()

    return modal(
        f"📊 {fundo.nome}",  # titulo (posicional)
        show,  # show (posicional)
        on_close,  # on_close (posicional)
        html.div(  # *children começa aqui
            {"style": {"padding": "1.5rem", "overflowY": "auto"}},

            # Conteúdo do modal

            # Grid de métricas
            html.div(
                {
                    "style": {
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                        "gap": "1rem",
                        "marginBottom": "2rem"
                    }
                },
                _metric_item("Tipo", fundo.tipo),
                _metric_item("PL Atual", _format_currency(fundo.pl)),
                _metric_item("Caixa Total", _format_currency(fundo.caixa_total)),
                _metric_item("% Caixa/PL", f"{fundo.perc_caixa_pl:.2f}%"),
            ),

            # Variações
            html.h4({"style": {"marginTop": "1.5rem", "marginBottom": "1rem"}}, "📈 Variações"),
            html.div(
                {
                    "style": {
                        "display": "grid",
                        "gridTemplateColumns": "repeat(3, 1fr)",
                        "gap": "1rem",
                        "marginBottom": "2rem"
                    }
                },
                _variation_card("D-1", fundo.variacao_d1, fundo.pl_d1),
                _variation_card("D-7", fundo.variacao_d7, fundo.pl_d7),
                _variation_card("D-30", fundo.variacao_d30, fundo.pl_d30),
            ),

            # Alertas
            html.h4({"style": {"marginTop": "1.5rem", "marginBottom": "1rem"}}, "⚠️ Alertas"),
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "0.5rem"
                    }
                },
                *[
                    html.div(
                        {
                            "key": idx,
                            "style": {
                                "padding": "0.75rem",
                                "borderRadius": "0.5rem",
                                "background": "#fef3c7" if nivel == "warning" else "#fee2e2" if nivel == "error" else "#dbeafe",
                                "color": "#78350f" if nivel == "warning" else "#991b1b" if nivel == "error" else "#1e40af"
                            }
                        },
                        f"• {mensagem}"
                    )
                    for idx, (nivel, mensagem) in enumerate(fundo.get_alertas())
                ] if fundo.get_alertas() else [
                    html.div(
                        {
                            "style": {
                                "padding": "0.75rem",
                                "borderRadius": "0.5rem",
                                "background": "#d1fae5",
                                "color": "#065f46",
                                "textAlign": "center"
                            }
                        },
                        "✓ Nenhum alerta no momento"
                    )
                ]
            )
        ),
        size="large"  # Keyword argument no final
    )


def _metric_item(label: str, value: str):
    """Item de métrica para modal"""
    return html.div(
        {
            "style": {
                "background": "#f9fafb",
                "padding": "1rem",
                "borderRadius": "0.5rem"
            }
        },
        html.div(
            {"style": {"fontSize": "0.75rem", "color": "#6b7280", "marginBottom": "0.25rem"}},
            label
        ),
        html.div(
            {"style": {"fontSize": "1.125rem", "fontWeight": "600", "color": "#111827"}},
            value
        )
    )


def _variation_card(periodo: str, variacao: float, pl_anterior: float):
    """Card de variação para modal"""
    color = _get_trend_color(variacao)
    arrow = _get_trend_arrow(variacao)

    return html.div(
        {
            "style": {
                "background": "white",
                "border": f"2px solid {color}",
                "borderRadius": "0.75rem",
                "padding": "1rem",
                "textAlign": "center"
            }
        },
        html.div(
            {"style": {"fontSize": "0.875rem", "color": "#6b7280", "marginBottom": "0.5rem"}},
            periodo
        ),
        html.div(
            {
                "style": {
                    "fontSize": "1.5rem",
                    "fontWeight": "700",
                    "color": color,
                    "marginBottom": "0.25rem"
                }
            },
            f"{arrow} {_format_percent(variacao)}"
        ),
        html.div(
            {"style": {"fontSize": "0.75rem", "color": "#9ca3af"}},
            _format_currency(pl_anterior)
        )
    )


# ============================================================================
# COMPONENTE PRINCIPAL
# ============================================================================

@component
def pagina_dashboard_ultra():
    """Dashboard Ultra - Versão avançada com filtros, busca e interatividade"""

    state_manager = get_state_manager()

    # Estados locais
    refresh_key, set_refresh_key = use_state(0)
    busca, set_busca = use_state("")
    busca_sugestoes, set_busca_sugestoes = use_state([])

    # Estados de filtro avançado
    tipos_selecionados, set_tipos_selecionados = use_state([])
    var_range, set_var_range = use_state((-20.0, 20.0))
    pl_range, set_pl_range = use_state((0.0, 100_000_000_000.0))  # 100B
    apenas_alertas, set_apenas_alertas = use_state(False)
    filtro_rapido, set_filtro_rapido = use_state(None)

    # Estados de UI
    fundo_selecionado, set_fundo_selecionado = use_state(None)
    mostrar_modal, set_mostrar_modal = use_state(False)
    loading, set_loading = use_state(True)

    # Estados de comparação
    modo_comparacao, set_modo_comparacao = use_state(False)
    fundos_selecionados_comparacao, set_fundos_selecionados_comparacao = use_state([])

    # Simular loading inicial
    def init_loading():
        set_loading(False)

    use_effect(init_loading, [])

    # Função de refresh
    def atualizar_dados():
        set_refresh_key(lambda k: k + 1)

    # Funções de filtro
    def handle_tipos_change(novos_tipos):
        set_tipos_selecionados(novos_tipos)

    def handle_var_change(min_val, max_val):
        set_var_range((min_val, max_val))

    def handle_pl_change(min_val, max_val):
        set_pl_range((min_val, max_val))

    def handle_alertas_toggle():
        set_apenas_alertas(not apenas_alertas)

    def handle_clear_filters():
        set_tipos_selecionados([])
        set_var_range((-20.0, 20.0))
        set_pl_range((0.0, 100_000_000_000.0))
        set_apenas_alertas(False)
        set_filtro_rapido(None)

    # Função de busca
    def handle_busca_change(valor: str):
        set_busca(valor)

    def handle_busca_select(nome_fundo: str):
        set_busca(nome_fundo)

    # Função de click em fundo
    def handle_fundo_click(fundo: FundoData):
        set_fundo_selecionado(fundo)
        set_mostrar_modal(True)

    def handle_modal_close():
        set_mostrar_modal(False)

    # Funções de comparação
    def toggle_modo_comparacao():
        set_modo_comparacao(not modo_comparacao)
        if modo_comparacao:  # Se estava ativo, limpar seleção
            set_fundos_selecionados_comparacao([])

    def handle_comparacao_selection(fundos_ids: List[str]):
        # Pegar fundos completos baseado nos IDs
        fundos_completos = [f for f in fundos_raw if f.nome in fundos_ids]
        set_fundos_selecionados_comparacao(fundos_completos)

    # Função de exportação
    def handle_export():
        """Exporta dados filtrados para Excel"""
        export_service = get_export_service()
        try:
            # Exportar para Excel com métricas avançadas
            excel_bytes = export_service.export_to_excel(
                fundos_filtrados,
                incluir_metricas_avancadas=True,
                incluir_alertas=True
            )

            # Gerar filename
            filename = export_service.get_filename("xlsx", "dashboard_fundos")

            # Criar download (via JavaScript)
            # Nota: Em produção, usar endpoint FastAPI para download
            print(f"[INFO] Excel gerado: {filename} ({len(excel_bytes)} bytes)")

        except Exception as e:
            print(f"[ERROR] Erro ao exportar: {e}")

    # Buscar dados
    ultima_exec = state_manager.ultima_execucao

    # Empty state
    if not ultima_exec or not ultima_exec.fundos:
        return html.div(
            {
                "class": "page-section animate-fade-in",
                "style": {
                    "textAlign": "center",
                    "padding": "4rem 2rem",
                    "background": "white",
                    "borderRadius": "1rem",
                    "maxWidth": "600px",
                    "margin": "2rem auto"
                }
            },
            html.div({"style": {"fontSize": "4rem", "marginBottom": "1rem"}}, "📊"),
            html.h2(
                {"style": {"fontSize": "1.875rem", "marginBottom": "1rem", "color": "#111827"}},
                "Nenhum relatório executado"
            ),
            html.p(
                {"style": {"color": "#6b7280", "marginBottom": "2rem"}},
                "Execute um relatório para visualizar o dashboard com todos os indicadores e análises."
            ),
            html.button(
                {
                    "class": "btn-primary",
                    "onClick": lambda e: state_manager.set_pagina("executar"),
                    "style": {
                        "padding": "0.75rem 2rem",
                        "fontSize": "1rem",
                        "borderRadius": "0.5rem",
                        "border": "none",
                        "background": "#005D90",
                        "color": "white",
                        "cursor": "pointer",
                        "fontWeight": "600"
                    }
                },
                "Gerar Relatório Agora"
            )
        )

    # Processar fundos
    fundos_raw = list(ultima_exec.fundos.values())

    # Extrair tipos únicos para o filtro
    tipos_unicos = sorted(list(set(f.tipo for f in fundos_raw if f.tipo)))
    tipo_options = [
        {"label": tipo, "value": tipo, "icon": "📁"}
        for tipo in tipos_unicos
    ]

    # Gerar sugestões de busca
    if busca:
        sugestoes = [f.nome for f in fundos_raw if busca.lower() in f.nome.lower()][:10]
        if sugestoes != busca_sugestoes:
            set_busca_sugestoes(sugestoes)

    # Aplicar filtros usando a função otimizada
    fundos_filtrados = filtrar_fundos(
        fundos_raw,
        tipos=tipos_selecionados if tipos_selecionados else None,
        var_min=var_range[0] if var_range[0] > -20 else None,
        var_max=var_range[1] if var_range[1] < 20 else None,
        pl_min=pl_range[0] if pl_range[0] > 0 else None,
        pl_max=pl_range[1] if pl_range[1] < 100_000_000_000 else None,
        com_alertas=apenas_alertas if apenas_alertas else None,
        busca=busca if busca else None
    )

    # Calcular métricas
    metricas = _calcular_metricas_agregadas(fundos_raw)
    fundos_por_tipo = _agrupar_por_tipo(fundos_raw)

    # Preparar dados para sparklines
    sparkline_pl = [
        metricas['total_pl_d30'] if metricas['total_pl_d30'] > 0 else metricas['total_pl'] * 0.92,
        metricas['total_pl_d7'] if metricas['total_pl_d7'] > 0 else metricas['total_pl'] * 0.96,
        metricas['total_pl_d1'] if metricas['total_pl_d1'] > 0 else metricas['total_pl'] * 0.98,
        metricas['total_pl']
    ]

    # Top fundos
    top_fundos_pl = sorted(fundos_filtrados, key=lambda f: f.pl, reverse=True)[:6]
    top_fundos_caixa = sorted(fundos_filtrados, key=lambda f: f.caixa_total, reverse=True)[:6]

    # Dados para gráficos
    tipos = list(fundos_por_tipo.keys())
    valores_tipo = [sum(f.pl for f in fundos_por_tipo[t]) for t in tipos]

    # Loading state
    if loading:
        return html.div(
            {
                "class": "grid grid-2",
                "style": {"gap": "1.5rem", "padding": "2rem"}
            },
            *[skeleton_card() for _ in range(6)]
        )

    # Renderizar dashboard
    return html.div(
        {"class": "dashboard-ultra animate-fade-in"},

        # Modal de detalhes
        fund_detail_modal_ultra(fundo_selecionado, mostrar_modal, handle_modal_close),

        # Header com título e ações
        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "2rem"
                }
            },
            html.div(
                html.h2(
                    {"style": {"margin": "0", "fontSize": "2rem", "fontWeight": "700", "color": "#111827"}},
                    "📊 Dashboard Ultra"
                ),
                html.p(
                    {"style": {"margin": "0.5rem 0 0 0", "color": "#6b7280"}},
                    f"Última atualização: {ultima_exec.data_relatorio.strftime('%d/%m/%Y %H:%M')}"
                )
            ),
            html.div(
                {"style": {"display": "flex", "gap": "0.75rem"}},
                html.button(
                    {
                        "class": "btn btn-outline",
                        "onClick": lambda e: atualizar_dados(),
                        "style": {
                            "padding": "0.625rem 1.25rem",
                            "borderRadius": "0.5rem",
                            "border": "1px solid #d1d5db",
                            "background": "white",
                            "cursor": "pointer",
                            "fontWeight": "500"
                        }
                    },
                    "🔄 Atualizar"
                ),
                html.button(
                    {
                        "class": "btn btn-outline",
                        "onClick": lambda e: toggle_modo_comparacao(),
                        "style": {
                            "padding": "0.625rem 1.25rem",
                            "borderRadius": "0.5rem",
                            "border": "1px solid #d1d5db",
                            "background": "#FEF3C7" if modo_comparacao else "white",
                            "cursor": "pointer",
                            "fontWeight": "500"
                        }
                    },
                    "📊 Comparar" if not modo_comparacao else "✓ Modo Comparação"
                ),
                html.button(
                    {
                        "class": "btn btn-primary",
                        "onClick": lambda e: handle_export(),
                        "style": {
                            "padding": "0.625rem 1.25rem",
                            "borderRadius": "0.5rem",
                            "border": "none",
                            "background": "#005D90",
                            "color": "white",
                            "cursor": "pointer",
                            "fontWeight": "500"
                        }
                    },
                    "📥 Exportar"
                )
            )
        ),

        # Busca com autocomplete
        search_with_suggestions(
            "🔍 Buscar fundos por nome...",
            busca,
            busca_sugestoes,
            handle_busca_change,
            handle_busca_select
        ),

        # Painel de filtros avançado
        filter_panel(
            tipo_options,
            tipos_selecionados,
            var_range,
            pl_range,
            apenas_alertas,
            handle_tipos_change,
            handle_var_change,
            handle_pl_change,
            handle_alertas_toggle,
            handle_clear_filters
        ),

        # Painel de comparação (condicional)
        html.div(
            {"style": {"display": "block" if modo_comparacao else "none", "marginBottom": "2rem"}},
            html.div(
                {"class": "card animate-slide-in-up"},
                html.div(
                    {"class": "card-header"},
                    html.h3({"class": "card-title"}, "📊 Comparação de Fundos"),
                    html.p(
                        {"style": {"margin": "0.5rem 0 0 0", "color": "#6b7280", "fontSize": "0.875rem"}},
                        "Selecione até 4 fundos para comparar lado a lado"
                    )
                ),
                html.div(
                    {"style": {"padding": "1.5rem"}},
                    # Seletor de fundos
                    comparison_selector(
                        fundos_filtrados,
                        [f.nome for f in fundos_selecionados_comparacao],
                        handle_comparacao_selection
                    ),

                    # Mostrar comparação se houver fundos selecionados
                    html.div(
                        {"style": {"display": "block" if len(fundos_selecionados_comparacao) >= 2 else "none"}},

                        # Cards de resumo
                        html.div(
                            {"style": {"marginTop": "1.5rem"}},
                            comparison_summary_cards(fundos_selecionados_comparacao)
                        ) if len(fundos_selecionados_comparacao) >= 2 else html.div(),

                        # Tabela comparativa
                        html.div(
                            {"style": {"marginTop": "1.5rem"}},
                            comparison_table(fundos_selecionados_comparacao)
                        ) if len(fundos_selecionados_comparacao) >= 2 else html.div(),

                        # Gráficos de comparação
                        html.div(
                            {"style": {"marginTop": "1.5rem"}},
                            comparison_charts(fundos_selecionados_comparacao)
                        ) if len(fundos_selecionados_comparacao) >= 2 else html.div()
                    )
                )
            )
        ) if modo_comparacao else html.div(),

        # Grid de KPIs principais
        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                    "gap": "1.5rem",
                    "marginBottom": "2rem"
                }
            },
            card_metrica_ultra(
                "Patrimônio Total",
                _format_currency(metricas['total_pl']),
                metricas['var_d1_media'],
                sparkline_pl,
                "💰"
            ),
            card_metrica_ultra(
                "Caixa Total",
                _format_currency(metricas['total_caixa']),
                None,
                None,
                "🏦"
            ),
            card_metrica_ultra(
                "Total de Fundos",
                str(metricas['total_fundos']),
                None,
                None,
                "📁"
            ),
            card_metrica_ultra(
                "% Caixa/PL",
                f"{metricas['perc_caixa_pl']:.2f}%",
                None,
                None,
                "📊"
            ),
        ),

        # Gráficos principais
        html.h3(
            {"style": {"margin": "2rem 0 1.5rem 0", "fontSize": "1.5rem", "fontWeight": "600", "color": "#111827"}},
            "📈 Visualizações"
        ),

        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(500px, 1fr))",
                    "gap": "1.5rem",
                    "marginBottom": "2rem"
                }
            },
            grafico_pizza(valores_tipo, tipos, "Distribuição de PL por Tipo", 400),
            grafico_barras(
                [f.pl for f in top_fundos_pl],
                [f.nome for f in top_fundos_pl],
                "Top Fundos por Patrimônio Líquido",
                True,
                400
            ),
        ),

        # Cards de Top Fundos (clicáveis)
        html.h3(
            {"style": {"margin": "2rem 0 1.5rem 0", "fontSize": "1.5rem", "fontWeight": "600", "color": "#111827"}},
            "🏆 Destaques"
        ),

        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(300px, 1fr))",
                    "gap": "1rem",
                    "marginBottom": "2rem"
                }
            },
            *[
                html.div(
                    {
                        "key": f.nome,
                        "class": "card-clickable",
                        "onClick": lambda e, fundo=f: handle_fundo_click(fundo),
                        "style": {
                            "background": "white",
                            "borderRadius": "0.75rem",
                            "padding": "1.25rem",
                            "border": "1px solid #e5e7eb",
                            "cursor": "pointer",
                            "transition": "all 0.2s",
                            "hover": {"boxShadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)"}
                        }
                    },
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
                                {"style": {"fontSize": "0.875rem", "fontWeight": "600", "color": "#111827", "marginBottom": "0.25rem"}},
                                f.nome[:40] + ("..." if len(f.nome) > 40 else "")
                            ),
                            html.div(
                                {"style": {"fontSize": "0.75rem", "color": "#6b7280"}},
                                f.tipo
                            )
                        ),
                        html.span(
                            {
                                "style": {
                                    "fontSize": "1.25rem",
                                    "color": _get_trend_color(f.variacao_d1)
                                }
                            },
                            _get_trend_arrow(f.variacao_d1)
                        )
                    ),
                    html.div(
                        {"style": {"fontSize": "1.25rem", "fontWeight": "700", "color": "#111827", "marginBottom": "0.5rem"}},
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
                        html.span(f"Caixa: {_format_currency(f.caixa_total)}"),
                        html.span(
                            {
                                "style": {
                                    "color": _get_trend_color(f.variacao_d1),
                                    "fontWeight": "600"
                                }
                            },
                            _format_percent(f.variacao_d1)
                        )
                    )
                )
                for f in top_fundos_pl
            ]
        ),

        # Resumo mostrando contagem de fundos filtrados
        html.div(
            {
                "style": {
                    "textAlign": "center",
                    "padding": "1rem",
                    "color": "#6b7280",
                    "fontSize": "0.875rem"
                }
            },
            f"Exibindo {len(fundos_filtrados)} de {len(fundos_raw)} fundos"
        )
    )
