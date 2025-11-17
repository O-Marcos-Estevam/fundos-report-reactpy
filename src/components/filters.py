"""
Componentes de Filtro Avançados
Filtros interativos para dashboard
"""

from reactpy import component, html, use_state
from typing import List, Dict, Callable, Optional, Any


@component
def multi_select_dropdown(
    label: str,
    options: List[Dict[str, str]],
    selected: List[str],
    on_change: Callable,
    icon: str = "🔽"
):
    """
    Dropdown multi-seleção

    Args:
        label: Label do dropdown
        options: Lista de {label, value, icon?}
        selected: Lista de valores selecionados
        on_change: Callback(new_selected_list)
        icon: Ícone do dropdown
    """
    is_open, set_is_open = use_state(False)

    def toggle_option(value: str):
        """Toggle seleção de uma opção"""
        if value in selected:
            new_selected = [v for v in selected if v != value]
        else:
            new_selected = selected + [value]
        on_change(new_selected)

    def clear_all():
        """Limpa todas as seleções"""
        on_change([])
        set_is_open(False)

    def select_all():
        """Seleciona todas as opções"""
        all_values = [opt['value'] for opt in options]
        on_change(all_values)

    return html.div(
        {
            "style": {
                "position": "relative",
                "display": "inline-block",
                "minWidth": "200px"
            }
        },
        # Botão do dropdown
        html.button(
            {
                "onClick": lambda e: set_is_open(not is_open),
                "style": {
                    "width": "100%",
                    "padding": "0.625rem 1rem",
                    "borderRadius": "0.5rem",
                    "border": "2px solid #e5e7eb",
                    "background": "white",
                    "cursor": "pointer",
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "fontSize": "0.875rem",
                    "fontWeight": "500",
                    "transition": "all 0.2s"
                }
            },
            html.span(f"{icon} {label}"),
            html.span(
                {
                    "style": {
                        "background": "#eff6ff",
                        "color": "#1e40af",
                        "padding": "0.125rem 0.5rem",
                        "borderRadius": "9999px",
                        "fontSize": "0.75rem",
                        "fontWeight": "600"
                    }
                },
                str(len(selected))
            ) if selected else html.span()
        ),

        # Menu dropdown
        html.div(
            {
                "style": {
                    "display": "block" if is_open else "none",
                    "position": "absolute",
                    "top": "calc(100% + 0.5rem)",
                    "left": "0",
                    "right": "0",
                    "background": "white",
                    "borderRadius": "0.75rem",
                    "boxShadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                    "border": "1px solid #e5e7eb",
                    "zIndex": "50",
                    "maxHeight": "300px",
                    "overflow": "auto"
                }
            },
            # Header com ações
            html.div(
                {
                    "style": {
                        "padding": "0.75rem",
                        "borderBottom": "1px solid #e5e7eb",
                        "display": "flex",
                        "gap": "0.5rem",
                        "background": "#f9fafb"
                    }
                },
                html.button(
                    {
                        "onClick": lambda e: select_all(),
                        "style": {
                            "flex": "1",
                            "padding": "0.375rem",
                            "fontSize": "0.75rem",
                            "borderRadius": "0.375rem",
                            "border": "1px solid #d1d5db",
                            "background": "white",
                            "cursor": "pointer"
                        }
                    },
                    "Todos"
                ),
                html.button(
                    {
                        "onClick": lambda e: clear_all(),
                        "style": {
                            "flex": "1",
                            "padding": "0.375rem",
                            "fontSize": "0.75rem",
                            "borderRadius": "0.375rem",
                            "border": "1px solid #d1d5db",
                            "background": "white",
                            "cursor": "pointer"
                        }
                    },
                    "Limpar"
                )
            ),

            # Lista de opções
            html.div(
                {"style": {"padding": "0.5rem"}},
                *[
                    html.label(
                        {
                            "key": opt['value'],
                            "style": {
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "0.75rem",
                                "padding": "0.625rem 0.75rem",
                                "borderRadius": "0.5rem",
                                "cursor": "pointer",
                                "transition": "background 0.2s",
                                "background": "#eff6ff" if opt['value'] in selected else "transparent"
                            },
                            "onClick": lambda e, v=opt['value']: toggle_option(v)
                        },
                        html.input({
                            "type": "checkbox",
                            "checked": opt['value'] in selected,
                            "style": {
                                "width": "1rem",
                                "height": "1rem",
                                "cursor": "pointer"
                            }
                        }),
                        html.span(
                            {"style": {"fontSize": "1.25rem"}},
                            opt.get('icon', '')
                        ) if opt.get('icon') else html.span(),
                        html.span(
                            {"style": {"fontSize": "0.875rem", "flex": "1"}},
                            opt['label']
                        )
                    )
                    for opt in options
                ]
            )
        ) if is_open else html.div()
    )


@component
def range_slider(
    label: str,
    min_val: float,
    max_val: float,
    current_min: float,
    current_max: float,
    on_change: Callable,
    step: float = 1,
    format_fn: Optional[Callable] = None,
    icon: str = "📊"
):
    """
    Slider de range duplo

    Args:
        label: Label do slider
        min_val: Valor mínimo possível
        max_val: Valor máximo possível
        current_min: Valor mínimo atual
        current_max: Valor máximo atual
        on_change: Callback(new_min, new_max)
        step: Incremento do slider
        format_fn: Função para formatar valores exibidos
        icon: Ícone
    """
    if format_fn is None:
        format_fn = lambda x: f"{x:.0f}"

    def handle_min_change(e):
        new_min = float(e['target']['value'])
        if new_min < current_max:
            on_change(new_min, current_max)

    def handle_max_change(e):
        new_max = float(e['target']['value'])
        if new_max > current_min:
            on_change(current_min, new_max)

    return html.div(
        {
            "style": {
                "padding": "1rem",
                "background": "white",
                "borderRadius": "0.75rem",
                "border": "1px solid #e5e7eb"
            }
        },
        # Header
        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "1rem"
                }
            },
            html.span(
                {"style": {"fontSize": "0.875rem", "fontWeight": "600", "color": "#374151"}},
                f"{icon} {label}"
            ),
            html.span(
                {"style": {"fontSize": "0.875rem", "color": "#6b7280"}},
                f"{format_fn(current_min)} - {format_fn(current_max)}"
            )
        ),

        # Sliders
        html.div(
            {"style": {"display": "flex", "flexDirection": "column", "gap": "0.5rem"}},
            # Min slider
            html.div(
                {"style": {"display": "flex", "alignItems": "center", "gap": "0.75rem"}},
                html.span(
                    {"style": {"fontSize": "0.75rem", "color": "#9ca3af", "minWidth": "3rem"}},
                    "Mín:"
                ),
                html.input({
                    "type": "range",
                    "min": min_val,
                    "max": max_val,
                    "step": step,
                    "value": current_min,
                    "onChange": handle_min_change,
                    "style": {
                        "flex": "1",
                        "cursor": "pointer"
                    }
                })
            ),
            # Max slider
            html.div(
                {"style": {"display": "flex", "alignItems": "center", "gap": "0.75rem"}},
                html.span(
                    {"style": {"fontSize": "0.75rem", "color": "#9ca3af", "minWidth": "3rem"}},
                    "Máx:"
                ),
                html.input({
                    "type": "range",
                    "min": min_val,
                    "max": max_val,
                    "step": step,
                    "value": current_max,
                    "onChange": handle_max_change,
                    "style": {
                        "flex": "1",
                        "cursor": "pointer"
                    }
                })
            )
        )
    )


@component
def quick_filters(
    filters: List[Dict[str, Any]],
    active_filter: Optional[str],
    on_filter_click: Callable
):
    """
    Filtros rápidos com badges clicáveis

    Args:
        filters: Lista de {id, label, icon, color}
        active_filter: ID do filtro ativo
        on_filter_click: Callback(filter_id)
    """
    return html.div(
        {
            "style": {
                "display": "flex",
                "gap": "0.5rem",
                "flexWrap": "wrap"
            }
        },
        *[
            html.button(
                {
                    "key": f['id'],
                    "onClick": lambda e, fid=f['id']: on_filter_click(fid),
                    "style": {
                        "display": "inline-flex",
                        "alignItems": "center",
                        "gap": "0.375rem",
                        "padding": "0.5rem 1rem",
                        "borderRadius": "9999px",
                        "border": "2px solid" + (" #1e40af" if active_filter == f['id'] else " #e5e7eb"),
                        "background": "#eff6ff" if active_filter == f['id'] else "white",
                        "color": "#1e40af" if active_filter == f['id'] else "#6b7280",
                        "fontSize": "0.875rem",
                        "fontWeight": "600" if active_filter == f['id'] else "500",
                        "cursor": "pointer",
                        "transition": "all 0.2s"
                    }
                },
                html.span(f.get('icon', '')),
                html.span(f['label'])
            )
            for f in filters
        ]
    )


@component
def search_with_suggestions(
    placeholder: str,
    value: str,
    suggestions: List[str],
    on_change: Callable,
    on_select: Callable
):
    """
    Campo de busca com sugestões/autocomplete

    Args:
        placeholder: Placeholder do input
        value: Valor atual
        suggestions: Lista de sugestões
        on_change: Callback(new_value)
        on_select: Callback(selected_suggestion)
    """
    show_suggestions, set_show_suggestions = use_state(False)

    def handle_change(e):
        new_value = e['target']['value']
        on_change(new_value)
        set_show_suggestions(bool(new_value and suggestions))

    def handle_select(suggestion):
        on_select(suggestion)
        set_show_suggestions(False)

    def handle_focus():
        if value and suggestions:
            set_show_suggestions(True)

    return html.div(
        {
            "style": {
                "position": "relative",
                "width": "100%"
            }
        },
        # Input de busca
        html.input({
            "type": "text",
            "placeholder": placeholder,
            "value": value,
            "onChange": handle_change,
            "onFocus": lambda e: handle_focus(),
            "onBlur": lambda e: set_show_suggestions(False),
            "style": {
                "width": "100%",
                "padding": "0.875rem 1rem 0.875rem 2.5rem",
                "fontSize": "0.9375rem",
                "borderRadius": "0.75rem",
                "border": "2px solid #e5e7eb",
                "background": "white",
                "transition": "all 0.2s",
                "outline": "none"
            }
        }),

        # Ícone de busca
        html.span(
            {
                "style": {
                    "position": "absolute",
                    "left": "1rem",
                    "top": "50%",
                    "transform": "translateY(-50%)",
                    "fontSize": "1.25rem",
                    "pointerEvents": "none"
                }
            },
            "🔍"
        ),

        # Lista de sugestões
        html.div(
            {
                "style": {
                    "display": "block" if show_suggestions and suggestions else "none",
                    "position": "absolute",
                    "top": "calc(100% + 0.5rem)",
                    "left": "0",
                    "right": "0",
                    "background": "white",
                    "borderRadius": "0.75rem",
                    "boxShadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                    "border": "1px solid #e5e7eb",
                    "maxHeight": "300px",
                    "overflow": "auto",
                    "zIndex": "50"
                }
            },
            *[
                html.div(
                    {
                        "key": suggestion,
                        "onMouseDown": lambda e, s=suggestion: handle_select(s),
                        "style": {
                            "padding": "0.75rem 1rem",
                            "cursor": "pointer",
                            "borderBottom": "1px solid #f3f4f6",
                            "transition": "background 0.2s"
                        }
                    },
                    html.span(
                        {"style": {"fontSize": "0.875rem"}},
                        suggestion
                    )
                )
                for suggestion in suggestions[:10]  # Limitar a 10 sugestões
            ]
        ) if show_suggestions and suggestions else html.div()
    )


@component
def filter_panel(
    tipo_options: List[Dict],
    selected_tipos: List[str],
    var_range: tuple,
    pl_range: tuple,
    show_only_alerts: bool,
    on_tipo_change: Callable,
    on_var_change: Callable,
    on_pl_change: Callable,
    on_alerts_toggle: Callable,
    on_clear_all: Callable
):
    """
    Painel completo de filtros

    Args:
        tipo_options: Opções de tipos de fundos
        selected_tipos: Tipos selecionados
        var_range: (min, max) variação D-1
        pl_range: (min, max) PL
        show_only_alerts: Mostrar apenas fundos com alertas
        on_tipo_change: Callback para mudança de tipos
        on_var_change: Callback para mudança de variação
        on_pl_change: Callback para mudança de PL
        on_alerts_toggle: Callback para toggle de alertas
        on_clear_all: Callback para limpar todos os filtros
    """
    is_expanded, set_is_expanded = use_state(False)

    total_active = len(selected_tipos) + (1 if show_only_alerts else 0)

    return html.div(
        {
            "style": {
                "background": "white",
                "borderRadius": "1rem",
                "padding": "1.5rem",
                "marginBottom": "1.5rem",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
                "border": "1px solid #e5e7eb"
            }
        },
        # Header
        html.div(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "1rem" if is_expanded else "0"
                }
            },
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "0.75rem"
                    }
                },
                html.h3(
                    {"style": {"margin": "0", "fontSize": "1.125rem", "fontWeight": "600"}},
                    "🎯 Filtros Avançados"
                ),
                html.span(
                    {
                        "style": {
                            "display": "inline-flex",
                            "alignItems": "center",
                            "background": "#eff6ff",
                            "color": "#1e40af",
                            "padding": "0.25rem 0.625rem",
                            "borderRadius": "9999px",
                            "fontSize": "0.75rem",
                            "fontWeight": "600"
                        }
                    },
                    f"{total_active} ativo" + ("s" if total_active != 1 else "")
                ) if total_active > 0 else html.span()
            ),
            html.div(
                {"style": {"display": "flex", "gap": "0.5rem"}},
                html.button(
                    {
                        "onClick": lambda e: on_clear_all(),
                        "style": {
                            "padding": "0.5rem 1rem",
                            "fontSize": "0.875rem",
                            "borderRadius": "0.5rem",
                            "border": "1px solid #d1d5db",
                            "background": "white",
                            "cursor": "pointer"
                        }
                    },
                    "Limpar"
                ) if total_active > 0 else html.div(),
                html.button(
                    {
                        "onClick": lambda e: set_is_expanded(not is_expanded),
                        "style": {
                            "padding": "0.5rem 1rem",
                            "fontSize": "0.875rem",
                            "borderRadius": "0.5rem",
                            "border": "1px solid #d1d5db",
                            "background": "white",
                            "cursor": "pointer"
                        }
                    },
                    "▼ Expandir" if not is_expanded else "▲ Recolher"
                )
            )
        ),

        # Conteúdo expansível
        html.div(
            {
                "style": {
                    "display": "block" if is_expanded else "none",
                    "animation": "fadeIn 0.3s ease-out"
                }
            },
            html.div(
                {
                    "style": {
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                        "gap": "1.5rem"
                    }
                },
                # Filtro por tipo
                multi_select_dropdown(
                    "Tipo de Fundo",
                    tipo_options,
                    selected_tipos,
                    on_tipo_change,
                    "📁"
                ),

                # Toggle de alertas
                html.div(
                    {
                        "style": {
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "0.75rem",
                            "padding": "1rem",
                            "background": "#fef3c7" if show_only_alerts else "#f9fafb",
                            "borderRadius": "0.75rem",
                            "border": "1px solid" + (" #f59e0b" if show_only_alerts else " #e5e7eb"),
                            "cursor": "pointer"
                        },
                        "onClick": lambda e: on_alerts_toggle()
                    },
                    html.input({
                        "type": "checkbox",
                        "checked": show_only_alerts,
                        "style": {
                            "width": "1.25rem",
                            "height": "1.25rem",
                            "cursor": "pointer"
                        }
                    }),
                    html.div(
                        html.span(
                            {"style": {"fontSize": "0.875rem", "fontWeight": "600", "display": "block"}},
                            "⚠️ Apenas com Alertas"
                        ),
                        html.span(
                            {"style": {"fontSize": "0.75rem", "color": "#6b7280"}},
                            "Fundos que requerem atenção"
                        )
                    )
                )
            ),

            # Sliders (linha separada)
            html.div(
                {
                    "style": {
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(300px, 1fr))",
                        "gap": "1.5rem",
                        "marginTop": "1.5rem"
                    }
                },
                range_slider(
                    "Variação D-1 (%)",
                    -20, 20,
                    var_range[0], var_range[1],
                    on_var_change,
                    step=0.5,
                    format_fn=lambda x: f"{x:+.1f}%",
                    icon="📈"
                ),
                range_slider(
                    "Patrimônio Líquido (M)",
                    0, 100_000,
                    pl_range[0], pl_range[1],
                    on_pl_change,
                    step=1000,
                    format_fn=lambda x: f"R$ {x/1_000_000:.0f}M",
                    icon="💰"
                )
            )
        ) if is_expanded else html.div()
    )
