"""
Componentes de Gráficos
Wrappers para gráficos Plotly
"""

from reactpy import component, html
from typing import List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px

from app.config import AppConfig


@component
def grafico_pizza(
    valores: List[float],
    labels: List[str],
    titulo: str = "Distribuição",
    altura: int = 400
):
    """
    Gráfico de pizza (donut chart)

    Args:
        valores: Lista de valores
        labels: Lista de labels
        titulo: Título do gráfico
        altura: Altura em pixels
    """
    if not valores or not labels:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem dados para exibir"
        )

    fig = px.pie(
        values=valores,
        names=labels,
        title=titulo,
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Purples_r
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Percentual: %{percent}<extra></extra>'
    )

    fig.update_layout(
        height=altura,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        )
    )

    html_chart = fig.to_html(include_plotlyjs='cdn', div_id=f'chart-pizza-{id(fig)}')

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
def grafico_barras(
    valores: List[float],
    labels: List[str],
    titulo: str = "Comparação",
    horizontal: bool = True,
    altura: int = 400
):
    """
    Gráfico de barras

    Args:
        valores: Lista de valores
        labels: Lista de labels
        titulo: Título do gráfico
        horizontal: Se True, barras horizontais
        altura: Altura em pixels
    """
    if not valores or not labels:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem dados para exibir"
        )

    if horizontal:
        fig = go.Figure(data=[
            go.Bar(
                x=valores,
                y=labels,
                orientation='h',
                marker_color=AppConfig.get_color('primary'),
                hovertemplate='<b>%{y}</b><br>Valor: R$ %{x:,.2f}<extra></extra>'
            )
        ])
        fig.update_layout(xaxis_title="Valor (R$)", yaxis_title="")
    else:
        fig = go.Figure(data=[
            go.Bar(
                x=labels,
                y=valores,
                marker_color=AppConfig.get_color('primary'),
                hovertemplate='<b>%{x}</b><br>Valor: R$ %{y:,.2f}<extra></extra>'
            )
        ])
        fig.update_layout(xaxis_title="", yaxis_title="Valor (R$)")

    fig.update_layout(
        title=titulo,
        height=altura,
        margin=dict(l=50, r=50, t=50, b=50),
        template='plotly_white'
    )

    html_chart = fig.to_html(include_plotlyjs='cdn', div_id=f'chart-barras-{id(fig)}')

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
def grafico_linha(
    dados: Dict[str, List[float]],
    labels_x: List[str],
    titulo: str = "Evolução",
    altura: int = 400
):
    """
    Gráfico de linha (múltiplas séries)

    Args:
        dados: Dicionário {nome_serie: [valores]}
        labels_x: Labels do eixo X
        titulo: Título do gráfico
        altura: Altura em pixels
    """
    if not dados or not labels_x:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem dados para exibir"
        )

    fig = go.Figure()

    cores = px.colors.qualitative.Set2

    for idx, (nome, valores) in enumerate(dados.items()):
        cor = cores[idx % len(cores)]
        fig.add_trace(go.Scatter(
            x=labels_x,
            y=valores,
            mode='lines+markers',
            name=nome,
            line=dict(width=2, color=cor),
            marker=dict(size=6),
            hovertemplate=f'<b>{nome}</b><br>%{{x}}<br>Valor: R$ %{{y:,.2f}}<extra></extra>'
        ))

    fig.update_layout(
        title=titulo,
        xaxis_title="Período",
        yaxis_title="Valor (R$)",
        height=altura,
        hovermode='x unified',
        template='plotly_white',
        margin=dict(l=50, r=50, t=50, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    html_chart = fig.to_html(include_plotlyjs='cdn', div_id=f'chart-linha-{id(fig)}')

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
def grafico_evolucao(
    periodos: List[str],
    valores: List[float],
    titulo: str = "Evolução do Patrimônio",
    altura: int = 350
):
    """
    Gráfico específico para evolução de PL

    Args:
        periodos: Lista de períodos (ex: ['Atual', 'D-1', 'D-7', 'D-30'])
        valores: Lista de valores correspondentes
        titulo: Título do gráfico
        altura: Altura em pixels
    """
    if not periodos or not valores:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem dados para exibir"
        )

    fig = px.line(
        x=periodos,
        y=valores,
        title=titulo,
        markers=True,
        color_discrete_sequence=[AppConfig.get_color('primary')]
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=10),
        hovertemplate='<b>%{x}</b><br>PL: R$ %{y:,.2f}<extra></extra>'
    )

    fig.update_layout(
        yaxis_title="PL (R$)",
        xaxis_title="Período",
        height=altura,
        template='plotly_white',
        margin=dict(l=50, r=50, t=50, b=50)
    )

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
def grafico_timeline(dados: Dict[str, int], titulo: str = "Execuções ao Longo do Tempo"):
    """
    Gráfico de linha temporal (para histórico)

    Args:
        dados: Dicionário {data: quantidade}
        titulo: Título do gráfico
    """
    if not dados:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem dados para exibir"
        )

    datas = list(dados.keys())
    quantidades = list(dados.values())

    fig = px.line(
        x=datas,
        y=quantidades,
        title=titulo,
        markers=True
    )

    fig.update_traces(
        line=dict(width=2, color=AppConfig.get_color('info')),
        marker=dict(size=8)
    )

    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Nº de Execuções",
        height=350,
        template='plotly_white'
    )

    html_chart = fig.to_html(include_plotlyjs='cdn', div_id=f'chart-timeline-{id(fig)}')

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
            "style": {"width": "100%", "height": "400px", "border": "none"}
        })
    )
