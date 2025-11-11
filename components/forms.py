"""
Componentes de Formulários
Inputs, seletores e botões
"""

from reactpy import component, html, use_state
from datetime import datetime, timedelta
from typing import List, Callable, Optional

from app.config import AppConfig, MODULOS_RELATORIO


@component
def seletor_data(value: datetime, on_change: Callable[[datetime], None]):
    """
    Seletor de data com quick select

    Args:
        value: Data atual
        on_change: Callback quando data muda
    """
    data_str = value.strftime('%Y-%m-%d')

    def handle_change(event):
        """Handler para mudança de data"""
        nova_data_str = event['target']['value']
        nova_data = datetime.strptime(nova_data_str, '%Y-%m-%d')
        on_change(nova_data)

    def set_ontem():
        """Define data como ontem"""
        on_change(datetime.now() - timedelta(days=1))

    def set_hoje():
        """Define data como hoje"""
        on_change(datetime.now())

    return html.div(
        {"style": {"margin_bottom": "1.5rem"}},
        html.label(
            {
                "style": {
                    "display": "block",
                    "margin_bottom": "0.5rem",
                    "font_weight": "600",
                    "color": "#333",
                }
            },
            "📅 Data do Relatório:"
        ),
        html.div(
            {"style": {"display": "flex", "gap": "10px", "align_items": "center"}},
            # Input de data
            html.input({
                "type": "date",
                "value": data_str,
                "max": datetime.now().strftime('%Y-%m-%d'),
                "onChange": handle_change,
                "style": {
                    "padding": "10px",
                    "border": "1px solid #ddd",
                    "border_radius": "8px",
                    "font_size": "1rem",
                    "flex": "1",
                }
            }),
            # Botão Ontem
            html.button(
                {
                    "onClick": lambda e: set_ontem(),
                    "style": {
                        "padding": "10px 20px",
                        "background": "#f5f5f5",
                        "border": "1px solid #ddd",
                        "border_radius": "8px",
                        "cursor": "pointer",
                        "font_weight": "600",
                    }
                },
                "Ontem"
            ),
            # Botão Hoje
            html.button(
                {
                    "onClick": lambda e: set_hoje(),
                    "style": {
                        "padding": "10px 20px",
                        "background": "#f5f5f5",
                        "border": "1px solid #ddd",
                        "border_radius": "8px",
                        "cursor": "pointer",
                        "font_weight": "600",
                    }
                },
                "Hoje"
            ),
        ),
        # Info sobre a data
        html.div(
            {
                "style": {
                    "margin_top": "0.5rem",
                    "padding": "0.75rem",
                    "background": "#f0f7ff",
                    "border_radius": "6px",
                    "font_size": "0.9rem",
                    "color": "#333",
                }
            },
            f"Data selecionada: {value.strftime('%d/%m/%Y (%A)')}"
        )
    )


@component
def seletor_versao(value: str, on_change: Callable[[str], None]):
    """
    Seletor de versão do módulo

    Args:
        value: Versão atual
        on_change: Callback quando versão muda
    """
    def handle_change(event):
        """Handler para mudança de versão"""
        nova_versao = event['target']['value']
        on_change(nova_versao)

    opcoes = [
        ("V6", "V6 Optimized", "Performance 70% mais rápida, análise preditiva"),
        ("V5", "V5 Enhanced", "Relatório com 3 abas e formatação avançada"),
        ("V4", "V4 Legacy", "Versão anterior para compatibilidade"),
    ]

    return html.div(
        {"style": {"margin_bottom": "1.5rem"}},
        html.label(
            {
                "style": {
                    "display": "block",
                    "margin_bottom": "0.5rem",
                    "font_weight": "600",
                    "color": "#333",
                }
            },
            "📦 Versão do Módulo:"
        ),
        html.select(
            {
                "value": value,
                "onChange": handle_change,
                "style": {
                    "width": "100%",
                    "padding": "10px",
                    "border": "1px solid #ddd",
                    "border_radius": "8px",
                    "font_size": "1rem",
                    "background": "white",
                    "cursor": "pointer",
                }
            },
            *[
                html.option(
                    {"value": v, "key": v},
                    f"{nome} - {desc}"
                )
                for v, nome, desc in opcoes
            ]
        ),
        # Info da versão
        html.div(
            {
                "style": {
                    "margin_top": "0.5rem",
                    "padding": "0.75rem",
                    "background": "#f0fff4",
                    "border_radius": "6px",
                    "font_size": "0.85rem",
                    "color": "#333",
                }
            },
            f"ℹ️ {MODULOS_RELATORIO[value].descricao}"
        )
    )


@component
def seletor_fundo(fundos: List[str], value: Optional[str], on_change: Callable[[str], None]):
    """
    Seletor de fundo com busca

    Args:
        fundos: Lista de nomes de fundos
        value: Fundo selecionado
        on_change: Callback quando fundo muda
    """
    def handle_change(event):
        """Handler para mudança de fundo"""
        novo_fundo = event['target']['value']
        if novo_fundo:
            on_change(novo_fundo)

    fundos_ordenados = sorted(fundos)

    return html.div(
        {"style": {"margin_bottom": "1.5rem"}},
        html.label(
            {
                "style": {
                    "display": "block",
                    "margin_bottom": "0.5rem",
                    "font_weight": "600",
                    "color": "#333",
                }
            },
            "🔍 Selecione o Fundo:"
        ),
        html.select(
            {
                "value": value or "",
                "onChange": handle_change,
                "style": {
                    "width": "100%",
                    "padding": "10px",
                    "border": "1px solid #ddd",
                    "border_radius": "8px",
                    "font_size": "1rem",
                    "background": "white",
                    "cursor": "pointer",
                }
            },
            html.option({"value": "", "key": "empty"}, "-- Selecione um fundo --"),
            *[
                html.option({"value": fundo, "key": fundo}, fundo)
                for fundo in fundos_ordenados
            ]
        )
    )


@component
def botao(
    texto: str,
    on_click: Callable,
    tipo: str = "primary",
    icone: Optional[str] = None,
    desabilitado: bool = False,
    full_width: bool = False
):
    """
    Botão customizado

    Args:
        texto: Texto do botão
        on_click: Callback quando clicado
        tipo: Tipo (primary, secondary, success, danger)
        icone: Ícone (emoji ou texto)
        desabilitado: Se True, botão desabilitado
        full_width: Se True, ocupa largura total
    """
    cores = {
        "primary": AppConfig.get_color('primary'),
        "secondary": "#6c757d",
        "success": AppConfig.get_color('success'),
        "danger": AppConfig.get_color('error'),
        "warning": AppConfig.get_color('warning'),
    }

    cor = cores.get(tipo, cores["primary"])

    return html.button(
        {
            "onClick": on_click,
            "disabled": desabilitado,
            "style": {
                "background": cor if not desabilitado else "#ccc",
                "color": "white",
                "border": "none",
                "padding": "12px 24px",
                "border_radius": "8px",
                "font_size": "1rem",
                "font_weight": "600",
                "cursor": "pointer" if not desabilitado else "not-allowed",
                "transition": "all 0.3s",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.1)",
                "width": "100%" if full_width else "auto",
                "opacity": "0.6" if desabilitado else "1",
            }
        },
        f"{icone} " if icone else "",
        texto
    )


@component
def input_texto(
    label: str,
    value: str,
    on_change: Callable[[str], None],
    placeholder: str = "",
    tipo: str = "text"
):
    """
    Input de texto genérico

    Args:
        label: Label do input
        value: Valor atual
        on_change: Callback quando muda
        placeholder: Placeholder
        tipo: Tipo do input (text, email, password, etc)
    """
    def handle_change(event):
        """Handler para mudança"""
        novo_valor = event['target']['value']
        on_change(novo_valor)

    return html.div(
        {"style": {"margin_bottom": "1.5rem"}},
        html.label(
            {
                "style": {
                    "display": "block",
                    "margin_bottom": "0.5rem",
                    "font_weight": "600",
                    "color": "#333",
                }
            },
            label
        ),
        html.input({
            "type": tipo,
            "value": value,
            "placeholder": placeholder,
            "onChange": handle_change,
            "style": {
                "width": "100%",
                "padding": "10px",
                "border": "1px solid #ddd",
                "border_radius": "8px",
                "font_size": "1rem",
            }
        })
    )


@component
def checkbox(label: str, checked: bool, on_change: Callable[[bool], None]):
    """
    Checkbox customizado

    Args:
        label: Label do checkbox
        checked: Se está marcado
        on_change: Callback quando muda
    """
    def handle_change(event):
        """Handler para mudança"""
        novo_valor = event['target']['checked']
        on_change(novo_valor)

    return html.label(
        {
            "style": {
                "display": "flex",
                "align_items": "center",
                "cursor": "pointer",
                "margin_bottom": "1rem",
            }
        },
        html.input({
            "type": "checkbox",
            "checked": checked,
            "onChange": handle_change,
            "style": {
                "width": "20px",
                "height": "20px",
                "margin_right": "10px",
                "cursor": "pointer",
            }
        }),
        html.span(
            {"style": {"color": "#333", "font_size": "1rem"}},
            label
        )
    )
