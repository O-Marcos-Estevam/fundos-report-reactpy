"""
Página de Lâmina de Fundos Moderna
Visualização detalhada de um fundo específico com componentes modernos
"""

from reactpy import component, html, use_state
from typing import Optional

from components.layout_modern import modern_grid, page_container, section_card
from components.cards_modern import metric_card_modern, info_card_modern, empty_state_card
from components.svg_illustrations import (
    empty_state_illustration,
    fund_icon,
    money_icon,
    trending_up_icon,
    trending_down_icon,
    document_icon,
    success_illustration
)
from components.advanced_components import tabs, breadcrumbs, dropdown
from components.charts import grafico_evolucao, grafico_pizza
from services.state_manager import get_state_manager
from models.fundo import FundoData


@component
def pagina_lamina_fundos_moderna():
    """Página de lâmina detalhada moderna de um fundo"""

    state_manager = get_state_manager()

    # Adicionar refresh key para forçar atualização
    refresh_key, set_refresh_key = use_state(0)
    fundo_selecionado, set_fundo = use_state(None)

    def atualizar_dados():
        """Força atualização dos dados"""
        set_refresh_key(lambda k: k + 1)

    # Buscar dados atualizados
    ultima_exec = state_manager.ultima_execucao

    # Breadcrumbs
    breadcrumb = breadcrumbs([
        {"label": "Home", "href": "#", "icon": "🏠"},
        {"label": "Lâmina de Fundos", "icon": "📄"}
    ])

    # Verificar se há dados
    if not ultima_exec or not ultima_exec.fundos:
        return html.div(
            breadcrumb,
            page_container(
                empty_state_card(
                    mensagem="Nenhum dado disponível. Execute um relatório primeiro.",
                    icone="📄"
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
                titulo="📄 Lâmina de Fundos",
                descricao="Visualização detalhada de um fundo específico"
            )
        )

    fundos_disponiveis = list(ultima_exec.fundos.keys())

    # Se não tiver fundo selecionado
    if not fundo_selecionado or fundo_selecionado not in ultima_exec.fundos:
        return html.div(
            {"class": "animate-fade-in"},
            breadcrumb,
            page_container(
                # Seletor moderno de fundo
                section_card(
                    "Selecione um Fundo",

                    html.div(
                        {"style": {"marginBottom": "1.5rem"}},
                        info_card_modern(
                            "Como usar",
                            html.p("Escolha um fundo da lista abaixo para visualizar sua lâmina detalhada com métricas, gráficos e análises."),
                            tipo="info"
                        )
                    ),

                    # Grid de fundos
                    modern_grid(
                        *[
                            _fundo_selection_card(nome, ultima_exec.fundos[nome], set_fundo)
                            for nome in sorted(fundos_disponiveis)
                        ],
                        cols=3,
                        gap="1rem"
                    ),
                    icone="🔍"
                ),
                titulo="📄 Lâmina de Fundos",
                descricao=f"{len(fundos_disponiveis)} fundos disponíveis para visualização"
            )
        )

    # Obter dados do fundo selecionado
    fundo = ultima_exec.fundos[fundo_selecionado]

    # Dados de evolução
    periodos = ['Atual', 'D-1', 'D-7', 'D-30']
    valores_pl = [
        fundo.pl or 0.0,
        fundo.pl_d1 or 0.0,
        fundo.pl_d7 or 0.0,
        fundo.pl_d30 or 0.0
    ]

    # Dados de composição
    componentes = []
    valores_comp = []
    if fundo.caixa_bancario and fundo.caixa_bancario > 0:
        componentes.append('Caixa Bancário')
        valores_comp.append(fundo.caixa_bancario)
    if fundo.caixa_reag_ii and fundo.caixa_reag_ii > 0:
        componentes.append('REAG II')
        valores_comp.append(fundo.caixa_reag_ii)
    if fundo.pl_posicao_ativos and fundo.pl_posicao_ativos > 0:
        componentes.append('Posição Ativos')
        valores_comp.append(fundo.pl_posicao_ativos)

    return html.div(
        {"class": "animate-fade-in"},
        # Breadcrumbs
        breadcrumb,
        # Page Container
        page_container(
            # Header do fundo com dropdown para trocar
            html.div(
                {"style": {"marginBottom": "2rem"}},
                _fundo_header(fundo_selecionado, fundo, fundos_disponiveis, set_fundo, ultima_exec.data_relatorio.strftime('%d/%m/%Y'))
            ),

            # Métricas principais
            html.div(
                {"style": {"marginBottom": "2rem"}},
                modern_grid(
                    metric_card_modern(
                        titulo="Patrimônio Líquido",
                        valor=f"R$ {(fundo.pl or 0.0)/1_000_000:.2f}M" if (fundo.pl or 0.0) > 1_000_000 else f"R$ {(fundo.pl or 0.0):,.0f}",
                        variacao=fundo.variacao_d1 if hasattr(fundo, 'variacao_d1') else None,
                        icone="💰",
                        cor="primary"
                    ),

                    metric_card_modern(
                        titulo="Caixa Total",
                        valor=f"R$ {(fundo.caixa_total or 0.0)/1_000_000:.2f}M" if (fundo.caixa_total or 0.0) > 1_000_000 else f"R$ {(fundo.caixa_total or 0.0):,.0f}",
                        variacao=None,
                        icone="🏦",
                        cor="success"
                    ),

                    metric_card_modern(
                        titulo="% Caixa/PL",
                        valor=f"{(fundo.perc_caixa_pl or 0.0):.2f}%",
                        variacao=None,
                        icone="📊",
                        cor="warning"
                    ),

                    metric_card_modern(
                        titulo="Taxas Devidas",
                        valor=f"R$ {(fundo.devido_taxas or 0.0):,.0f}",
                        variacao=None,
                        icone="💳",
                        cor="info"
                    ),
                    cols=4,
                    gap="1.5rem"
                )
            ),

            # Tabs com diferentes visualizações
            tabs(
                tabs_data=[
                    {
                        "id": "visao_geral",
                        "label": "Visão Geral",
                        "icon": "📊",
                        "content": tab_visao_geral(fundo, periodos, valores_pl, componentes, valores_comp)
                    },
                    {
                        "id": "composicao",
                        "label": "Composição",
                        "icon": "🥧",
                        "content": tab_composicao(fundo, componentes, valores_comp)
                    },
                    {
                        "id": "historico",
                        "label": "Histórico",
                        "icon": "📈",
                        "content": tab_historico(fundo, periodos, valores_pl)
                    },
                    {
                        "id": "detalhes",
                        "label": "Detalhes",
                        "icon": "📋",
                        "content": tab_detalhes(fundo, ultima_exec.data_relatorio.strftime('%d/%m/%Y'))
                    },
                    {
                        "id": "alertas",
                        "label": "Alertas",
                        "icon": "⚠️",
                        "content": tab_alertas(fundo)
                    }
                ],
                default_tab="visao_geral"
            ),
            titulo="📄 Lâmina de Fundos",
            descricao=f"Análise detalhada • Data: {ultima_exec.data_relatorio.strftime('%d/%m/%Y')}"
        )
    )


@component
def _fundo_header(nome: str, fundo: FundoData, fundos_disponiveis: list, set_fundo, data_base: str):
    """Header do fundo com informações e dropdown para trocar"""
    return html.div(
        {
            "class": "card",
            "style": {
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "color": "white",
                "padding": "2rem",
                "borderRadius": "1.5rem",
                "boxShadow": "var(--shadow-xl)",
            }
        },

        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space_between",
                    "alignItems": "start",
                    "flexWrap": "wrap",
                    "gap": "1rem",
                }
            },

            # Left side
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "alignItems": "start",
                        "gap": "1.5rem",
                    }
                },

                # Icon
                html.div(
                    {
                        "style": {
                            "width": "4rem",
                            "height": "4rem",
                            "background": "rgba(255, 255, 255, 0.2)",
                            "borderRadius": "1rem",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "fontSize": "2rem",
                        }
                    },
                    "🏦"
                ),

                # Info
                html.div(
                    html.h2(
                        {"style": {"margin": "0", "color": "white", "fontSize": "1.75rem"}},
                        nome
                    ),
                    html.div(
                        {
                            "style": {
                                "display": "flex",
                                "gap": "1rem",
                                "marginTop": "0.5rem",
                                "alignItems": "center",
                            }
                        },
                        html.div(
                            {
                                "class": "badge",
                                "style": {
                                    "background": "rgba(255, 255, 255, 0.2)",
                                    "color": "white",
                                    "border": "1px solid rgba(255, 255, 255, 0.3)",
                                }
                            },
                            fundo.tipo
                        ),
                        html.span(
                            {"style": {"opacity": "0.9"}},
                            f"📅 {data_base}"
                        )
                    )
                )
            ),

            # Right side - Dropdown para trocar fundo
            html.div(
                dropdown(
                    label="Trocar Fundo",
                    items=[
                        {"label": f, "value": f, "icon": "🏦"}
                        for f in sorted(fundos_disponiveis)
                        if f != nome
                    ],
                    on_select=lambda value: set_fundo(value)
                )
            )
        )
    )


@component
def tab_visao_geral(fundo: FundoData, periodos: list, valores_pl: list, componentes: list, valores_comp: list):
    """Tab de visão geral"""
    return html.div(
        {"class": "animate-fade-in"},

        # Resumo rápido
        html.div(
            {"style": {"marginBottom": "2rem"}},
            section_card(
                "Resumo Rápido",

                modern_grid(
                    info_card_modern(
                        "Informação do Fundo",
                        html.p(f"Fundo do tipo {fundo.tipo or '-'} com patrimônio líquido de R$ {(fundo.pl or 0.0):,.2f}."),
                        tipo="info"
                    ),

                    info_card_modern(
                        "Posição de Caixa",
                        html.p(f"O fundo possui {(fundo.perc_caixa_pl or 0.0):.2f}% do PL em caixa, totalizando R$ {(fundo.caixa_total or 0.0):,.2f}."),
                        tipo="success" if (fundo.perc_caixa_pl or 0.0) < 20 else "warning"
                    ),
                    cols=2,
                    gap="1.5rem"
                ),
                icone="📊"
            )
        ),

        # Gráficos
        modern_grid(
            section_card(
                "Evolução do Patrimônio",
                grafico_evolucao(periodos, valores_pl, titulo="Evolução do PL") if valores_pl and len(valores_pl) > 0 and any(v > 0 for v in valores_pl) else html.div(
                    {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
                    "Sem dados de evolução disponíveis"
                ),
                icone="📈"
            ),

            section_card(
                "Composição Patrimonial",
                grafico_pizza(valores_comp, componentes, titulo="Composição") if valores_comp and len(valores_comp) > 0 else html.div(
                    {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
                    "Sem dados de composição disponíveis"
                ),
                icone="🥧"
            ),
            cols=2,
            gap="1.5rem"
        )
    )


@component
def tab_composicao(fundo: FundoData, componentes: list, valores_comp: list):
    """Tab de composição detalhada"""
    return html.div(
        {"class": "animate-fade-in"},

        section_card(
            "Composição Detalhada do Patrimônio",
            html.div(
                {"style": {"marginBottom": "2rem"}},
                modern_grid(
                    _componente_card("Caixa Bancário", fundo.caixa_bancario, fundo.pl, "🏦"),
                    _componente_card("REAG II", fundo.caixa_reag_ii, fundo.pl, "💰"),
                    _componente_card("Posição Ativos", fundo.pl_posicao_ativos, fundo.pl, "📊"),
                    cols=3,
                    gap="1.5rem"
                )
            ),

            # Gráfico maior
            html.div(
                {"style": {"marginTop": "2rem"}},
                grafico_pizza(valores_comp, componentes, titulo="Distribuição Patrimonial", altura=400) if valores_comp and len(valores_comp) > 0 else html.div(
                    {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
                    "Sem dados de composição disponíveis"
                )
            ),
            icone="🥧"
        )
    )


@component
def tab_historico(fundo: FundoData, periodos: list, valores_pl: list):
    """Tab de histórico de evolução"""
    return html.div(
        {"class": "animate-fade-in"},

        section_card(
            "Evolução Histórica do Patrimônio",
            # Métricas de variação
            html.div(
                {"style": {"marginBottom": "2rem"}},
                modern_grid(
                    _variacao_card("Variação D-1", fundo.variacao_d1, fundo.pl, fundo.pl_d1),
                    _variacao_card("Variação D-7", fundo.variacao_d7, fundo.pl, fundo.pl_d7),
                    _variacao_card("Variação D-30", fundo.variacao_d30, fundo.pl, fundo.pl_d30),
                    cols=3,
                    gap="1.5rem"
                )
            ),

            # Gráfico de evolução
            html.div(
                {"style": {"marginTop": "2rem"}},
                grafico_evolucao(periodos, valores_pl, titulo="Evolução do Patrimônio Líquido", altura=400) if valores_pl and len(valores_pl) > 0 and any(v > 0 for v in valores_pl) else html.div(
                    {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
                    "Sem dados históricos disponíveis para exibir o gráfico"
                )
            ),
            icone="📈"
        )
    )


@component
def tab_detalhes(fundo: FundoData, data_base: str):
    """Tab com detalhes completos"""
    return html.div(
        {"class": "animate-fade-in"},

        section_card(
            "Informações Completas",
            html.div(
                {
                    "style": {
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                        "gap": "1rem",
                    }
                },

                _detail_field("Tipo de Fundo", fundo.tipo or "-", "🏷️"),
                _detail_field("Data Base", data_base, "📅"),
                _detail_field("PL Atual", f"R$ {fundo.pl or 0.0:,.2f}", "💰"),
                _detail_field("PL D-1", f"R$ {fundo.pl_d1 or 0.0:,.2f}", "📊"),
                _detail_field("PL D-7", f"R$ {fundo.pl_d7 or 0.0:,.2f}", "📊"),
                _detail_field("PL D-30", f"R$ {fundo.pl_d30 or 0.0:,.2f}", "📊"),
                _detail_field("Caixa Bancário", f"R$ {fundo.caixa_bancario or 0.0:,.2f}", "🏦"),
                _detail_field("REAG II", f"R$ {fundo.caixa_reag_ii or 0.0:,.2f}", "💵"),
                _detail_field("Caixa Total", f"R$ {fundo.caixa_total or 0.0:,.2f}", "💰"),
                _detail_field("% Caixa/PL", f"{fundo.perc_caixa_pl:.2f}%", "📊"),
                _detail_field("Posição Ativos", f"R$ {fundo.pl_posicao_ativos or 0.0:,.2f}", "📈"),
                _detail_field("Taxas Devidas", f"R$ {fundo.devido_taxas or 0.0:,.2f}", "💳"),
            )
        ),

        # Informações adicionais se houver cotista
        html.div(
            {"style": {"marginTop": "2rem"}},
            section_card(
                "Informações Adicionais",
                html.div(
                    {"style": {"padding": "1rem"}},
                    _detail_field("Cotista", fundo.cotista if fundo.cotista else "N/A", "👤")
                ) if fundo.cotista else info_card_modern(
                    "Sem informações adicionais",
                    html.p("Não há informações adicionais disponíveis para este fundo."),
                    tipo="info"
                )
            )
        )
    )


@component
def tab_alertas(fundo: FundoData):
    """Tab com alertas e análises"""
    alertas = fundo.get_alertas() if hasattr(fundo, 'get_alertas') else []
    tem_alertas = fundo.tem_alertas() if hasattr(fundo, 'tem_alertas') else len(alertas) > 0

    return html.div(
        {"class": "animate-fade-in"},

        section_card(
            "Análise e Alertas",
            html.div(
                {"style": {"marginBottom": "1.5rem"}},
                info_card_modern(
                    "Sobre os Alertas",
                    html.p("Os alertas são gerados automaticamente com base em regras de negócio e limites predefinidos."),
                    tipo="info"
                )
            ),

            # Lista de alertas
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "1rem",
                    }
                },

                *[
                    _alerta_card(nivel, mensagem)
                    for nivel, mensagem in alertas
                ] if tem_alertas else [
                    html.div(
                        {
                            "style": {
                                "textAlign": "center",
                                "padding": "3rem",
                            }
                        },
                        success_illustration(width="150px", height="150px"),
                        html.h3(
                            {"style": {"marginTop": "1.5rem", "color": "var(--color-success)"}},
                            "✅ Sem Alertas"
                        ),
                        html.p(
                            {"style": {"color": "var(--color-text-secondary)"}},
                            "Nenhum alerta identificado para este fundo. Tudo está dentro dos parâmetros esperados."
                        )
                    )
                ]
            )
        )
    )


@component
def _fundo_selection_card(nome: str, fundo: FundoData, set_fundo):
    """Card para seleção de fundo"""
    return html.button(
        {
            "onClick": lambda e: set_fundo(nome),
            "class": "card",
            "style": {
                "background": "white",
                "padding": "1.5rem",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-sm)",
                "cursor": "pointer",
                "border": "2px solid transparent",
                "transition": "all 0.2s",
                "textAlign": "left",
            }
        },

        html.div(
            {"style": {"display": "flex", "alignItems": "center", "gap": "1rem", "marginBottom": "1rem"}},
            html.div(
                {
                    "style": {
                        "width": "3rem",
                        "height": "3rem",
                        "background": "var(--color-primary-light)",
                        "color": "var(--color-primary)",
                        "borderRadius": "0.75rem",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "fontSize": "1.5rem",
                    }
                },
                "🏦"
            ),
            html.div(
                {"class": "badge badge-primary"},
                fundo.tipo
            )
        ),

        html.h4(
            {
                "style": {
                    "margin": "0 0 0.5rem 0",
                    "fontSize": "1rem",
                    "color": "var(--color-text-primary)",
                }
            },
            nome
        ),

        html.div(
            {
                "style": {
                    "fontSize": "1.25rem",
                    "fontWeight": "700",
                    "color": "var(--color-primary)",
                }
            },
            f"R$ {(fundo.pl or 0.0)/1_000_000:.2f}M" if (fundo.pl or 0.0) > 1_000_000 else f"R$ {(fundo.pl or 0.0):,.0f}"
        )
    )


@component
def _componente_card(titulo: str, valor: float, pl_total: float, icone: str):
    """Card de componente patrimonial"""
    valor = valor or 0.0
    pl_total = pl_total or 0.0
    percentual = (valor / pl_total * 100) if pl_total > 0 else 0

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
            {"style": {"display": "flex", "alignItems": "center", "gap": "0.75rem", "marginBottom": "1rem"}},
            html.span({"style": {"fontSize": "1.5rem"}}, icone),
            html.h4(
                {"style": {"margin": "0", "fontSize": "1rem", "color": "var(--color-text-secondary)"}},
                titulo
            )
        ),

        html.div(
            {"style": {"fontSize": "1.5rem", "fontWeight": "700", "color": "var(--color-text-primary)", "marginBottom": "0.5rem"}},
            f"R$ {valor:,.2f}"
        ),

        html.div(
            {
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "0.5rem",
                }
            },
            html.div(
                {
                    "style": {
                        "flex": "1",
                        "height": "0.5rem",
                        "background": "var(--color-bg-secondary)",
                        "borderRadius": "0.25rem",
                        "overflow": "hidden",
                    }
                },
                html.div(
                    {
                        "style": {
                            "width": f"{min(percentual, 100)}%",
                            "height": "100%",
                            "background": "var(--color-primary)",
                            "transition": "width 0.3s",
                        }
                    }
                )
            ),
            html.span(
                {"style": {"fontSize": "0.875rem", "fontWeight": "600", "color": "var(--color-text-secondary)"}},
                f"{percentual:.1f}%"
            )
        )
    )


@component
def _variacao_card(titulo: str, variacao: Optional[float], valor_atual: float, valor_anterior: float):
    """Card de variação"""
    valor_atual = valor_atual or 0.0
    valor_anterior = valor_anterior or 0.0
    variacao = variacao or 0.0
    cor = "success" if variacao > 0 else "error" if variacao < 0 else "info"
    icone = "📈" if variacao > 0 else "📉" if variacao < 0 else "➖"

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
            {"style": {"fontSize": "0.875rem", "color": "var(--color-text-secondary)", "marginBottom": "0.5rem"}},
            titulo
        ),

        html.div(
            {
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "0.5rem",
                    "marginBottom": "1rem",
                }
            },
            html.span({"style": {"fontSize": "1.5rem"}}, icone),
            html.div(
                {
                    "style": {
                        "fontSize": "1.75rem",
                        "fontWeight": "700",
                        "color": f"var(--color-{cor})",
                    }
                },
                f"{variacao:+.2f}%" if variacao is not None else "N/A"
            )
        ),

        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space_between",
                    "fontSize": "0.875rem",
                    "color": "var(--color-text-secondary)",
                }
            },
            html.span(f"Atual: R$ {valor_atual:,.0f}"),
            html.span(f"Anterior: R$ {valor_anterior:,.0f}")
        )
    )


@component
def _detail_field(label: str, value: str, icon: str):
    """Campo de detalhe"""
    return html.div(
        {
            "class": "card",
            "style": {
                "background": "var(--color-bg-secondary)",
                "padding": "1rem",
                "borderRadius": "0.75rem",
            }
        },

        html.div(
            {"style": {"display": "flex", "alignItems": "center", "gap": "0.5rem", "marginBottom": "0.5rem"}},
            html.span({"style": {"fontSize": "1rem"}}, icon),
            html.div(
                {"style": {"fontSize": "0.75rem", "color": "var(--color-text-secondary)", "textTransform": "uppercase", "letterSpacing": "0.05em"}},
                label
            )
        ),

        html.div(
            {"style": {"fontWeight": "600", "color": "var(--color-text-primary)"}},
            value
        )
    )


@component
def _alerta_card(nivel: str, mensagem: str):
    """Card de alerta"""
    tipo_map = {
        "error": "error",
        "warning": "warning",
        "info": "info",
        "success": "success"
    }

    tipo = "error"
    for key in tipo_map:
        if key in nivel.lower() or "crítico" in mensagem.lower():
            tipo = tipo_map[key]
            break

    icone_map = {
        "error": "🚨",
        "warning": "⚠️",
        "info": "ℹ️",
        "success": "✅"
    }

    return info_card_modern(
        f"{icone_map.get(tipo, '⚠️')} {nivel.upper()}",
        html.p(mensagem),
        tipo=tipo
    )
