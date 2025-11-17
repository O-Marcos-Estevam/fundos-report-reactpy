"""
Gráficos Avançados
Visualizações complexas e interativas com Plotly
"""

from reactpy import component, html
from typing import List, Dict, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from models.fundo import FundoData


@component
def grafico_evolucao_temporal(
    fundos: List[FundoData],
    titulo: str = "Evolução do Patrimônio Líquido",
    altura: int = 450,
    mostrar_legenda: bool = True
):
    """
    Gráfico de linha multi-série mostrando evolução temporal do PL

    Args:
        fundos: Lista de fundos a visualizar
        titulo: Título do gráfico
        altura: Altura em pixels
        mostrar_legenda: Se deve mostrar legenda
    """
    if not fundos:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Selecione fundos para visualizar a evolução"
        )

    fig = go.Figure()

    # Cores para as linhas
    cores = px.colors.qualitative.Set2

    for idx, fundo in enumerate(fundos[:6]):  # Limitar a 6 fundos
        # Preparar dados de evolução (D-30, D-7, D-1, Atual)
        periodos = []
        valores = []

        # D-30
        if fundo.pl_d30 > 0:
            periodos.append("D-30")
            valores.append(fundo.pl_d30)

        # D-7
        if fundo.pl_d7 > 0:
            periodos.append("D-7")
            valores.append(fundo.pl_d7)

        # D-1
        if fundo.pl_d1 > 0:
            periodos.append("D-1")
            valores.append(fundo.pl_d1)

        # Atual
        periodos.append("Atual")
        valores.append(fundo.pl)

        # Adicionar linha
        cor = cores[idx % len(cores)]
        fig.add_trace(go.Scatter(
            x=periodos,
            y=valores,
            mode='lines+markers',
            name=fundo.nome[:30],  # Truncar nome
            line=dict(width=3, color=cor),
            marker=dict(size=8),
            hovertemplate=f'<b>{fundo.nome}</b><br>%{{x}}<br>PL: R$ %{{y:,.2f}}<extra></extra>'
        ))

    fig.update_layout(
        title=titulo,
        xaxis_title="Período",
        yaxis_title="Patrimônio Líquido (R$)",
        height=altura,
        hovermode='x unified',
        template='plotly_white',
        margin=dict(l=80, r=50, t=80, b=50),
        legend=dict(
            orientation="h" if mostrar_legenda else "v",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ) if mostrar_legenda else dict(visible=False)
    )

    # Formatar eixo Y para valores grandes
    fig.update_yaxes(tickformat=".2s")

    html_chart = fig.to_html(include_plotlyjs='cdn', div_id=f'chart-evolucao-{id(fig)}')

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "1rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
            }
        },
        html.iframe({
            "srcDoc": html_chart,
            "style": {
                "width": "100%",
                "height": f"{altura + 50}px",
                "border": "none"
            }
        })
    )


@component
def grafico_area_stacked(
    fundos_por_tipo: Dict[str, List[FundoData]],
    titulo: str = "Evolução por Tipo de Fundo",
    altura: int = 450
):
    """
    Gráfico de área empilhada mostrando evolução por tipo

    Args:
        fundos_por_tipo: Dicionário {tipo: [fundos]}
        titulo: Título do gráfico
        altura: Altura em pixels
    """
    if not fundos_por_tipo:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem dados para exibir"
        )

    fig = go.Figure()

    periodos = ["D-30", "D-7", "D-1", "Atual"]

    for tipo, fundos in fundos_por_tipo.items():
        valores = []

        for periodo in periodos:
            if periodo == "D-30":
                total = sum(f.pl_d30 for f in fundos if f.pl_d30 > 0)
            elif periodo == "D-7":
                total = sum(f.pl_d7 for f in fundos if f.pl_d7 > 0)
            elif periodo == "D-1":
                total = sum(f.pl_d1 for f in fundos if f.pl_d1 > 0)
            else:  # Atual
                total = sum(f.pl for f in fundos)

            valores.append(total)

        fig.add_trace(go.Scatter(
            x=periodos,
            y=valores,
            mode='lines',
            name=tipo,
            stackgroup='one',
            fillcolor='tonexty',
            hovertemplate=f'<b>{tipo}</b><br>%{{x}}<br>Total: R$ %{{y:,.2f}}<extra></extra>'
        ))

    fig.update_layout(
        title=titulo,
        xaxis_title="Período",
        yaxis_title="Patrimônio Líquido Total (R$)",
        height=altura,
        hovermode='x unified',
        template='plotly_white',
        margin=dict(l=80, r=50, t=80, b=50),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        )
    )

    fig.update_yaxes(tickformat=".2s")

    html_chart = fig.to_html(include_plotlyjs='cdn', div_id=f'chart-area-{id(fig)}')

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "1rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
            }
        },
        html.iframe({
            "srcDoc": html_chart,
            "style": {
                "width": "100%",
                "height": f"{altura + 50}px",
                "border": "none"
            }
        })
    )


@component
def grafico_treemap(
    fundos_por_tipo: Dict[str, List[FundoData]],
    titulo: str = "Distribuição Hierárquica de Patrimônio",
    altura: int = 500
):
    """
    Treemap mostrando distribuição hierárquica

    Args:
        fundos_por_tipo: Dicionário {tipo: [fundos]}
        titulo: Título do gráfico
        altura: Altura em pixels
    """
    if not fundos_por_tipo:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem dados para exibir"
        )

    # Preparar dados para treemap
    labels = ["Total"]
    parents = [""]
    values = [0]
    colors = []

    # Adicionar tipos
    for tipo, fundos in fundos_por_tipo.items():
        total_tipo = sum(f.pl for f in fundos)
        labels.append(tipo)
        parents.append("Total")
        values.append(total_tipo)
        colors.append(total_tipo)

        # Adicionar fundos individuais (top 5 por tipo)
        top_fundos = sorted(fundos, key=lambda f: f.pl, reverse=True)[:5]
        for fundo in top_fundos:
            labels.append(fundo.nome[:25])
            parents.append(tipo)
            values.append(fundo.pl)
            colors.append(fundo.variacao_d1)

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colorscale='RdYlGn',
            cmid=0,
            colorbar=dict(title="Var. D-1 (%)")
        ),
        textposition="middle center",
        hovertemplate='<b>%{label}</b><br>PL: R$ %{value:,.2f}<br>Var: %{color:.2f}%<extra></extra>'
    ))

    fig.update_layout(
        title=titulo,
        height=altura,
        margin=dict(l=10, r=10, t=50, b=10)
    )

    html_chart = fig.to_html(include_plotlyjs='cdn', div_id=f'chart-treemap-{id(fig)}')

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "1rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
            }
        },
        html.iframe({
            "srcDoc": html_chart,
            "style": {
                "width": "100%",
                "height": f"{altura + 50}px",
                "border": "none"
            }
        })
    )


@component
def grafico_waterfall(
    fundo: FundoData,
    titulo: Optional[str] = None,
    altura: int = 400
):
    """
    Gráfico waterfall mostrando variações do PL

    Args:
        fundo: Fundo para visualizar
        titulo: Título do gráfico (usa nome do fundo se None)
        altura: Altura em pixels
    """
    if not fundo:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Selecione um fundo"
        )

    titulo = titulo or f"Evolução de {fundo.nome}"

    # Calcular variações
    var_d30_d7 = fundo.pl_d7 - fundo.pl_d30 if fundo.pl_d30 > 0 and fundo.pl_d7 > 0 else 0
    var_d7_d1 = fundo.pl_d1 - fundo.pl_d7 if fundo.pl_d7 > 0 and fundo.pl_d1 > 0 else 0
    var_d1_atual = fundo.pl - fundo.pl_d1 if fundo.pl_d1 > 0 else 0

    fig = go.Figure(go.Waterfall(
        name="PL",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["D-30", "Var D-30→D-7", "Var D-7→D-1", "Var D-1→Atual", "PL Atual"],
        y=[fundo.pl_d30 if fundo.pl_d30 > 0 else fundo.pl * 0.9,
           var_d30_d7, var_d7_d1, var_d1_atual, fundo.pl],
        text=[
            f"R$ {fundo.pl_d30:,.0f}" if fundo.pl_d30 > 0 else "N/A",
            f"+R$ {var_d30_d7:,.0f}" if var_d30_d7 >= 0 else f"R$ {var_d30_d7:,.0f}",
            f"+R$ {var_d7_d1:,.0f}" if var_d7_d1 >= 0 else f"R$ {var_d7_d1:,.0f}",
            f"+R$ {var_d1_atual:,.0f}" if var_d1_atual >= 0 else f"R$ {var_d1_atual:,.0f}",
            f"R$ {fundo.pl:,.0f}"
        ],
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#10b981"}},
        decreasing={"marker": {"color": "#ef4444"}},
        totals={"marker": {"color": "#005D90"}}
    ))

    fig.update_layout(
        title=titulo,
        yaxis_title="Patrimônio Líquido (R$)",
        height=altura,
        template='plotly_white',
        margin=dict(l=80, r=50, t=80, b=50),
        showlegend=False
    )

    fig.update_yaxes(tickformat=".2s")

    html_chart = fig.to_html(include_plotlyjs='cdn', div_id=f'chart-waterfall-{id(fig)}')

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "1rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
            }
        },
        html.iframe({
            "srcDoc": html_chart,
            "style": {
                "width": "100%",
                "height": f"{altura + 50}px",
                "border": "none"
            }
        })
    )


@component
def grafico_scatter_pl_vs_var(
    fundos: List[FundoData],
    titulo: str = "PL vs Variação D-1",
    altura: int = 500
):
    """
    Scatter plot mostrando relação entre PL e variação

    Args:
        fundos: Lista de fundos
        titulo: Título do gráfico
        altura: Altura em pixels
    """
    if not fundos:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem dados para exibir"
        )

    # Preparar dados
    nomes = [f.nome[:30] for f in fundos]
    pls = [f.pl for f in fundos]
    vars_d1 = [f.variacao_d1 for f in fundos]
    tipos = [f.tipo for f in fundos]
    caixas = [f.perc_caixa_pl for f in fundos]

    fig = go.Figure()

    # Agrupar por tipo para cores diferentes
    tipos_unicos = list(set(tipos))
    cores = px.colors.qualitative.Set2

    for idx, tipo in enumerate(tipos_unicos):
        # Filtrar fundos deste tipo
        indices = [i for i, t in enumerate(tipos) if t == tipo]

        fig.add_trace(go.Scatter(
            x=[pls[i] for i in indices],
            y=[vars_d1[i] for i in indices],
            mode='markers',
            name=tipo,
            marker=dict(
                size=[caixas[i]/2 for i in indices],  # Tamanho proporcional ao % caixa
                color=cores[idx % len(cores)],
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            text=[nomes[i] for i in indices],
            hovertemplate='<b>%{text}</b><br>PL: R$ %{x:,.2f}<br>Var D-1: %{y:.2f}%<extra></extra>'
        ))

    fig.update_layout(
        title=titulo,
        xaxis_title="Patrimônio Líquido (R$)",
        yaxis_title="Variação D-1 (%)",
        height=altura,
        template='plotly_white',
        margin=dict(l=80, r=50, t=80, b=50),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        hovermode='closest'
    )

    # Adicionar linhas de referência
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_xaxes(tickformat=".2s")

    html_chart = fig.to_html(include_plotlyjs='cdn', div_id=f'chart-scatter-{id(fig)}')

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "1rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
            }
        },
        html.iframe({
            "srcDoc": html_chart,
            "style": {
                "width": "100%",
                "height": f"{altura + 50}px",
                "border": "none"
            }
        })
    )


@component
def grafico_heatmap_correlacao(
    fundos: List[FundoData],
    titulo: str = "Mapa de Calor - Performance",
    altura: int = 400
):
    """
    Heatmap mostrando performance dos fundos

    Args:
        fundos: Lista de fundos
        titulo: Título do gráfico
        altura: Altura em pixels
    """
    if not fundos:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem dados para exibir"
        )

    # Limitar a 20 fundos
    fundos_sorted = sorted(fundos, key=lambda f: f.pl, reverse=True)[:20]

    nomes = [f.nome[:20] for f in fundos_sorted]
    periodos = ["D-30", "D-7", "D-1"]

    # Preparar matriz de variações
    valores = []
    for fundo in fundos_sorted:
        valores.append([fundo.variacao_d30, fundo.variacao_d7, fundo.variacao_d1])

    fig = go.Figure(data=go.Heatmap(
        z=valores,
        x=periodos,
        y=nomes,
        colorscale='RdYlGn',
        zmid=0,
        text=[[f"{v:.2f}%" for v in row] for row in valores],
        texttemplate="%{text}",
        textfont={"size": 10},
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.2f}%<extra></extra>',
        colorbar=dict(title="Variação (%)")
    ))

    fig.update_layout(
        title=titulo,
        xaxis_title="Período",
        height=altura,
        template='plotly_white',
        margin=dict(l=150, r=50, t=80, b=50)
    )

    html_chart = fig.to_html(include_plotlyjs='cdn', div_id=f'chart-heatmap-{id(fig)}')

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "1rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
            }
        },
        html.iframe({
            "srcDoc": html_chart,
            "style": {
                "width": "100%",
                "height": f"{altura + 50}px",
                "border": "none"
            }
        })
    )
