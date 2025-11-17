"""
Página de Histórico Moderna
Histórico de execuções com componentes modernos, timeline e filtros
"""

from reactpy import component, html, use_state
from datetime import datetime, timedelta
from typing import List

from components.layout_modern import modern_grid, page_container, section_card
from components.cards_modern import metric_card_modern, info_card_modern, stats_card_modern, empty_state_card
from components.svg_illustrations import (
    empty_state_illustration,
    success_illustration,
    error_illustration,
    chart_illustration,
    document_icon
)
from components.advanced_components import tabs, breadcrumbs, modal, pagination, accordion
from services.state_manager import get_state_manager
from services.historico_service import HistoricoService
from models.historico import HistoricoEntry


@component
def pagina_historico_moderna():
    """Página de histórico moderna com timeline e filtros"""

    state_manager = get_state_manager()
    historico_service = HistoricoService()

    # Estados
    filtro_status, set_filtro_status = use_state("todos")  # todos, sucesso, erro
    pagina_atual, set_pagina_atual = use_state(1)
    show_confirm_modal, set_show_confirm_modal = use_state(False)

    # Breadcrumbs
    breadcrumb = breadcrumbs([
        {"label": "Home", "href": "#", "icon": "🏠"},
        {"label": "Histórico", "icon": "📜"}
    ])

    # Carregar histórico
    historico = historico_service.carregar()

    # Verificar se há dados
    if not historico:
        return html.div(
            {"class": "animate-fade-in"},
            breadcrumb,
            page_container(
                empty_state_card(
                    mensagem="Nenhum histórico disponível. Execute relatórios para construir o histórico.",
                    icone="📜"
                ),
                html.div(
                    {
                        "style": {
                            "textAlign": "center",
                            "marginTop": "2rem",
                        }
                    },
                    empty_state_illustration(width="250px", height="250px"),
                    html.div(
                        {"style": {"marginTop": "1.5rem"}},
                        html.button(
                            {
                                "class": "btn btn-primary btn-lg",
                                "onClick": lambda e: state_manager.set_pagina("executar")
                            },
                            "🚀 Executar Primeiro Relatório"
                        )
                    )
                ),
                titulo="📜 Histórico de Execuções",
                descricao="Acompanhe todas as execuções realizadas"
            )
        )

    # Estatísticas
    stats = historico_service.obter_estatisticas()

    # Filtrar histórico
    historico_filtrado = historico
    if filtro_status == "sucesso":
        historico_filtrado = [e for e in historico if e.sucesso]
    elif filtro_status == "erro":
        historico_filtrado = [e for e in historico if not e.sucesso]

    # Paginação
    items_por_pagina = 10
    total_paginas = max(1, (len(historico_filtrado) + items_por_pagina - 1) // items_por_pagina)
    inicio = (pagina_atual - 1) * items_por_pagina
    fim = inicio + items_por_pagina
    historico_paginado = historico_filtrado[inicio:fim]

    # Função para limpar histórico
    def confirmar_limpar():
        set_show_confirm_modal(True)

    def limpar_historico():
        historico_service.limpar()
        state_manager.set_historico([])
        set_show_confirm_modal(False)

    # Agrupar por data para timeline
    dados_timeline = historico_service.agrupar_por_data()

    return html.div(
        {"class": "animate-fade-in"},

        # Breadcrumbs
        breadcrumb,

        # Modal de confirmação
        modal(
            "⚠️ Confirmar Exclusão",
            show_confirm_modal,
            lambda: set_show_confirm_modal(False),

            html.div(
                {"style": {"textAlign": "center", "padding": "1rem"}},
                error_illustration(width="120px", height="120px"),

                html.p(
                    {"style": {"marginTop": "1.5rem", "fontSize": "1.125rem"}},
                    "Tem certeza que deseja limpar todo o histórico?"
                ),

                html.p(
                    {
                        "style": {
                            "color": "var(--color-text-secondary)",
                            "fontSize": "0.875rem",
                        }
                    },
                    "Esta ação não pode ser desfeita!"
                ),

                html.div(
                    {
                        "style": {
                            "display": "flex",
                            "gap": "1rem",
                            "justifyContent": "center",
                            "marginTop": "2rem",
                        }
                    },
                    html.button(
                        {
                            "class": "btn btn-ghost",
                            "onClick": lambda e: set_show_confirm_modal(False)
                        },
                        "Cancelar"
                    ),
                    html.button(
                        {
                            "class": "btn btn-error",
                            "onClick": lambda e: limpar_historico()
                        },
                        "🗑️ Limpar Histórico"
                    )
                )
            ),

            size="medium"
        ),

        # Page Container
        page_container(
            # Métricas Principais
            html.div(
                {"style": {"marginBottom": "2rem"}},
                modern_grid(
                    metric_card_modern(
                        titulo="Total de Execuções",
                        valor=str(stats['total']),
                        variacao=None,
                        icone="📊",
                        cor="primary"
                    ),

                    metric_card_modern(
                        titulo="Execuções Bem-Sucedidas",
                        valor=str(stats['sucessos']),
                        variacao=None,
                        icone="✅",
                        cor="success"
                    ),

                    metric_card_modern(
                        titulo="Execuções com Erro",
                        valor=str(stats['erros']),
                        variacao=None,
                        icone="❌",
                        cor="error"
                    ),

                    metric_card_modern(
                        titulo="Taxa de Sucesso",
                        valor=f"{stats['taxa_sucesso']:.1f}%",
                        variacao=None,
                        icone="🎯",
                        cor="info"
                    ),
                    cols=4,
                    gap="1.5rem"
                )
            ),

            # Estatísticas adicionais
            html.div(
                {"style": {"marginBottom": "2rem"}},
                section_card(
                    "Estatísticas Detalhadas",
                    stats_card_modern([
                        ("Tempo Médio", f"{stats['tempo_medio']:.1f}s", "⏱️"),
                        ("Tempo Total", f"{stats['tempo_total']:.1f}s", "⏰"),
                        ("Última Execução", historico[0].data_formatada if historico else "N/A", "📅"),
                        ("Período", _calcular_periodo(historico), "📆"),
                    ]),
                    icone="📈"
                )
            ),

            # Tabs
            tabs(
                tabs_data=[
                    {
                        "id": "timeline",
                        "label": "Timeline",
                        "icon": "📈",
                        "content": tab_timeline(historico_paginado, dados_timeline, stats)
                    },
                    {
                        "id": "lista",
                        "label": "Lista Completa",
                        "icon": "📋",
                        "content": tab_lista(
                            historico_filtrado,
                            historico_paginado,
                            filtro_status,
                            set_filtro_status,
                            pagina_atual,
                            set_pagina_atual,
                            total_paginas,
                            confirmar_limpar
                        )
                    },
                    {
                        "id": "analise",
                        "label": "Análise",
                        "icon": "🔍",
                        "content": tab_analise(historico, stats, dados_timeline)
                    }
                ],
                default_tab="timeline"
            ),

            titulo="📜 Histórico de Execuções",
            descricao=f"Total de {stats['total']} execuções registradas"
        )
    )


@component
def tab_timeline(historico: List[HistoricoEntry], dados_timeline: dict, stats: dict):
    """Tab com visualização em timeline"""
    return html.div(
        {"class": "animate-fade-in"},

        section_card(
            "Timeline de Execuções",

            # Info sobre timeline
            html.div(
                {"style": {"marginBottom": "2rem"}},
                info_card_modern(
                    "Sobre a Timeline",
                    html.p(f"Mostrando as últimas {len(historico)} execuções em ordem cronológica reversa."),
                    tipo="info"
                )
            ),

            # Timeline
            html.div(
                {
                    "style": {
                        "position": "relative",
                        "paddingLeft": "2rem",
                    }
                },

                # Vertical line
                html.div(
                    {
                        "style": {
                            "position": "absolute",
                            "left": "1rem",
                            "top": "0",
                            "bottom": "0",
                            "width": "2px",
                            "background": "linear-gradient(to bottom, var(--color-primary), var(--color-border-light))",
                        }
                    }
                ),

                # Timeline items
                *[
                    _timeline_item(entry, idx)
                    for idx, entry in enumerate(historico)
                ]
            ),
            icone="📈"
        ),

        # Chart section
        html.div(
            {"style": {"marginTop": "2rem"}},
            section_card(
                "Execuções ao Longo do Tempo",

                html.div(
                    {"style": {"textAlign": "center", "padding": "2rem"}},
                    chart_illustration(width="200px", height="200px"),
                    html.p(
                        {
                            "style": {
                                "marginTop": "1rem",
                                "color": "var(--color-text-secondary)",
                            }
                        },
                        f"{len(dados_timeline)} dias com execuções registradas"
                    )
                ),
                icone="📊"
            )
        )
    )


@component
def tab_lista(
    historico_filtrado,
    historico_paginado,
    filtro_status,
    set_filtro_status,
    pagina_atual,
    set_pagina_atual,
    total_paginas,
    confirmar_limpar
):
    """Tab com lista completa e filtros"""
    return html.div(
        {"class": "animate-fade-in"},

        # Filtros e ações
        html.div(
            {"style": {"marginBottom": "2rem"}},
            section_card(
                "Filtros e Ações",

                html.div(
                    {
                        "style": {
                            "display": "flex",
                            "justifyContent": "space_between",
                            "alignItems": "center",
                            "flexWrap": "wrap",
                            "gap": "1rem",
                        }
                    },

                    # Filtros
                    html.div(
                        {
                            "style": {
                                "display": "flex",
                                "gap": "0.5rem",
                            }
                        },
                        html.button(
                            {
                                "class": f"btn {'btn-primary' if filtro_status == 'todos' else 'btn-ghost'}",
                                "onClick": lambda e: (set_filtro_status("todos"), set_pagina_atual(1))
                            },
                            "📊 Todos"
                        ),
                        html.button(
                            {
                                "class": f"btn {'btn-success' if filtro_status == 'sucesso' else 'btn-ghost'}",
                                "onClick": lambda e: (set_filtro_status("sucesso"), set_pagina_atual(1))
                            },
                            "✅ Sucessos"
                        ),
                        html.button(
                            {
                                "class": f"btn {'btn-error' if filtro_status == 'erro' else 'btn-ghost'}",
                                "onClick": lambda e: (set_filtro_status("erro"), set_pagina_atual(1))
                            },
                            "❌ Erros"
                        )
                    ),

                    # Botão limpar
                    html.button(
                        {
                            "class": "btn btn-error",
                            "onClick": lambda e: confirmar_limpar()
                        },
                        "🗑️ Limpar Histórico"
                    )
                ),
                icone="🔍"
            )
        ),

        # Lista de execuções
        section_card(
            f"Execuções ({len(historico_filtrado)})",

            # Cards de execução
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "1rem",
                    }
                },

                *[
                    _execution_card(entry)
                    for entry in historico_paginado
                ]
            ),

            # Paginação
            html.div(
                {"style": {"marginTop": "2rem"}},
                pagination(
                    current_page=pagina_atual,
                    total_pages=total_paginas,
                    on_page_change=set_pagina_atual
                ) if total_paginas > 1 else None
            ),
            icone="📋"
        )
    )


@component
def tab_analise(historico: List[HistoricoEntry], stats: dict, dados_timeline: dict):
    """Tab com análise detalhada"""
    return html.div(
        {"class": "animate-fade-in"},

        # Insights
        html.div(
            {"style": {"marginBottom": "2rem"}},
            section_card(
                "Insights e Análises",

                modern_grid(
                    info_card_modern(
                        "Performance",
                        html.p(_gerar_insight_performance(stats)),
                        tipo="success" if stats['taxa_sucesso'] >= 90 else "warning"
                    ),

                    info_card_modern(
                        "Tempo de Execução",
                        html.p(_gerar_insight_tempo(stats)),
                        tipo="info"
                    ),

                    info_card_modern(
                        "Frequência",
                        html.p(_gerar_insight_frequencia(historico)),
                        tipo="info"
                    ),

                    info_card_modern(
                        "Tendência",
                        html.p(_gerar_insight_tendencia(historico)),
                        tipo="info"
                    ),
                    cols=2,
                    gap="1.5rem"
                ),
                icone="💡"
            )
        ),

        # FAQ / Dúvidas Frequentes
        section_card(
            "Dúvidas Frequentes",

            accordion(
                items=[
                    {
                        "title": "Como funciona o histórico?",
                        "icon": "❓",
                        "content": html.p(
                            "O histórico registra automaticamente todas as execuções de relatórios, incluindo data, status, tempo de execução e número de fundos processados."
                        )
                    },
                    {
                        "title": "Quantas execuções são mantidas?",
                        "icon": "💾",
                        "content": html.p(
                            "O sistema mantém as últimas 100 execuções. Execuções mais antigas são automaticamente removidas."
                        )
                    },
                    {
                        "title": "Posso exportar o histórico?",
                        "icon": "📥",
                        "content": html.p(
                            "Sim! O histórico é salvo em formato JSON e pode ser acessado na pasta 'data/historico.json'."
                        )
                    },
                    {
                        "title": "O que fazer quando há muitos erros?",
                        "icon": "🆘",
                        "content": html.p(
                            "Verifique os detalhes dos erros nas execuções específicas. Problemas comuns incluem conexão com banco de dados, dados inválidos ou configurações incorretas."
                        )
                    }
                ]
            ),
            icone="❓"
        )
    )


@component
def _timeline_item(entry: HistoricoEntry, index: int):
    """Item da timeline"""
    cor = "var(--color-success)" if entry.sucesso else "var(--color-error)"
    icone = "✅" if entry.sucesso else "❌"

    return html.div(
        {
            "key": f"timeline-{index}",
            "style": {
                "position": "relative",
                "marginBottom": "2rem",
                "animation": f"slideInLeft 0.3s ease-out {index * 0.05}s both",
            }
        },

        # Dot
        html.div(
            {
                "style": {
                    "position": "absolute",
                    "left": "-2.125rem",
                    "top": "0.5rem",
                    "width": "1.5rem",
                    "height": "1.5rem",
                    "background": cor,
                    "border": "3px solid white",
                    "borderRadius": "50%",
                    "boxShadow": "0 0 0 3px " + cor + "20",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "fontSize": "0.75rem",
                }
            },
            icone
        ),

        # Card
        html.div(
            {
                "class": "card",
                "style": {
                    "background": "white",
                    "padding": "1.5rem",
                    "borderRadius": "1rem",
                    "boxShadow": "var(--shadow-sm)",
                    "border_left": f"4px solid {cor}",
                }
            },

            # Header
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "justifyContent": "space_between",
                        "alignItems": "start",
                        "marginBottom": "1rem",
                    }
                },

                html.div(
                    html.div(
                        {
                            "style": {
                                "fontWeight": "600",
                                "fontSize": "1.125rem",
                                "color": "var(--color-text-primary)",
                            }
                        },
                        f"{icone} Relatório de {entry.data_relatorio}"
                    ),
                    html.div(
                        {
                            "style": {
                                "fontSize": "0.875rem",
                                "color": "var(--color-text-secondary)",
                                "marginTop": "0.25rem",
                            }
                        },
                        f"Executado em {entry.data_formatada}"
                    )
                ),

                html.div(
                    {
                        "class": f"badge badge-{'success' if entry.sucesso else 'error'}",
                    },
                    entry.status.upper()
                )
            ),

            # Details
            html.div(
                {
                    "style": {
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(150px, 1fr))",
                        "gap": "1rem",
                    }
                },

                _detail_item("⏱️ Tempo", f"{entry.tempo_execucao:.2f}s"),
                _detail_item("📁 Fundos", str(entry.fundos_processados)),
                _detail_item("📅 Data", entry.data_relatorio)
            )
        )
    )


@component
def _execution_card(entry: HistoricoEntry):
    """Card de execução"""
    cor = "success" if entry.sucesso else "error"
    icone = "✅" if entry.sucesso else "❌"

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

        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space_between",
                    "alignItems": "center",
                    "flexWrap": "wrap",
                    "gap": "1rem",
                }
            },

            # Left side
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "1rem",
                    }
                },

                # Icon
                html.div(
                    {
                        "style": {
                            "width": "3rem",
                            "height": "3rem",
                            "background": f"var(--color-{cor}-light)",
                            "color": f"var(--color-{cor})",
                            "borderRadius": "0.75rem",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "fontSize": "1.5rem",
                        }
                    },
                    icone
                ),

                # Info
                html.div(
                    html.div(
                        {
                            "style": {
                                "fontWeight": "600",
                                "fontSize": "1rem",
                                "color": "var(--color-text-primary)",
                            }
                        },
                        f"Relatório de {entry.data_relatorio}"
                    ),
                    html.div(
                        {
                            "style": {
                                "fontSize": "0.875rem",
                                "color": "var(--color-text-secondary)",
                                "marginTop": "0.25rem",
                            }
                        },
                        entry.data_formatada
                    )
                )
            ),

            # Right side
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "gap": "2rem",
                        "alignItems": "center",
                    }
                },

                _stat_item("⏱️", f"{entry.tempo_execucao:.2f}s", "Tempo"),
                _stat_item("📁", str(entry.fundos_processados), "Fundos"),

                html.div(
                    {"class": f"badge badge-{cor}"},
                    entry.status.upper()
                )
            )
        )
    )


@component
def _detail_item(label: str, value: str):
    """Item de detalhe"""
    return html.div(
        {
            "style": {
                "padding": "0.75rem",
                "background": "var(--color-bg-secondary)",
                "borderRadius": "0.5rem",
            }
        },
        html.div(
            {
                "style": {
                    "fontSize": "0.75rem",
                    "color": "var(--color-text-secondary)",
                    "marginBottom": "0.25rem",
                }
            },
            label
        ),
        html.div(
            {
                "style": {
                    "fontWeight": "600",
                    "color": "var(--color-text-primary)",
                }
            },
            value
        )
    )


@component
def _stat_item(icon: str, value: str, label: str):
    """Item de estatística"""
    return html.div(
        {
            "style": {
                "textAlign": "center",
            }
        },
        html.div(
            {
                "style": {
                    "fontSize": "1.5rem",
                    "marginBottom": "0.25rem",
                }
            },
            icon
        ),
        html.div(
            {
                "style": {
                    "fontWeight": "700",
                    "fontSize": "1.125rem",
                    "color": "var(--color-text-primary)",
                }
            },
            value
        ),
        html.div(
            {
                "style": {
                    "fontSize": "0.75rem",
                    "color": "var(--color-text-secondary)",
                }
            },
            label
        )
    )


def _calcular_periodo(historico: List[HistoricoEntry]) -> str:
    """Calcula período do histórico"""
    if not historico:
        return "N/A"

    primeiro = historico[-1].timestamp
    ultimo = historico[0].timestamp
    dias = (ultimo - primeiro).days

    if dias == 0:
        return "Hoje"
    elif dias == 1:
        return "Últimos 2 dias"
    else:
        return f"Últimos {dias + 1} dias"


def _gerar_insight_performance(stats: dict) -> str:
    """Gera insight sobre performance"""
    taxa = stats['taxa_sucesso']

    if taxa >= 95:
        return f"Excelente! Taxa de sucesso de {taxa:.1f}%. Sistema operando perfeitamente."
    elif taxa >= 90:
        return f"Muito bom! Taxa de sucesso de {taxa:.1f}%. Sistema funcionando bem."
    elif taxa >= 75:
        return f"Atenção: Taxa de sucesso de {taxa:.1f}%. Considere investigar os erros."
    else:
        return f"Crítico: Taxa de sucesso de apenas {taxa:.1f}%. Verifique os erros urgentemente."


def _gerar_insight_tempo(stats: dict) -> str:
    """Gera insight sobre tempo de execução"""
    tempo = stats['tempo_medio']

    if tempo < 5:
        return f"Tempo médio excelente: {tempo:.1f}s por execução. Sistema muito rápido!"
    elif tempo < 15:
        return f"Tempo médio bom: {tempo:.1f}s por execução. Desempenho adequado."
    elif tempo < 30:
        return f"Tempo médio razoável: {tempo:.1f}s por execução. Pode ser otimizado."
    else:
        return f"Tempo médio alto: {tempo:.1f}s por execução. Considere otimizações."


def _gerar_insight_frequencia(historico: List[HistoricoEntry]) -> str:
    """Gera insight sobre frequência de execuções"""
    if not historico:
        return "Sem dados de frequência."

    dias = (historico[0].timestamp - historico[-1].timestamp).days + 1
    execucoes_por_dia = len(historico) / max(dias, 1)

    if execucoes_por_dia >= 5:
        return f"Alta frequência: {execucoes_por_dia:.1f} execuções/dia em média."
    elif execucoes_por_dia >= 2:
        return f"Frequência moderada: {execucoes_por_dia:.1f} execuções/dia em média."
    elif execucoes_por_dia >= 1:
        return f"Frequência baixa: {execucoes_por_dia:.1f} execuções/dia em média."
    else:
        return f"Frequência muito baixa: Menos de 1 execução por dia."


def _gerar_insight_tendencia(historico: List[HistoricoEntry]) -> str:
    """Gera insight sobre tendência"""
    if len(historico) < 10:
        return "Histórico insuficiente para análise de tendência."

    # Últimas 5 vs 5 anteriores
    recentes = historico[:5]
    antigas = historico[5:10]

    taxa_recente = sum(1 for e in recentes if e.sucesso) / len(recentes) * 100
    taxa_antiga = sum(1 for e in antigas if e.sucesso) / len(antigas) * 100

    diff = taxa_recente - taxa_antiga

    if diff > 10:
        return f"Tendência positiva! Taxa de sucesso aumentou {diff:.1f}% nas últimas execuções."
    elif diff < -10:
        return f"Tendência negativa. Taxa de sucesso caiu {abs(diff):.1f}% nas últimas execuções."
    else:
        return "Tendência estável. Taxa de sucesso manteve-se consistente."
