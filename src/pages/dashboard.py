"""
Página de Dashboard
Exibe métricas agregadas, gráficos e análises dos fundos
"""

from reactpy import component, html
from typing import Dict

from components.layout import container_pagina
from components.cards import card_metrica, card_info
from components.charts import grafico_pizza, grafico_barras
from components.tables import tabela_fundos
from services.state_manager import get_state_manager
from models.fundo import FundoData


@component
def pagina_dashboard():
    """Página de dashboard com análises"""

    state_manager = get_state_manager()
    ultima_exec = state_manager.ultima_execucao

    # Verificar se há dados
    if not ultima_exec or not ultima_exec.fundos:
        return container_pagina(
            html.div(
                {
                    "style": {
                        "textAlign": "center",
                        "padding": "3rem",
                        "color": "#999",
                    }
                },
                html.div(
                    {"style": {"fontSize": "3rem", "marginBottom": "1rem"}},
                    "📊"
                ),
                html.h3("Nenhum dado disponível"),
                html.p("Execute um relatório primeiro para visualizar o dashboard"),
                html.p(
                    {"style": {"marginTop": "1rem"}},
                    "Vá para a página 'Executar' e gere um relatório"
                )
            )
        )

    fundos = list(ultima_exec.fundos.values())

    # Calcular métricas agregadas
    total_pl = sum(f.pl for f in fundos)
    total_caixa = sum(f.caixa_total for f in fundos)
    total_fundos = len(fundos)
    perc_caixa_pl = (total_caixa / total_pl * 100) if total_pl > 0 else 0

    # Agrupar por tipo
    fundos_por_tipo: Dict[str, list[FundoData]] = {}
    for fundo in fundos:
        tipo = fundo.tipo
        if tipo not in fundos_por_tipo:
            fundos_por_tipo[tipo] = []
        fundos_por_tipo[tipo].append(fundo)

    # Dados para gráfico de pizza
    tipos = list(fundos_por_tipo.keys())
    valores_tipo = [sum(f.pl for f in fundos_por_tipo[t]) for t in tipos]

    # Top 10 fundos
    top_fundos = sorted(fundos, key=lambda f: f.pl, reverse=True)[:10]
    nomes_top = [f.nome for f in top_fundos]
    valores_top = [f.pl for f in top_fundos]

    return container_pagina(
        # Título
        html.h2(
            {"style": {"margin": "0 0 2rem 0", "color": "#333"}},
            "📊 Dashboard de Análise"
        ),

        # Cards de métricas
        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                    "gap": "1.5rem",
                    "marginBottom": "2rem",
                }
            },
            card_metrica("Patrimônio Total", f"R$ {total_pl/1000000:.1f}M", None, "primary", "💰"),
            card_metrica("Caixa Total", f"R$ {total_caixa/1000000:.1f}M", None, "success", "🏦"),
            card_metrica("Total de Fundos", str(total_fundos), None, "info", "📁"),
            card_metrica("% Caixa/PL", f"{perc_caixa_pl:.2f}%", None, "warning", "📊"),
        ),

        # Info da execução
        card_info(
            "ℹ️ Informações da Execução",
            html.div(
                html.p(
                    {"style": {"margin": "0.5rem 0"}},
                    html.strong("Data do relatório: "),
                    ultima_exec.data_relatorio.strftime('%d/%m/%Y')
                ),
                html.p(
                    {"style": {"margin": "0.5rem 0"}},
                    html.strong("Tempo de execução: "),
                    f"{ultima_exec.tempo_execucao:.2f}s"
                ),
                html.p(
                    {"style": {"margin": "0.5rem 0"}},
                    html.strong("Versão: "),
                    ultima_exec.versao_modulo
                ),
            )
        ),

        # Gráficos
        html.h3(
            {"style": {"margin": "2rem 0 1rem 0", "color": "#333"}},
            "📈 Visualizações"
        ),

        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(450px, 1fr))",
                    "gap": "2rem",
                    "marginBottom": "2rem",
                }
            },
            # Gráfico de pizza - PL por tipo
            grafico_pizza(
                valores_tipo,
                tipos,
                "Distribuição de PL por Tipo de Fundo",
                400
            ),
            # Gráfico de barras - Top 10
            grafico_barras(
                valores_top,
                nomes_top,
                "Top 10 Fundos por Patrimônio Líquido",
                True,
                400
            ),
        ),

        # Análise por tipo
        html.h3(
            {"style": {"margin": "2rem 0 1rem 0", "color": "#333"}},
            "📋 Análise por Tipo de Fundo"
        ),

        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(300px, 1fr))",
                    "gap": "1.5rem",
                    "marginBottom": "2rem",
                }
            },
            *[
                html.div(
                    {
                        "key": tipo,
                        "style": {
                            "background": "#f8f9fa",
                            "padding": "1.5rem",
                            "borderRadius": "12px",
                            "border_left": "5px solid #667eea",
                        }
                    },
                    html.h4(
                        {"style": {"margin": "0 0 1rem 0", "color": "#333"}},
                        tipo
                    ),
                    html.div(
                        {"style": {"fontSize": "0.9rem", "color": "#666"}},
                        html.p(
                            {"style": {"margin": "0.5rem 0"}},
                            html.strong("Quantidade: "),
                            f"{len(fundos_por_tipo[tipo])} fundos"
                        ),
                        html.p(
                            {"style": {"margin": "0.5rem 0"}},
                            html.strong("PL Total: "),
                            f"R$ {sum(f.pl for f in fundos_por_tipo[tipo])/1000000:.1f}M"
                        ),
                        html.p(
                            {"style": {"margin": "0.5rem 0"}},
                            html.strong("PL Médio: "),
                            f"R$ {sum(f.pl for f in fundos_por_tipo[tipo])/len(fundos_por_tipo[tipo])/1000000:.1f}M"
                        ),
                        html.p(
                            {"style": {"margin": "0.5rem 0"}},
                            html.strong("% do Total: "),
                            f"{sum(f.pl for f in fundos_por_tipo[tipo])/total_pl*100:.1f}%"
                        ),
                    )
                )
                for tipo in sorted(fundos_por_tipo.keys())
            ]
        ),

        # Tabela de fundos
        html.h3(
            {"style": {"margin": "2rem 0 1rem 0", "color": "#333"}},
            "📄 Dados Detalhados dos Fundos"
        ),

        tabela_fundos(fundos, mostrar_alertas=True),

        # Estatísticas adicionais
        html.div(
            {"style": {"marginTop": "2rem"}},
            card_info(
                "📊 Estatísticas Adicionais",
                html.div(
                    {"style": {"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))", "gap": "1rem"}},
                    html.div(
                        html.p({"style": {"margin": "0", "color": "#666", "fontSize": "0.85rem"}}, "Maior PL"),
                        html.p(
                            {"style": {"margin": "0.25rem 0 0 0", "fontWeight": "600", "fontSize": "1.1rem"}},
                            f"{max(fundos, key=lambda f: f.pl).nome}"
                        ),
                        html.p(
                            {"style": {"margin": "0", "color": "#999", "fontSize": "0.85rem"}},
                            f"R$ {max(fundos, key=lambda f: f.pl).pl/1000000:.1f}M"
                        ),
                    ),
                    html.div(
                        html.p({"style": {"margin": "0", "color": "#666", "fontSize": "0.85rem"}}, "Maior Caixa"),
                        html.p(
                            {"style": {"margin": "0.25rem 0 0 0", "fontWeight": "600", "fontSize": "1.1rem"}},
                            f"{max(fundos, key=lambda f: f.caixa_total).nome}"
                        ),
                        html.p(
                            {"style": {"margin": "0", "color": "#999", "fontSize": "0.85rem"}},
                            f"R$ {max(fundos, key=lambda f: f.caixa_total).caixa_total/1000000:.1f}M"
                        ),
                    ),
                    html.div(
                        html.p({"style": {"margin": "0", "color": "#666", "fontSize": "0.85rem"}}, "Maior Var. D-1"),
                        html.p(
                            {"style": {"margin": "0.25rem 0 0 0", "fontWeight": "600", "fontSize": "1.1rem", "color": "#10b981"}},
                            f"{max(fundos, key=lambda f: f.variacao_d1).nome}"
                        ),
                        html.p(
                            {"style": {"margin": "0", "color": "#10b981", "fontSize": "0.85rem", "fontWeight": "600"}},
                            f"+{max(fundos, key=lambda f: f.variacao_d1).variacao_d1:.2f}%"
                        ),
                    ),
                    html.div(
                        html.p({"style": {"margin": "0", "color": "#666", "fontSize": "0.85rem"}}, "Fundos com Alerta"),
                        html.p(
                            {"style": {"margin": "0.25rem 0 0 0", "fontWeight": "600", "fontSize": "1.1rem", "color": "#f59e0b"}},
                            f"{sum(1 for f in fundos if f.tem_alertas())}"
                        ),
                        html.p(
                            {"style": {"margin": "0", "color": "#999", "fontSize": "0.85rem"}},
                            f"de {total_fundos} fundos"
                        ),
                    ),
                )
            )
        )
    )
