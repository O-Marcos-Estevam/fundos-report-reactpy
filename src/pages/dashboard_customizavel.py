"""
Dashboard Customizável
Dashboard com widgets modulares e layout personalizável
"""

from typing import List, Dict, Any
from reactpy import component, html, use_state

from services.state_manager import get_state_manager
from services.preferences_manager import get_preferences_manager
from components.widgets import (
    widget_container,
    widget_kpi,
    widget_alertas,
    widget_top_fundos,
    widget_grafico_pizza,
    widget_grafico_barras,
    widget_health_score,
    widget_resumo_executivo
)
from models.fundo import FundoData


# ============================================================================
# MAPEAMENTO DE WIDGETS
# ============================================================================

def _render_widget(widget_config: Dict[str, Any], fundos: List[FundoData], on_fund_click):
    """Renderiza um widget baseado em sua configuração"""

    widget_type = widget_config.get("type")
    widget_id = widget_config.get("id")
    enabled = widget_config.get("enabled", True)

    if not enabled:
        return html.div()  # Widget desabilitado

    config = widget_config.get("config", {})

    # Mapa de widgets disponíveis
    if widget_type == "resumo_executivo":
        return widget_resumo_executivo(fundos, tamanho="xlarge")

    elif widget_type == "alertas":
        limite = config.get("limite", 5)
        return widget_alertas(fundos, limite=limite, tamanho="medium")

    elif widget_type == "top_fundos":
        criterio = config.get("criterio", "pl")
        limite = config.get("limite", 5)
        return widget_top_fundos(
            fundos,
            criterio=criterio,
            limite=limite,
            tamanho="medium",
            on_fund_click=on_fund_click
        )

    elif widget_type == "grafico_pizza":
        return widget_grafico_pizza(fundos, tamanho="medium")

    elif widget_type == "grafico_barras":
        criterio = config.get("criterio", "pl")
        limite = config.get("limite", 10)
        return widget_grafico_barras(
            fundos,
            criterio=criterio,
            limite=limite,
            tamanho="large"
        )

    elif widget_type == "health_score":
        limite = config.get("limite", 5)
        ordem = config.get("ordem", "desc")
        return widget_health_score(fundos, limite=limite, ordem=ordem, tamanho="medium")

    elif widget_type == "kpi_pl":
        total_pl = sum(f.pl for f in fundos)
        var_d1 = sum(f.variacao_d1 for f in fundos if f.variacao_d1) / len([f for f in fundos if f.variacao_d1]) if fundos else 0
        return widget_kpi(
            "Patrimônio Total",
            f"R$ {total_pl/1_000_000_000:.2f}B",
            icone="💰",
            variacao=var_d1,
            tamanho="small"
        )

    elif widget_type == "kpi_caixa":
        total_caixa = sum(f.caixa_total for f in fundos)
        return widget_kpi(
            "Caixa Total",
            f"R$ {total_caixa/1_000_000_000:.2f}B",
            icone="🏦",
            tamanho="small"
        )

    elif widget_type == "kpi_fundos":
        return widget_kpi(
            "Total de Fundos",
            str(len(fundos)),
            icone="📁",
            tamanho="small"
        )

    else:
        # Widget desconhecido
        return widget_container(
            titulo=f"Widget: {widget_type}",
            icone="❓",
            tamanho="medium",
            children=html.div(
                {"style": {"textAlign": "center", "padding": "2rem", "color": "#9ca3af"}},
                f"Tipo de widget '{widget_type}' não implementado"
            )
        )


# ============================================================================
# PAINEL DE CONFIGURAÇÃO
# ============================================================================

@component
def painel_configuracao_widgets(widgets_config: List[Dict[str, Any]], on_config_change):
    """Painel lateral para configurar widgets"""

    is_open, set_is_open = use_state(False)

    def toggle_widget(widget_id: str):
        prefs = get_preferences_manager()
        # Encontrar widget atual
        for w in widgets_config:
            if w["id"] == widget_id:
                prefs.toggle_widget(widget_id, not w.get("enabled", True))
                break
        on_config_change()

    def change_grid_columns(cols: int):
        prefs = get_preferences_manager()
        prefs.set_grid_columns(cols)
        on_config_change()

    prefs = get_preferences_manager()
    current_cols = prefs.get_grid_columns()

    return html.div(
        # Botão flutuante
        html.button(
            {
                "onClick": lambda e: set_is_open(not is_open),
                "style": {
                    "position": "fixed",
                    "bottom": "2rem",
                    "right": "2rem",
                    "width": "3.5rem",
                    "height": "3.5rem",
                    "borderRadius": "50%",
                    "border": "none",
                    "background": "#005D90",
                    "color": "white",
                    "fontSize": "1.5rem",
                    "cursor": "pointer",
                    "boxShadow": "0 4px 12px rgba(0,0,0,0.15)",
                    "zIndex": "1000",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center"
                }
            },
            "⚙️"
        ),

        # Painel lateral
        html.div(
            {
                "style": {
                    "position": "fixed",
                    "top": "0",
                    "right": "0" if is_open else "-400px",
                    "width": "400px",
                    "height": "100vh",
                    "background": "white",
                    "boxShadow": "-2px 0 8px rgba(0,0,0,0.1)",
                    "transition": "right 0.3s ease",
                    "zIndex": "999",
                    "overflowY": "auto",
                    "padding": "2rem"
                }
            },
            # Header
            html.div(
                {"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "2rem"}},
                html.h2({"style": {"margin": "0"}}, "⚙️ Configurações"),
                html.button(
                    {
                        "onClick": lambda e: set_is_open(False),
                        "style": {
                            "border": "none",
                            "background": "transparent",
                            "fontSize": "1.5rem",
                            "cursor": "pointer"
                        }
                    },
                    "✕"
                )
            ),

            # Seção: Grid Layout
            html.div(
                {"style": {"marginBottom": "2rem"}},
                html.h3({"style": {"fontSize": "1.125rem", "marginBottom": "1rem"}}, "Layout do Grid"),
                html.div(
                    {"style": {"display": "flex", "gap": "0.5rem"}},
                    *[
                        html.button(
                            {
                                "onClick": lambda e, c=cols: change_grid_columns(c),
                                "style": {
                                    "flex": "1",
                                    "padding": "0.75rem",
                                    "border": f"2px solid {'#005D90' if current_cols == cols else '#d1d5db'}",
                                    "background": "#f0f9ff" if current_cols == cols else "white",
                                    "borderRadius": "0.5rem",
                                    "cursor": "pointer",
                                    "fontWeight": "600"
                                }
                            },
                            f"{cols} colunas"
                        )
                        for cols in [1, 2, 3, 4]
                    ]
                )
            ),

            # Seção: Widgets
            html.div(
                html.h3({"style": {"fontSize": "1.125rem", "marginBottom": "1rem"}}, "Widgets Disponíveis"),
                html.div(
                    {"style": {"display": "flex", "flexDirection": "column", "gap": "0.75rem"}},
                    *[
                        html.div(
                            {
                                "style": {
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "alignItems": "center",
                                    "padding": "0.75rem",
                                    "background": "#f9fafb",
                                    "borderRadius": "0.5rem"
                                }
                            },
                            html.div(
                                {"style": {"fontWeight": "500"}},
                                widget.get("id", "Widget").replace("_", " ").title()
                            ),
                            html.label(
                                {
                                    "style": {
                                        "position": "relative",
                                        "display": "inline-block",
                                        "width": "3rem",
                                        "height": "1.5rem"
                                    }
                                },
                                html.input({
                                    "type": "checkbox",
                                    "checked": widget.get("enabled", True),
                                    "onChange": lambda e, wid=widget["id"]: toggle_widget(wid),
                                    "style": {"display": "none"}
                                }),
                                html.span(
                                    {
                                        "style": {
                                            "position": "absolute",
                                            "cursor": "pointer",
                                            "top": "0",
                                            "left": "0",
                                            "right": "0",
                                            "bottom": "0",
                                            "background": "#10b981" if widget.get("enabled", True) else "#d1d5db",
                                            "borderRadius": "1.5rem",
                                            "transition": "0.3s"
                                        }
                                    },
                                    html.span(
                                        {
                                            "style": {
                                                "position": "absolute",
                                                "content": "",
                                                "height": "1.125rem",
                                                "width": "1.125rem",
                                                "left": "0.1875rem" if not widget.get("enabled", True) else "1.6875rem",
                                                "bottom": "0.1875rem",
                                                "background": "white",
                                                "borderRadius": "50%",
                                                "transition": "0.3s"
                                            }
                                        }
                                    )
                                )
                            )
                        )
                        for widget in widgets_config
                    ]
                )
            ),

            # Botão de reset
            html.div(
                {"style": {"marginTop": "2rem", "paddingTop": "2rem", "borderTop": "1px solid #e5e7eb"}},
                html.button(
                    {
                        "onClick": lambda e: reset_preferences(),
                        "style": {
                            "width": "100%",
                            "padding": "0.75rem",
                            "border": "1px solid #ef4444",
                            "background": "white",
                            "color": "#ef4444",
                            "borderRadius": "0.5rem",
                            "cursor": "pointer",
                            "fontWeight": "600"
                        }
                    },
                    "🔄 Restaurar Padrões"
                )
            )
        )
    )

    def reset_preferences():
        prefs = get_preferences_manager()
        prefs.reset_to_defaults()
        on_config_change()
        set_is_open(False)


# ============================================================================
# COMPONENTE PRINCIPAL
# ============================================================================

@component
def pagina_dashboard_customizavel():
    """Dashboard customizável com widgets modulares"""

    state_manager = get_state_manager()
    prefs_manager = get_preferences_manager()

    # Estado local
    refresh_key, set_refresh_key = use_state(0)
    fundo_selecionado, set_fundo_selecionado = use_state(None)

    def refresh():
        set_refresh_key(refresh_key + 1)

    def handle_fund_click(fundo: FundoData):
        set_fundo_selecionado(fundo)
        # TODO: Abrir modal de detalhes

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
                "Execute um relatório para visualizar o dashboard customizável."
            )
        )

    # Processar fundos
    fundos = list(ultima_exec.fundos.values())

    # Obter configuração de widgets
    widgets_config = prefs_manager.get_dashboard_widgets()
    grid_columns = prefs_manager.get_grid_columns()

    return html.div(
        {"class": "dashboard-customizavel animate-fade-in"},

        # Painel de configuração
        painel_configuracao_widgets(widgets_config, refresh),

        # Header
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
                    "📊 Dashboard Customizável"
                ),
                html.p(
                    {"style": {"margin": "0.5rem 0 0 0", "color": "#6b7280"}},
                    f"Última atualização: {ultima_exec.data_relatorio.strftime('%d/%m/%Y %H:%M')} • {len([w for w in widgets_config if w.get('enabled', True)])} widgets ativos"
                )
            ),
            html.div(
                {"style": {"display": "flex", "gap": "0.75rem"}},
                html.button(
                    {
                        "onClick": lambda e: refresh(),
                        "class": "btn btn-outline",
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
                )
            )
        ),

        # Grid de widgets
        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": f"repeat({grid_columns}, 1fr)",
                    "gap": "1.5rem",
                    "gridAutoRows": "minmax(auto, auto)"
                }
            },
            *[
                _render_widget(widget, fundos, handle_fund_click)
                for widget in widgets_config
                if widget.get("enabled", True)
            ]
        ),

        # Informações adicionais
        html.div(
            {
                "style": {
                    "marginTop": "3rem",
                    "padding": "1.5rem",
                    "background": "#f0f9ff",
                    "borderRadius": "0.75rem",
                    "textAlign": "center"
                }
            },
            html.div(
                {"style": {"fontSize": "2rem", "marginBottom": "0.5rem"}},
                "⚙️"
            ),
            html.p(
                {"style": {"margin": "0", "color": "#1e40af", "fontWeight": "500"}},
                "Clique no botão de configuração para personalizar seu dashboard"
            )
        )
    )
