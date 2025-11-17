"""
Página de Histórico
Exibe histórico de execuções com estatísticas
"""

from reactpy import component, html

from components.layout import container_pagina
from components.cards import card_metrica, card_estatistica
from components.charts import grafico_timeline
from components.tables import tabela_historico
from components.forms import botao
from services.state_manager import get_state_manager
from services.historico_service import HistoricoService


@component
def pagina_historico():
    """Página de histórico de execuções"""

    state_manager = get_state_manager()
    historico_service = HistoricoService()

    # Carregar histórico
    historico = historico_service.carregar()

    # Estatísticas
    stats = historico_service.obter_estatisticas()

    # Dados para gráfico
    dados_timeline = historico_service.agrupar_por_data()

    def limpar_historico(event):
        """Limpa o histórico"""
        historico_service.limpar()
        state_manager.set_historico([])

    if not historico:
        return container_pagina(
            html.h2(
                {"style": {"margin": "0 0 2rem 0", "color": "#333"}},
                "📜 Histórico de Execuções"
            ),
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
                    "📜"
                ),
                html.h3("Nenhum histórico disponível"),
                html.p("Execute relatórios para construir o histórico de execuções")
            )
        )

    return container_pagina(
        # Título
        html.h2(
            {"style": {"margin": "0 0 2rem 0", "color": "#333"}},
            "📜 Histórico de Execuções"
        ),

        # Estatísticas gerais
        html.h3(
            {"style": {"margin": "0 0 1rem 0", "color": "#333"}},
            "📊 Estatísticas Gerais"
        ),

        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))",
                    "gap": "1.5rem",
                    "marginBottom": "2rem",
                }
            },
            card_estatistica("Total de Execuções", str(stats['total'])),
            card_estatistica("Execuções Bem-Sucedidas", str(stats['sucessos']), "✅"),
            card_estatistica("Execuções com Erro", str(stats['erros']), "❌"),
            card_estatistica("Taxa de Sucesso", f"{stats['taxa_sucesso']:.1f}%", "🎯"),
            card_estatistica("Tempo Médio", f"{stats['tempo_medio']:.1f}s", "⏱️"),
        ),

        # Gráfico temporal
        html.h3(
            {"style": {"margin": "2rem 0 1rem 0", "color": "#333"}},
            "📈 Execuções ao Longo do Tempo"
        ),

        html.div(
            {"style": {"marginBottom": "2rem"}},
            grafico_timeline(dados_timeline) if dados_timeline else html.div(
                {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
                "Sem dados suficientes para gráfico"
            )
        ),

        # Lista de execuções
        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space_between",
                    "alignItems": "center",
                    "margin": "2rem 0 1rem 0",
                }
            },
            html.h3(
                {"style": {"margin": "0", "color": "#333"}},
                f"📋 Lista de Execuções (Últimas {min(len(historico), 20)})"
            ),
            botao(
                "Limpar Histórico",
                limpar_historico,
                tipo="danger",
                icone="🗑️"
            )
        ),

        tabela_historico(historico[:20]),  # Mostrar últimas 20

        # Informação adicional
        html.div(
            {
                "style": {
                    "marginTop": "2rem",
                    "padding": "1rem",
                    "background": "#f0f7ff",
                    "borderRadius": "8px",
                    "color": "#333",
                    "fontSize": "0.9rem",
                }
            },
            html.p(
                {"style": {"margin": "0"}},
                f"ℹ️ O histórico mantém até {historico_service.obter_estatisticas()['total']} execuções recentes. ",
                "Execuções mais antigas são automaticamente removidas."
            )
        )
    )
