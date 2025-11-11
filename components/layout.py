"""
Componentes de Layout
Header, Sidebar, Navegação e Containers
"""

from reactpy import component, html
from datetime import datetime
from typing import Optional

from app.config import AppConfig


@component
def header(titulo: str = None, subtitulo: str = None):
    """
    Cabeçalho principal da aplicação

    Args:
        titulo: Título customizado (opcional)
        subtitulo: Subtítulo customizado (opcional)
    """
    titulo = titulo or AppConfig.APP_TITLE
    subtitulo = subtitulo or f"Versão {AppConfig.APP_VERSION} - {AppConfig.APP_SUBTITLE}"

    return html.header(
        {
            "style": {
                "background": f"linear-gradient(135deg, {AppConfig.get_color('primary')} 0%, {AppConfig.get_color('secondary')} 100%)",
                "color": "white",
                "padding": "2.5rem",
                "border_radius": "15px",
                "margin_bottom": "2rem",
                "box_shadow": "0 8px 16px rgba(0,0,0,0.1)",
                "text_align": "center",
            }
        },
        html.h1(
            {"style": {"margin": "0", "font_size": "2.5rem", "font_weight": "700"}},
            titulo
        ),
        html.h3(
            {"style": {"margin": "0.5rem 0 0 0", "font_weight": "300", "opacity": "0.9"}},
            subtitulo
        ),
        html.p(
            {"style": {"margin": "1rem 0 0 0", "opacity": "0.8", "font_size": "0.9rem"}},
            f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )
    )


@component
def navegacao(pagina_atual: str, on_change):
    """
    Menu de navegação entre páginas

    Args:
        pagina_atual: Página atualmente ativa
        on_change: Callback quando página muda
    """
    paginas = [
        ("executar", "Executar", "🚀"),
        ("dashboard", "Dashboard", "📊"),
        ("lamina", "Lâmina de Fundos", "📄"),
        ("historico", "Histórico", "📜"),
        ("configuracoes", "Configurações", "⚙️"),
    ]

    def criar_botao(key: str, nome: str, icone: str):
        """Cria botão de navegação"""
        ativo = key == pagina_atual

        return html.button(
            {
                "key": key,
                "onClick": lambda e: on_change(key),
                "style": {
                    "background": AppConfig.get_color('primary') if ativo else "#f5f5f5",
                    "color": "white" if ativo else "#333",
                    "border": "none",
                    "padding": "12px 24px",
                    "border_radius": "8px",
                    "font_size": "1rem",
                    "font_weight": "600" if ativo else "500",
                    "cursor": "pointer",
                    "transition": "all 0.3s",
                    "margin": "0 8px",
                    "box_shadow": "0 2px 4px rgba(0,0,0,0.1)" if ativo else "none",
                }
            },
            f"{icone} {nome}"
        )

    return html.div(
        {
            "style": {
                "display": "flex",
                "justify_content": "center",
                "flex_wrap": "wrap",
                "gap": "8px",
                "margin_bottom": "2rem",
                "padding": "1rem",
                "background": "white",
                "border_radius": "12px",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.05)",
            }
        },
        *[criar_botao(key, nome, icone) for key, nome, icone in paginas]
    )


@component
def sidebar(state_manager):
    """
    Barra lateral com status do sistema

    Args:
        state_manager: Instância do StateManager
    """
    stats = state_manager.get_estatisticas_rapidas()

    return html.aside(
        {
            "style": {
                "background": "white",
                "padding": "1.5rem",
                "border_radius": "12px",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.05)",
                "min_width": "250px",
            }
        },
        # Status do Sistema
        html.div(
            html.h3(
                {"style": {"margin": "0 0 1rem 0", "color": "#333"}},
                "🔧 Status do Sistema"
            ),
            html.div(
                {"style": {"margin_bottom": "1rem"}},
                html.p(
                    {"style": {"margin": "0.5rem 0", "font_size": "0.9rem"}},
                    html.strong("Versão: "),
                    state_manager.versao_modulo
                ),
                html.p(
                    {"style": {"margin": "0.5rem 0", "font_size": "0.9rem"}},
                    html.strong("Página: "),
                    state_manager.pagina_atual
                ),
            )
        ),

        html.hr({"style": {"margin": "1.5rem 0", "border": "none", "border_top": "1px solid #eee"}}),

        # Estatísticas
        html.div(
            html.h3(
                {"style": {"margin": "0 0 1rem 0", "color": "#333"}},
                "📊 Estatísticas"
            ),
            html.div(
                {"style": {"margin_bottom": "1rem"}},
                html.p(
                    {"style": {"margin": "0.5rem 0", "font_size": "0.9rem"}},
                    html.strong("Total Execuções: "),
                    str(stats.get('total_execucoes', 0))
                ),
                html.p(
                    {"style": {"margin": "0.5rem 0", "font_size": "0.9rem"}},
                    html.strong("Taxa Sucesso: "),
                    f"{stats.get('taxa_sucesso', 0):.1f}%"
                ),
            )
        ),

        html.hr({"style": {"margin": "1.5rem 0", "border": "none", "border_top": "1px solid #eee"}}),

        # Última Execução
        html.div(
            html.h3(
                {"style": {"margin": "0 0 1rem 0", "color": "#333"}},
                "⏱️ Última Execução"
            ),
            html.div(
                {"style": {"font_size": "0.9rem"}},
                html.p(
                    {"style": {"margin": "0.5rem 0", "color": AppConfig.get_color('success')}},
                    "✅ Disponível"
                ) if stats.get('tem_execucao') else html.p(
                    {"style": {"margin": "0.5rem 0", "color": "#999"}},
                    "ℹ️ Nenhuma execução"
                ),
                html.p(
                    {"style": {"margin": "0.5rem 0"}},
                    f"Fundos: {stats.get('fundos_processados', 0)}"
                ) if stats.get('tem_execucao') else None,
                html.p(
                    {"style": {"margin": "0.5rem 0"}},
                    f"Tempo: {stats.get('tempo_ultima', 0):.1f}s"
                ) if stats.get('tem_execucao') else None,
            )
        )
    )


@component
def container_pagina(*children):
    """
    Container padrão para conteúdo de páginas

    Args:
        *children: Elementos filhos
    """
    return html.div(
        {
            "style": {
                "background": "white",
                "padding": "2rem",
                "border_radius": "12px",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.05)",
                "min_height": "500px",
            }
        },
        *children
    )
