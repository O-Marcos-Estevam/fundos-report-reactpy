"""
Página de Execução de Relatórios
Permite configurar e executar a geração de relatórios
"""

from reactpy import component, html, use_state
from datetime import datetime, timedelta
import asyncio

from components.layout import container_pagina
from components.cards import card_metrica, card_status
from components.forms import seletor_data, seletor_versao, botao
from services.state_manager import get_state_manager
from services.report_executor import ReportExecutor
from services.historico_service import HistoricoService


@component
def pagina_executar():
    """Página principal de execução de relatórios"""

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

    def atualizar_versao(nova_versao: str):
        """Atualiza versão do módulo"""
        set_versao(nova_versao)
        state_manager.set_versao_modulo(nova_versao)

    async def executar_relatorio():
        """Executa a geração do relatório"""
        set_executando(True)
        set_progresso(0)
        set_mensagem("Iniciando execução...")
        set_logs([])
        set_resultado(None)

        try:
            # Criar executor
            executor = ReportExecutor(versao_selecionada)

            # Callbacks
            def on_progress(prog: int, msg: str):
                set_progresso(prog)
                set_mensagem(msg)

            def on_log(log: str):
                set_logs(lambda logs: logs + [log])

            # Executar (simular async)
            await asyncio.sleep(0.1)  # Yield control

            execucao = executor.executar(
                data_selecionada,
                progress_callback=on_progress,
                log_callback=on_log
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
            else:
                historico_service.adicionar(
                    data_selecionada.strftime('%Y-%m-%d'),
                    'erro',
                    execucao.tempo_execucao,
                    0,
                    {'erro': execucao.mensagem}
                )

            set_resultado(execucao)

        except Exception as e:
            set_mensagem(f"Erro: {str(e)}")
            set_resultado(None)

        finally:
            set_executando(False)

    def handle_executar(event):
        """Handler do botão executar"""
        asyncio.create_task(executar_relatorio())

    return container_pagina(
        # Título
        html.h2(
            {"style": {"margin": "0 0 2rem 0", "color": "#333"}},
            "🚀 Executar Relatório"
        ),

        # Formulário de configuração
        html.div(
            {
                "style": {
                    "background": "#f8f9fa",
                    "padding": "2rem",
                    "border_radius": "12px",
                    "margin_bottom": "2rem",
                }
            },
            html.h3(
                {"style": {"margin": "0 0 1.5rem 0", "color": "#333"}},
                "⚙️ Configuração"
            ),

            # Seletor de versão
            seletor_versao(versao_selecionada, atualizar_versao),

            # Seletor de data
            seletor_data(data_selecionada, set_data),

            # Botões de ação
            html.div(
                {"style": {"display": "flex", "gap": "1rem", "margin_top": "1.5rem"}},
                botao(
                    "Gerar Relatório",
                    handle_executar,
                    tipo="primary",
                    icone="🚀",
                    desabilitado=executando,
                    full_width=True
                ),
                botao(
                    "Testar Conexão",
                    lambda e: None,  # TODO: implementar
                    tipo="secondary",
                    icone="🔍",
                    desabilitado=executando
                ),
            )
        ),

        # Área de execução (se estiver executando ou tiver resultado)
        html.div(
            # Métricas de progresso
            html.div(
                {
                    "style": {
                        "display": "grid",
                        "grid_template_columns": "repeat(auto-fit, minmax(200px, 1fr))",
                        "gap": "1rem",
                        "margin_bottom": "2rem",
                    }
                },
                card_metrica("Progresso", f"{progresso}%", None, "info", "⚙️"),
                card_metrica("Status", mensagem_status if len(mensagem_status) < 20 else mensagem_status[:17] + "...", None, "primary", "📊"),
                card_metrica(
                    "Fundos",
                    str(resultado.fundos_processados if resultado else 0),
                    None,
                    "success",
                    "📁"
                ),
                card_metrica(
                    "Tempo",
                    f"{resultado.tempo_execucao:.1f}s" if resultado else "0s",
                    None,
                    "warning",
                    "⏱️"
                ),
            ) if executando or resultado else None,

            # Barra de progresso
            html.div(
                {
                    "style": {
                        "background": "#e0e0e0",
                        "border_radius": "8px",
                        "height": "30px",
                        "overflow": "hidden",
                        "margin_bottom": "2rem",
                    }
                },
                html.div(
                    {
                        "style": {
                            "background": f"linear-gradient(90deg, #667eea 0%, #764ba2 100%)",
                            "height": "100%",
                            "width": f"{progresso}%",
                            "transition": "width 0.3s",
                            "display": "flex",
                            "align_items": "center",
                            "justify_content": "center",
                            "color": "white",
                            "font_weight": "600",
                        }
                    },
                    f"{progresso}%" if progresso > 10 else ""
                )
            ) if executando or resultado else None,

            # Logs
            html.div(
                html.h3(
                    {"style": {"margin": "0 0 1rem 0", "color": "#333"}},
                    "📋 Logs de Execução"
                ),
                html.div(
                    {
                        "style": {
                            "background": "#1e1e1e",
                            "color": "#d4d4d4",
                            "padding": "1rem",
                            "border_radius": "8px",
                            "font_family": "'Courier New', monospace",
                            "font_size": "0.85rem",
                            "max_height": "400px",
                            "overflow_y": "auto",
                        }
                    },
                    *[
                        html.div(
                            {"key": f"log-{i}", "style": {"margin": "0.25rem 0"}},
                            log
                        )
                        for i, log in enumerate(logs[-20:])  # Últimas 20 linhas
                    ] if logs else [html.div("Aguardando execução...")]
                )
            ) if executando or resultado else None,

            # Resultado
            html.div(
                {"style": {"margin_top": "2rem"}},
                card_status(
                    "Relatório Gerado com Sucesso!",
                    f"Processados {resultado.fundos_processados} fundos em {resultado.tempo_execucao:.2f} segundos.",
                    "success"
                ) if resultado and resultado.sucesso else card_status(
                    "Erro na Execução",
                    resultado.mensagem if resultado else "Erro desconhecido",
                    "error"
                ) if resultado and not resultado.sucesso else None,

                # Arquivos gerados
                html.div(
                    {"style": {"margin_top": "1rem"}},
                    html.h4("📁 Arquivos Gerados:"),
                    html.ul(
                        *[
                            html.li(
                                {"key": f"arq-{i}"},
                                arquivo
                            )
                            for i, arquivo in enumerate(resultado.arquivos_gerados)
                        ] if resultado and resultado.arquivos_gerados else [
                            html.li("Nenhum arquivo gerado")
                        ]
                    )
                ) if resultado and resultado.sucesso else None
            ) if resultado else None

        ) if executando or resultado else html.div(
            {
                "style": {
                    "text_align": "center",
                    "padding": "3rem",
                    "color": "#999",
                }
            },
            html.div(
                {"style": {"font_size": "3rem", "margin_bottom": "1rem"}},
                "📊"
            ),
            html.h3("Pronto para gerar relatório"),
            html.p("Configure a data e versão acima e clique em 'Gerar Relatório'")
        )
    )
