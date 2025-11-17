"""
Componentes de Tabelas
Tabelas com dados de fundos, histórico e detalhes
"""

from reactpy import component, html
from typing import List, Dict, Any
from models.fundo import FundoData
from models.historico import HistoricoEntry
from app.config import AppConfig


@component
def tabela_fundos(fundos: List[FundoData], mostrar_alertas: bool = False):
    """
    Tabela com dados de fundos

    Args:
        fundos: Lista de fundos
        mostrar_alertas: Se True, mostra coluna de alertas
    """
    if not fundos:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Nenhum fundo para exibir"
        )

    def render_linha(fundo: FundoData):
        """Renderiza uma linha da tabela"""
        cor_variacao = AppConfig.get_color('success') if fundo.variacao_d1 > 0 else AppConfig.get_color('error') if fundo.variacao_d1 < 0 else "#999"

        colunas = [
            # Nome
            html.td(
                {"style": {"padding": "12px", "fontWeight": "600"}},
                fundo.nome
            ),
            # Tipo
            html.td(
                {"style": {"padding": "12px"}},
                html.span(
                    {
                        "style": {
                            "background": AppConfig.get_color('primary'),
                            "color": "white",
                            "padding": "0.25rem 0.75rem",
                            "borderRadius": "12px",
                            "fontSize": "0.85rem",
                            "fontWeight": "600",
                        }
                    },
                    fundo.tipo
                )
            ),
            # PL
            html.td(
                {"style": {"padding": "12px", "textAlign": "right"}},
                f"R$ {fundo.pl:,.2f}"
            ),
            # Caixa
            html.td(
                {"style": {"padding": "12px", "textAlign": "right"}},
                f"R$ {fundo.caixa_total:,.2f}"
            ),
            # % Caixa/PL
            html.td(
                {"style": {"padding": "12px", "textAlign": "right"}},
                f"{fundo.perc_caixa_pl:.2f}%"
            ),
            # Variação D-1
            html.td(
                {
                    "style": {
                        "padding": "12px",
                        "textAlign": "right",
                        "color": cor_variacao,
                        "fontWeight": "600",
                    }
                },
                f"{fundo.variacao_d1:+.2f}%"
            ),
        ]

        # Adicionar alertas se solicitado
        if mostrar_alertas:
            if fundo.tem_alertas():
                alertas = fundo.get_alertas()
                colunas.append(
                    html.td(
                        {"style": {"padding": "12px"}},
                        html.span(
                            {
                                "style": {
                                    "background": AppConfig.get_color('warning'),
                                    "color": "white",
                                    "padding": "0.25rem 0.5rem",
                                    "borderRadius": "8px",
                                    "fontSize": "0.8rem",
                                }
                            },
                            f"⚠️ {len(alertas)}"
                        )
                    )
                )
            else:
                colunas.append(
                    html.td(
                        {"style": {"padding": "12px", "textAlign": "center"}},
                        html.span({"style": {"color": "#999"}}, "✅")
                    )
                )

        return html.tr(
            {"key": fundo.nome, "style": {"border_bottom": "1px solid #eee"}},
            *colunas
        )

    # Headers
    headers = ["Fundo", "Tipo", "PL", "Caixa", "% Caixa/PL", "Var. D-1"]
    if mostrar_alertas:
        headers.append("Alertas")

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "1rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
                "overflow": "auto",
            }
        },
        html.table(
            {"style": {"width": "100%", "border_collapse": "collapse"}},
            # Header
            html.thead(
                html.tr(
                    {"style": {"background": "#f5f5f5"}},
                    *[
                        html.th(
                            {
                                "key": h,
                                "style": {
                                    "padding": "12px",
                                    "textAlign": "left" if h in ["Fundo", "Tipo"] else "right" if h != "Alertas" else "center",
                                    "border_bottom": "2px solid #ddd",
                                    "fontWeight": "700",
                                    "color": "#333",
                                }
                            },
                            h
                        )
                        for h in headers
                    ]
                )
            ),
            # Body
            html.tbody(*[render_linha(fundo) for fundo in fundos])
        )
    )


@component
def tabela_historico(historico: List[HistoricoEntry]):
    """
    Tabela com histórico de execuções

    Args:
        historico: Lista de entradas do histórico
    """
    if not historico:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Nenhum histórico disponível"
        )

    def render_linha(entry: HistoricoEntry):
        """Renderiza uma linha do histórico"""
        cor_status = AppConfig.get_color('success') if entry.sucesso else AppConfig.get_color('error')
        icone_status = "✅" if entry.sucesso else "❌"

        return html.tr(
            {"key": entry.timestamp.isoformat(), "style": {"border_bottom": "1px solid #eee"}},
            # Status
            html.td(
                {"style": {"padding": "12px", "textAlign": "center"}},
                html.span(
                    {"style": {"fontSize": "1.2rem"}},
                    icone_status
                )
            ),
            # Timestamp
            html.td(
                {"style": {"padding": "12px"}},
                entry.data_formatada
            ),
            # Data Relatório
            html.td(
                {"style": {"padding": "12px"}},
                entry.data_relatorio
            ),
            # Fundos
            html.td(
                {"style": {"padding": "12px", "textAlign": "center"}},
                str(entry.fundos_processados)
            ),
            # Tempo
            html.td(
                {"style": {"padding": "12px", "textAlign": "right"}},
                f"{entry.tempo_execucao:.1f}s"
            ),
            # Status
            html.td(
                {
                    "style": {
                        "padding": "12px",
                        "color": cor_status,
                        "fontWeight": "600",
                    }
                },
                entry.status.upper()
            ),
        )

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "1rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
                "overflow": "auto",
            }
        },
        html.table(
            {"style": {"width": "100%", "border_collapse": "collapse"}},
            # Header
            html.thead(
                html.tr(
                    {"style": {"background": "#f5f5f5"}},
                    html.th(
                        {"style": {"padding": "12px", "textAlign": "center", "border_bottom": "2px solid #ddd"}},
                        "Status"
                    ),
                    html.th(
                        {"style": {"padding": "12px", "textAlign": "left", "border_bottom": "2px solid #ddd"}},
                        "Data/Hora"
                    ),
                    html.th(
                        {"style": {"padding": "12px", "textAlign": "left", "border_bottom": "2px solid #ddd"}},
                        "Data Relatório"
                    ),
                    html.th(
                        {"style": {"padding": "12px", "textAlign": "center", "border_bottom": "2px solid #ddd"}},
                        "Fundos"
                    ),
                    html.th(
                        {"style": {"padding": "12px", "textAlign": "right", "border_bottom": "2px solid #ddd"}},
                        "Tempo"
                    ),
                    html.th(
                        {"style": {"padding": "12px", "textAlign": "left", "border_bottom": "2px solid #ddd"}},
                        "Resultado"
                    ),
                )
            ),
            # Body
            html.tbody(*[render_linha(entry) for entry in historico])
        )
    )


@component
def tabela_detalhes(dados: Dict[str, Any], titulo: str = "Detalhes"):
    """
    Tabela chave-valor para exibir detalhes

    Args:
        dados: Dicionário com dados
        titulo: Título da tabela
    """
    if not dados:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem detalhes disponíveis"
        )

    def formatar_valor(valor: Any) -> str:
        """Formata valor para exibição"""
        if isinstance(valor, float):
            return f"R$ {valor:,.2f}" if valor > 1000 else f"{valor:.2f}"
        elif isinstance(valor, (int, bool)):
            return str(valor)
        elif valor is None:
            return "-"
        else:
            return str(valor)

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "1.5rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
            }
        },
        html.h3(
            {"style": {"margin": "0 0 1rem 0", "color": "#333"}},
            titulo
        ),
        html.table(
            {"style": {"width": "100%", "border_collapse": "collapse"}},
            html.tbody(
                *[
                    html.tr(
                        {
                            "key": chave,
                            "style": {"border_bottom": "1px solid #eee"}
                        },
                        html.td(
                            {
                                "style": {
                                    "padding": "12px",
                                    "fontWeight": "600",
                                    "color": "#666",
                                    "width": "40%",
                                }
                            },
                            chave
                        ),
                        html.td(
                            {"style": {"padding": "12px", "color": "#333"}},
                            formatar_valor(valor)
                        ),
                    )
                    for chave, valor in dados.items()
                ]
            )
        )
    )


@component
def tabela_simples(headers: List[str], rows: List[List[Any]]):
    """
    Tabela simples genérica

    Args:
        headers: Lista de cabeçalhos
        rows: Lista de linhas (cada linha é uma lista de valores)
    """
    if not rows:
        return html.div(
            {"style": {"padding": "2rem", "textAlign": "center", "color": "#999"}},
            "Sem dados para exibir"
        )

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "1rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
                "overflow": "auto",
            }
        },
        html.table(
            {"style": {"width": "100%", "border_collapse": "collapse"}},
            # Header
            html.thead(
                html.tr(
                    {"style": {"background": "#f5f5f5"}},
                    *[
                        html.th(
                            {
                                "key": f"h-{i}",
                                "style": {
                                    "padding": "12px",
                                    "textAlign": "left",
                                    "border_bottom": "2px solid #ddd",
                                    "fontWeight": "700",
                                }
                            },
                            h
                        )
                        for i, h in enumerate(headers)
                    ]
                )
            ),
            # Body
            html.tbody(
                *[
                    html.tr(
                        {"key": f"r-{i}", "style": {"border_bottom": "1px solid #eee"}},
                        *[
                            html.td(
                                {"key": f"c-{i}-{j}", "style": {"padding": "12px"}},
                                str(cell)
                            )
                            for j, cell in enumerate(row)
                        ]
                    )
                    for i, row in enumerate(rows)
                ]
            )
        )
    )
