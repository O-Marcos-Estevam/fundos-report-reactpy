"""
Aplicação Principal
FastAPI + ReactPy - Relatório Diário de Fundos
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from reactpy import component, html, use_state
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
from datetime import datetime

# Importar componentes e páginas
from components.layout import header, navegacao
from pages.executar import pagina_executar
from pages.dashboard import pagina_dashboard
from pages.lamina_fundos import pagina_lamina_fundos
from pages.historico import pagina_historico
from services.state_manager import get_state_manager
from app.config import AppConfig


@component
def app_root():
    """Componente raiz da aplicação"""

    state_manager = get_state_manager()

    # Estado da página atual
    pagina_atual, set_pagina = use_state(state_manager.pagina_atual)

    def mudar_pagina(nova_pagina: str):
        """Muda a página atual"""
        set_pagina(nova_pagina)
        state_manager.set_pagina(nova_pagina)

    # Renderizar página baseada no estado
    def renderizar_pagina():
        """Renderiza a página atual"""
        if pagina_atual == "executar":
            return pagina_executar()
        elif pagina_atual == "dashboard":
            return pagina_dashboard()
        elif pagina_atual == "lamina":
            return pagina_lamina_fundos()
        elif pagina_atual == "historico":
            return pagina_historico()
        elif pagina_atual == "configuracoes":
            return pagina_configuracoes()
        else:
            return pagina_executar()

    return html.div(
        {
            "style": {
                "font_family": "Arial, sans-serif",
                "background": "#f5f7fa",
                "min_height": "100vh",
                "padding": "20px",
            }
        },
        # Header
        header(),

        # Navegação
        navegacao(pagina_atual, mudar_pagina),

        # Conteúdo da página
        html.div(
            {"style": {"margin_top": "2rem"}},
            renderizar_pagina()
        ),

        # Footer
        html.footer(
            {
                "style": {
                    "text_align": "center",
                    "padding": "2rem",
                    "margin_top": "3rem",
                    "color": "#999",
                    "font_size": "0.9rem",
                }
            },
            html.p(
                {"style": {"margin": "0"}},
                f"Relatório Diário de Fundos - Versão {AppConfig.APP_VERSION}"
            ),
            html.p(
                {"style": {"margin": "0.5rem 0 0 0"}},
                f"© {datetime.now().year} - Arquitetura Modular com ReactPy"
            )
        )
    )


@component
def pagina_configuracoes():
    """Página de configurações (placeholder)"""
    from components.layout import container_pagina
    from components.cards import card_info
    from components.forms import checkbox

    state_manager = get_state_manager()
    config = state_manager.config_avancada

    def toggle_config(key: str):
        """Toggle configuração"""
        def handler(value: bool):
            state_manager.update_config(key, value)
        return handler

    return container_pagina(
        html.h2(
            {"style": {"margin": "0 0 2rem 0", "color": "#333"}},
            "⚙️ Configurações"
        ),

        card_info(
            "🎨 Aparência",
            checkbox(
                "Modo Escuro",
                state_manager.modo_escuro,
                lambda v: state_manager.toggle_modo_escuro()
            )
        ),

        card_info(
            "🔧 Sistema",
            checkbox(
                "Auto-refresh após execução",
                config.get('auto_refresh', False),
                toggle_config('auto_refresh')
            ),
            checkbox(
                "Notificações",
                config.get('notificacoes', True),
                toggle_config('notificacoes')
            ),
            checkbox(
                "Backup automático",
                config.get('backup_automatico', True),
                toggle_config('backup_automatico')
            )
        ),

        card_info(
            "ℹ️ Informações do Sistema",
            html.div(
                html.p(
                    {"style": {"margin": "0.5rem 0"}},
                    html.strong("Versão da Aplicação: "),
                    AppConfig.APP_VERSION
                ),
                html.p(
                    {"style": {"margin": "0.5rem 0"}},
                    html.strong("Módulo Atual: "),
                    state_manager.versao_modulo
                ),
                html.p(
                    {"style": {"margin": "0.5rem 0"}},
                    html.strong("Banco de Dados: "),
                    "Conectado ✅"
                )
            )
        )
    )


# ============================================================================
# Configuração do FastAPI
# ============================================================================

# Criar aplicação FastAPI
app = FastAPI(
    title="Relatório Diário de Fundos",
    description="Sistema modular de geração de relatórios com ReactPy",
    version=AppConfig.APP_VERSION
)

# Configurar ReactPy
configure(app, app_root)

# ============================================================================
# Execução
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("  Relatório Diário de Fundos - ReactPy")
    print(f"  Versão {AppConfig.APP_VERSION}")
    print("=" * 70)
    print()
    print(f"  Iniciando servidor em http://{AppConfig.HOST}:{AppConfig.PORT}")
    print()
    print("  Páginas disponíveis:")
    print("  - Executar: Geração de relatórios")
    print("  - Dashboard: Métricas e análises")
    print("  - Lâmina: Detalhes de fundos")
    print("  - Histórico: Execuções anteriores")
    print()
    print("  Pressione CTRL+C para parar")
    print("=" * 70)

    uvicorn.run(
        app,
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        log_level="info"
    )
