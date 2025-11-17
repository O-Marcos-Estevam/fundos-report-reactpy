"""
Página de Execução Moderna
Interface moderna para executar relatórios com feedback visual
"""

from reactpy import component, html, use_state
from datetime import datetime, timedelta
import threading

from components.layout_modern import page_container, section_card, modern_grid
from components.cards_modern import metric_card_modern, info_card_modern
from components.svg_illustrations import (
    loading_illustration,
    success_illustration,
    error_illustration,
    document_icon
)
from components.advanced_components import (
    tabs,
    toast_notification,
    breadcrumbs,
    modal
)
from components.forms import seletor_data, seletor_versao, botao
from services.state_manager import get_state_manager
from services.report_executor import ReportExecutor
from services.historico_service import HistoricoService


@component
def pagina_executar_moderna():
    """Página moderna de execução de relatórios"""

    state_manager = get_state_manager()
    historico_service = HistoricoService()

    # Estado local
    data_selecionada, set_data = use_state(datetime.now() - timedelta(days=1))
    versao_selecionada, set_versao = use_state(state_manager.versao_modulo)
    executando, set_executando = use_state(False)
    progresso, set_progresso = use_state(0)
    mensagem_status, set_mensagem = use_state("Pronto para executar")
    logs, set_logs = use_state([])
    resultado, set_resultado = use_state(None)
    show_toast, set_show_toast = use_state(False)
    toast_message, set_toast_message = use_state("")
    toast_type, set_toast_type = use_state("info")
    show_confirm_modal, set_show_confirm_modal = use_state(False)

    def atualizar_versao(nova_versao: str):
        """Atualiza versão do módulo"""
        set_versao(nova_versao)
        state_manager.set_versao_modulo(nova_versao)

    def mostrar_toast(mensagem: str, tipo: str = "info"):
        """Mostra toast notification"""
        set_toast_message(mensagem)
        set_toast_type(tipo)
        set_show_toast(True)
        # Auto-hide será feito via timeout no componente

    def confirmar_execucao():
        """Abre modal de confirmação"""
        set_show_confirm_modal(True)

    def executar_relatorio():
        """Executa a geração do relatório"""
        set_show_confirm_modal(False)
        set_executando(True)
        set_progresso(0)
        set_mensagem("Iniciando execução...")
        set_logs([])
        set_resultado(None)

        def executar_em_thread():
            """Executa o relatório em thread separada"""
            try:
                # Criar executor
                executor = ReportExecutor(versao_selecionada)

                # Callbacks
                def on_progress(prog: int, msg: str):
                    set_progresso(prog)
                    set_mensagem(msg)

                def on_log(log: str):
                    set_logs(lambda logs: logs + [log])

                # Executar com timeout de 120 segundos
                execucao = executor.executar(
                    data_selecionada,
                    progress_callback=on_progress,
                    log_callback=on_log,
                    timeout=120
                )

                # Salvar no state manager
                state_manager.set_ultima_execucao(execucao)

                # Salvar no histórico
                if execucao.sucesso:
                    historico_service.adicionar(
                        data_selecionada.strftime('%Y-%m-%d'),
                        'sucesso',
                        execucao.tempo_execucao,
                        execucao.fundos_processados,
                        {'modulo': execucao.nome_modulo}
                    )

                set_resultado(execucao)
                set_progresso(100)

                # Mostrar toast
                if execucao.sucesso:
                    mostrar_toast("Relatório gerado com sucesso!", "success")
                else:
                    mostrar_toast("Erro ao gerar relatório", "error")

            except Exception as e:
                set_mensagem(f"Erro: {str(e)}")
                set_resultado({"sucesso": False, "erro": str(e)})
                mostrar_toast(f"Erro: {str(e)}", "error")
            finally:
                set_executando(False)

        # Executar em thread separada
        import threading
        thread = threading.Thread(target=executar_em_thread, daemon=True)
        thread.start()


    # Breadcrumbs
    breadcrumb = breadcrumbs([
        {"label": "Home", "href": "#", "icon": "🏠"},
        {"label": "Executar", "icon": "🚀"}
    ])

    return html.div(
        {"class": "animate-fade-in"},

        # Breadcrumbs
        breadcrumb,

        # Toast Notification
        toast_notification(
            message=toast_message,
            tipo=toast_type,
            show=show_toast
        ),

        # Modal de Confirmação
        modal(
            "Confirmar Execução",
            show_confirm_modal,
            lambda: set_show_confirm_modal(False),

            html.div(
                {"style": {"textAlign": "center"}},
                document_icon(width="80px", height="80px", color="#4F46E5"),
                html.h3(
                    {"style": {"margin": "1rem 0"}},
                    "Executar Relatório?"
                ),
                html.p(
                    {"style": {"color": "var(--color-text-secondary)", "marginBottom": "1.5rem"}},
                    f"Data: {data_selecionada.strftime('%d/%m/%Y')} | Versão: {versao_selecionada.upper()}"
                ),
                html.div(
                    {
                        "class": "alert alert-info",
                        "style": {"marginBottom": "1.5rem", "textAlign": "left"}
                    },
                    "ℹ️ Esta operação pode levar alguns minutos dependendo da quantidade de dados."
                ),
                html.div(
                    {"style": {"display": "flex", "gap": "1rem", "justifyContent": "center"}},
                    html.button(
                        {
                            "class": "btn btn-primary btn-lg",
                            "onClick": lambda e: executar_relatorio()
                        },
                        "🚀 Executar Agora"
                    ),
                    html.button(
                        {
                            "class": "btn btn-outline",
                            "onClick": lambda e: set_show_confirm_modal(False)
                        },
                        "Cancelar"
                    )
                )
            ),

            size="medium"
        ),

        # Page Container
        page_container(
            # Tabs de conteúdo
            tabs(
                tabs_data=[
                    {
                        "id": "config",
                        "label": "Configuração",
                        "icon": "⚙️",
                        "content": tab_configuracao(
                            data_selecionada,
                            set_data,
                            versao_selecionada,
                            atualizar_versao,
                            executando,
                            confirmar_execucao
                        )
                    },
                    {
                        "id": "execucao",
                        "label": "Execução",
                        "icon": "⚡",
                        "content": tab_execucao(
                            executando,
                            progresso,
                            mensagem_status,
                            logs,
                            resultado
                        )
                    },
                    {
                        "id": "ajuda",
                        "label": "Ajuda",
                        "icon": "❓",
                        "content": tab_ajuda(versao_selecionada)
                    }
                ],
                default_tab="config"
            ),

            titulo="🚀 Executar Relatório",
            descricao="Configure e execute a geração de relatórios de fundos"
        )
    )


@component
def tab_configuracao(data, set_data, versao, set_versao, executando, confirmar):
    """Tab de configuração do relatório"""
    return html.div(
        {"class": "animate-fade-in"},

        modern_grid(
            # Configurações
            section_card(
                "Parâmetros do Relatório",

                html.div(
                    {"style": {"display": "flex", "flexDirection": "column", "gap": "1.5rem"}},

                    # Data
                    html.div(
                        {"class": "input-group"},
                        html.label(
                            {"class": "input-label"},
                            "📅 Data Base"
                        ),
                        seletor_data(data, set_data),
                        html.p(
                            {"class": "input-helper"},
                            "Selecione a data base para o relatório"
                        )
                    ),

                    # Versão
                    html.div(
                        {"class": "input-group"},
                        html.label(
                            {"class": "input-label"},
                            "🔧 Versão do Módulo"
                        ),
                        seletor_versao(versao, set_versao),
                        html.p(
                            {"class": "input-helper"},
                            "V6 é recomendado (70% mais rápido)"
                        )
                    ),

                    # Botão de execução
                    html.div(
                        {"style": {"marginTop": "1rem"}},
                        html.button(
                            {
                                "class": "btn btn-primary btn-lg",
                                "onClick": lambda e: confirmar(),
                                "disabled": executando,
                                "style": {"width": "100%"}
                            },
                            "🚀 Executar Relatório" if not executando else "⏳ Executando..."
                        )
                    )
                ),

                icone="📋"
            ),

            # Informações
            section_card(
                "Informações",

                html.div(
                    {"style": {"display": "flex", "flexDirection": "column", "gap": "1rem"}},

                    info_card_modern(
                        "Versões Disponíveis",
                        html.ul(
                            {"style": {"margin": "0.5rem 0", "paddingLeft": "1.5rem"}},
                            html.li("V4 - Legacy (40-65s)"),
                            html.li("V5 - Enhanced (40-65s)"),
                            html.li(html.strong("V6 - Optimized (7-15s) ⭐ Recomendado"))
                        ),
                        tipo="info"
                    ),

                    info_card_modern(
                        "Tempo Estimado",
                        html.p(
                            {"style": {"margin": "0.5rem 0"}},
                            f"V6: ~10 segundos | V4/V5: ~50 segundos"
                        ),
                        tipo="warning"
                    )
                ),

                icone="ℹ️"
            ),

            cols=2,
            gap="1.5rem"
        )
    )


@component
def tab_execucao(executando, progresso, mensagem, logs, resultado):
    """Tab de execução e monitoramento"""
    return html.div(
        {"class": "animate-fade-in"},

        # Status atual
        section_card(
            "Status da Execução",

            html.div(
                # Ilustração de status
                html.div(
                    {"style": {"textAlign": "center", "marginBottom": "2rem"}},
                    loading_illustration(width="120px", height="120px") if executando
                    else success_illustration(width="120px", height="120px") if resultado and resultado.sucesso
                    else error_illustration(width="120px", height="120px") if resultado and not resultado.sucesso
                    else document_icon(width="120px", height="120px", color="#6B7280")
                ),

                # Mensagem de status
                html.div(
                    {
                        "style": {
                            "textAlign": "center",
                            "fontSize": "1.25rem",
                            "fontWeight": "600",
                            "marginBottom": "1.5rem",
                            "color": "var(--color-primary)" if executando else "var(--color-text-primary)"
                        }
                    },
                    mensagem
                ),

                # Progress bar
                html.div(
                    {"class": "progress", "style": {"marginBottom": "1rem"}},
                    html.div(
                        {
                            "class": "progress-bar",
                            "style": {"width": f"{progresso}%"}
                        }
                    )
                ) if executando or progresso > 0 else None,

                # Porcentagem
                html.div(
                    {
                        "style": {
                            "textAlign": "center",
                            "fontSize": "0.875rem",
                            "color": "var(--color-text-secondary)",
                            "marginBottom": "2rem"
                        }
                    },
                    f"{progresso}% concluído"
                ) if executando or progresso > 0 else None,

                # Resultado
                _render_resultado(resultado) if resultado else None
            ),

            icone="⚡"
        ),

        # Logs
        section_card(
            f"Logs de Execução ({len(logs)})",

            html.div(
                {
                    "style": {
                        "background": "#1F2937",
                        "color": "#E5E7EB",
                        "padding": "1rem",
                        "borderRadius": "0.5rem",
                        "fontFamily": "monospace",
                        "fontSize": "0.875rem",
                        "maxHeight": "300px",
                        "overflowY": "auto",
                    }
                },
                *[
                    html.div(
                        {"style": {"marginBottom": "0.25rem"}},
                        f"[{idx+1}] {log}"
                    )
                    for idx, log in enumerate(logs)
                ]
            ) if logs else html.div(
                {
                    "style": {
                        "textAlign": "center",
                        "padding": "2rem",
                        "color": "var(--color-text-tertiary)"
                    }
                },
                "Nenhum log ainda"
            ),

            icone="📝"
        ) if executando or logs else None
    )


@component
def tab_ajuda(versao):
    """Tab de ajuda e documentação"""
    return html.div(
        {"class": "animate-fade-in"},

        section_card(
            "Como Usar",

            html.div(
                {"style": {"display": "flex", "flexDirection": "column", "gap": "1.5rem"}},

                html.div(
                    html.h4("1️⃣ Selecione a Data"),
                    html.p("Escolha a data base para o relatório. Geralmente D-1 (ontem).")
                ),

                html.div(
                    html.h4("2️⃣ Escolha a Versão"),
                    html.p("V6 Optimized é recomendado por ser 70% mais rápido.")
                ),

                html.div(
                    html.h4("3️⃣ Execute"),
                    html.p("Clique em 'Executar Relatório' e aguarde o processamento.")
                ),

                html.div(
                    html.h4("4️⃣ Visualize"),
                    html.p("Após concluído, vá para 'Dashboard' para visualizar os dados.")
                ),

                html.div(
                    {"class": "alert alert-info"},
                    "💡 Dica: Use V6 para relatórios diários. V4/V5 apenas para compatibilidade."
                )
            ),

            icone="📖"
        )
    )


@component
def _render_resultado(resultado):
    """Renderiza resultado da execução"""
    if not resultado:
        return None

    sucesso = resultado.sucesso if hasattr(resultado, 'sucesso') else False

    return html.div(
        {
            "class": f"alert alert-{'success' if sucesso else 'error'}",
            "style": {"marginTop": "2rem"}
        },

        html.div(
            {"style": {"display": "flex", "alignItems": "center", "gap": "0.75rem", "marginBottom": "1rem"}},
            html.span({"style": {"fontSize": "1.5rem"}}, "✅" if sucesso else "❌"),
            html.strong(
                {"style": {"fontSize": "1.125rem"}},
                "Relatório gerado com sucesso!" if sucesso else "Erro na execução"
            )
        ),

        html.div(
            {"style": {"display": "grid", "gridTemplateColumns": "repeat(2, 1fr)", "gap": "1rem"}},
            html.div(
                html.div({"style": {"fontSize": "0.875rem", "opacity": "0.8"}}, "Fundos Processados"),
                html.div({"style": {"fontSize": "1.5rem", "fontWeight": "700"}}, str(resultado.fundos_processados))
            ) if hasattr(resultado, 'fundos_processados') else None,
            html.div(
                html.div({"style": {"fontSize": "0.875rem", "opacity": "0.8"}}, "Tempo de Execução"),
                html.div({"style": {"fontSize": "1.5rem", "fontWeight": "700"}}, f"{resultado.tempo_execucao:.1f}s")
            ) if hasattr(resultado, 'tempo_execucao') else None,
        )
    )
