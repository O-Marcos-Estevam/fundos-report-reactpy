"""
Página de Lâmina de Fundos
Visualização detalhada de um fundo específico
"""

from reactpy import component, html, use_state

from components.layout import container_pagina
from components.cards import card_metrica, card_status
from components.charts import grafico_evolucao, grafico_pizza
from components.forms import seletor_fundo
from components.tables import tabela_detalhes
from services.state_manager import get_state_manager


@component
def pagina_lamina_fundos():
    """Página de lâmina detalhada de um fundo"""

    state_manager = get_state_manager()
    ultima_exec = state_manager.ultima_execucao

    fundo_selecionado, set_fundo = use_state(None)

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
                    "📄"
                ),
                html.h3("Nenhum dado disponível"),
                html.p("Execute um relatório primeiro para visualizar a lâmina de fundos")
            )
        )

    fundos_disponiveis = list(ultima_exec.fundos.keys())

    # Seletor de fundo
    seletor = seletor_fundo(fundos_disponiveis, fundo_selecionado, set_fundo)

    # Se não tiver fundo selecionado
    if not fundo_selecionado or fundo_selecionado not in ultima_exec.fundos:
        return container_pagina(
            html.h2(
                {"style": {"margin": "0 0 2rem 0", "color": "#333"}},
                "📄 Lâmina de Fundo"
            ),
            seletor,
            html.div(
                {
                    "style": {
                        "textAlign": "center",
                        "padding": "3rem",
                        "color": "#999",
                    }
                },
                html.h3("Selecione um fundo"),
                html.p("Use o seletor acima para escolher um fundo e visualizar seus detalhes")
            )
        )

    # Obter dados do fundo
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

    # Detalhes para tabela
    try:
        detalhes = {
            "Tipo": fundo.tipo or "-",
            "PL Atual": fundo.pl or 0.0,
            "PL D-1": fundo.pl_d1 or 0.0,
            "PL D-7": fundo.pl_d7 or 0.0,
            "PL D-30": fundo.pl_d30 or 0.0,
            "Caixa Total": fundo.caixa_total or 0.0,
            "% Caixa/PL": f"{fundo.perc_caixa_pl:.2f}%",
            "Taxas Devidas": fundo.devido_taxas or 0.0,
        }

        if fundo.cotista:
            detalhes["Cotista"] = fundo.cotista
    except AttributeError as e:
        # Fallback caso algum atributo não exista
        detalhes = {
            "Tipo": getattr(fundo, 'tipo', '-'),
            "PL Atual": getattr(fundo, 'pl', 0.0),
            "Erro": f"Erro ao carregar dados: {str(e)}"
        }

    return container_pagina(
        # Título
        html.h2(
            {"style": {"margin": "0 0 2rem 0", "color": "#333"}},
            f"📄 Lâmina de Fundo"
        ),

        # Seletor
        seletor,

        # Cabeçalho do fundo
        html.div(
            {
                "style": {
                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "color": "white",
                    "padding": "2rem",
                    "borderRadius": "15px",
                    "marginBottom": "2rem",
                }
            },
            html.h2(
                {"style": {"margin": "0", "color": "white"}},
                fundo_selecionado
            ),
            html.p(
                {"style": {"margin": "0.5rem 0 0 0", "opacity": "0.9"}},
                f"{fundo.tipo} • Data: {ultima_exec.data_relatorio.strftime('%d/%m/%Y')}"
            )
        ),

        # Métricas principais
        html.h3(
            {"style": {"margin": "2rem 0 1rem 0", "color": "#333"}},
            "💰 Métricas Principais"
        ),

        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                    "gap": "1.5rem",
                    "marginBottom": "2rem",
                }
            },
            card_metrica("Patrimônio Líquido", f"R$ {fundo.pl:,.2f}", fundo.variacao_d1, "primary", "💰"),
            card_metrica("Caixa Total", f"R$ {fundo.caixa_total:,.2f}", None, "success", "🏦"),
            card_metrica("% Caixa/PL", f"{fundo.perc_caixa_pl:.2f}%", None, "warning", "📊"),
            card_metrica("Taxas Devidas", f"R$ {fundo.devido_taxas:,.2f}", None, "info", "💳"),
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
                    "gridTemplateColumns": "repeat(auto-fit, minmax(400px, 1fr))",
                    "gap": "2rem",
                    "marginBottom": "2rem",
                }
            },
            grafico_evolucao(periodos, valores_pl, "Evolução do Patrimônio Líquido"),
            grafico_pizza(valores_comp, componentes, "Composição Patrimonial") if valores_comp and len(valores_comp) > 0 else None
        ) if valores_pl and len(valores_pl) > 0 else html.div(
            {
                "style": {
                    "padding": "2rem",
                    "textAlign": "center",
                    "color": "#999",
                    "background": "#f8f9fa",
                    "borderRadius": "12px",
                    "marginBottom": "2rem",
                }
            },
            html.p("Não há dados suficientes para exibir gráficos")
        ),

        # Alertas
        html.h3(
            {"style": {"margin": "2rem 0 1rem 0", "color": "#333"}},
            "⚠️ Análise e Alertas"
        ),

        html.div(
            {"style": {"marginBottom": "2rem"}},
            *(
                [
                    card_status(
                        f"{nivel.upper()}",
                        mensagem,
                        "error" if "error" in nivel.lower() or "crítico" in mensagem.lower() else "warning" if "warning" in nivel.lower() else "info"
                    )
                    for nivel, mensagem in fundo.get_alertas()
                ] if fundo.tem_alertas() else [
                    card_status("Sem Alertas", "Nenhum alerta identificado para este fundo", "success")
                ]
            )
        ),

        # Detalhes completos
        html.h3(
            {"style": {"margin": "2rem 0 1rem 0", "color": "#333"}},
            "📋 Detalhes Completos"
        ),

        tabela_detalhes(detalhes, fundo_selecionado)
    )
