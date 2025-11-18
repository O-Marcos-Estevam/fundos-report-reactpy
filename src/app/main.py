"""
Aplicação Principal
FastAPI + ReactPy - Relatório Diário de Fundos
"""

import sys
import os
import logging
from pathlib import Path

# Adicionar diretório raiz ao Python path (agora dentro de src/)
ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = ROOT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reactpy import component, html, use_state
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from datetime import datetime

# Importar componentes e páginas
from components.layout_v2 import app_shell_v2
from components.forms import checkbox
# Páginas modernas
from pages.dashboard_modern import pagina_dashboard_moderna
from pages.dashboard_ultra import pagina_dashboard_ultra
from pages.dashboard_customizavel import pagina_dashboard_customizavel
from pages.executar_modern import pagina_executar_moderna
from pages.historico_modern import pagina_historico_moderna
from pages.lamina_fundos_modern import pagina_lamina_fundos_moderna
from services.state_manager import get_state_manager
from app.config import AppConfig
from app.init_data import init_sample_data

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@component
def pagina_configuracoes():
    """Página de configurações V2"""
    state_manager = get_state_manager()
    config = state_manager.config_avancada

    def toggle_config(key: str):
        """Toggle configuração com validação"""
        # Validar chave de configuração
        allowed_keys = {'auto_refresh', 'notificacoes', 'backup_automatico'}
        if key not in allowed_keys:
            logger.warning(f"Tentativa de modificar configuração inválida: {key}")
            return lambda v: None

        def handler(value: bool):
            try:
                if not isinstance(value, bool):
                    logger.error(f"Valor inválido para configuração {key}: {value}")
                    return
                state_manager.update_config(key, value)
                logger.info(f"Configuração {key} atualizada para {value}")
            except Exception as e:
                logger.error(f"Erro ao atualizar configuração {key}: {e}")
        return handler

    return html.div(
        {"class": "page-section animate-fade-in"},
        html.div(
            {"class": "card animate-pop"},
            html.div({"class": "card-header"},
                html.h3({"class": "card-title"}, "⚙️ Configurações")
            ),
            html.div(
                {"style": {"display": "flex", "flexDirection": "column", "gap": "2rem", "padding": "1.5rem"}},
                
                # Aparência
                html.div(
                    html.h4({"style": {"margin": "0 0 1rem", "fontSize": "1.1rem"}}, "🎨 Aparência"),
                    checkbox(
                        "Modo Escuro",
                        state_manager.modo_escuro,
                        lambda v: state_manager.toggle_modo_escuro()
                    )
                ),

                # Sistema
                html.div(
                    html.h4({"style": {"margin": "0 0 1rem", "fontSize": "1.1rem"}}, "🔧 Sistema"),
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

                # Informações
                html.div(
                    html.h4({"style": {"margin": "0 0 1rem", "fontSize": "1.1rem"}}, "ℹ️ Informações do Sistema"),
                    html.div(
                        {"class": "grid grid-3", "style": {"gap": "1rem"}},
                        html.div({"class": "stat-box"},
                            html.span({"class": "stat-label"}, "Versão"),
                            html.span({"class": "stat-value"}, AppConfig.APP_VERSION)
                        ),
                        html.div({"class": "stat-box"},
                            html.span({"class": "stat-label"}, "Módulo"),
                            html.span({"class": "stat-value"}, state_manager.versao_modulo)
                        ),
                        html.div({"class": "stat-box"},
                            html.span({"class": "stat-label"}, "Banco de Dados"),
                            html.span({"class": "stat-value"}, "✅ Conectado")
                        )
                    )
                )
            )
        )
    )


# Dicionário de rotas da aplicação
ROTAS_PAGINAS = {
    "executar": pagina_executar_moderna,
    "dashboard": pagina_dashboard_ultra,
    "dashboard_modern": pagina_dashboard_moderna,
    "dashboard_customizavel": pagina_dashboard_customizavel,
    "lamina": pagina_lamina_fundos_moderna,
    "historico": pagina_historico_moderna,
    "configuracoes": pagina_configuracoes,
}


@component
def app_root():
    """Componente raiz da aplicação"""

    state_manager = get_state_manager()

    # Estado local para controlar re-renderização
    pagina_atual, set_pagina_atual = use_state(state_manager.pagina_atual)

    def mudar_pagina(nova_pagina: str):
        """Muda a página atual e sincroniza com state_manager"""
        try:
            if nova_pagina not in ROTAS_PAGINAS:
                logger.warning(f"Tentativa de navegar para página inválida: {nova_pagina}")
                nova_pagina = "executar"

            # Atualizar estado local (triggera re-render)
            set_pagina_atual(nova_pagina)
            # Sincronizar com state_manager
            state_manager.set_pagina(nova_pagina)
            logger.info(f"Navegação para página: {nova_pagina}")
        except Exception as e:
            logger.error(f"Erro ao mudar página: {e}")

    # Renderizar página baseada no estado
    def renderizar_pagina():
        """Renderiza a página atual usando dicionário de rotas"""
        try:
            pagina_func = ROTAS_PAGINAS.get(pagina_atual, pagina_executar_moderna)
            return pagina_func()
        except Exception as e:
            logger.error(f"Erro ao renderizar página {pagina_atual}: {e}")
            # Fallback para página de execução em caso de erro
            return pagina_executar_moderna()

    return html._(
        html.head(
            html.meta({"charset": "utf-8"}),
            html.meta({"name": "viewport", "content": "width=device-width,initial-scale=1"}),
            html.link({"rel": "stylesheet", "href": "/static/css/design-system.css"}),
            html.link({"rel": "stylesheet", "href": "/static/css/components.css"}),
            html.link({"rel": "stylesheet", "href": "/static/css/dashboard-ultra.css"})
        ),
        app_shell_v2(
            pagina_atual,
            mudar_pagina,
            renderizar_pagina()
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

# Montar diretório de arquivos estáticos
static_dir = PROJECT_ROOT / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    logger.info(f"Arquivos estáticos montados em: {static_dir}")
else:
    logger.warning(f"Diretório de arquivos estáticos não encontrado: {static_dir}")

# Adicionar endpoint de diagnóstico
from app.diagnostico import router as diagnostico_router
app.include_router(diagnostico_router)

# Configurar ReactPy
configure(app, app_root)

# ============================================================================
# Inicializar dados de exemplo (se necessário)
# ============================================================================
# Controle via variável de ambiente LOAD_SAMPLE_DATA (padrão: true)
# Para desabilitar: export LOAD_SAMPLE_DATA=false (Linux/Mac)
#                   set LOAD_SAMPLE_DATA=false (Windows)
init_result = init_sample_data()
if init_result:
    logger.info(f"Sistema inicializado com {init_result['fundos_count']} fundos de exemplo")

# ============================================================================
# Execução
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    import sys
    sys.path.insert(0, str(ROOT_DIR))

    from utils.server_utils import find_available_port, get_server_info

    # Tentar encontrar porta disponível
    port = AppConfig.PORT
    if not find_available_port(port, 1):
        print(f"[WARNING] Porta {port} já está em uso. Procurando porta disponível...")
        available_port = find_available_port(port, 10)
        if available_port:
            port = available_port
            print(f"[INFO] Usando porta alternativa: {port}")
        else:
            print(f"[ERROR] Nenhuma porta disponível encontrada entre {port} e {port + 9}")
            print(f"[INFO] Você pode:")
            print(f"  1. Fechar o processo que está usando a porta {AppConfig.PORT}")
            print(f"  2. Usar: set PORT=8001 && python src/app/main.py")
            sys.exit(1)

    # Obter informações do servidor
    server_info = get_server_info(AppConfig.HOST, port)

    # Configurar encoding para suportar emojis no Windows
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 70)
    print("  Relatório Diário de Fundos - ReactPy")
    print(f"  Versão {AppConfig.APP_VERSION}")
    print("=" * 70)
    print()
    print("  🚀 Servidor iniciado com sucesso!")
    print()
    print("  📍 URLs de acesso:")
    print(f"     - Local:   {server_info['urls']['local']}")
    if AppConfig.HOST == "0.0.0.0":
        print(f"     - Rede:    {server_info['urls']['network']}")
    print()
    print(f"  💻 Hostname: {server_info['hostname']}")
    print(f"  🌐 IP Local: {server_info['local_ip']}")
    print()
    print("  📋 Páginas disponíveis:")
    print("     - Executar: Geração de relatórios")
    print("     - Dashboard: Métricas e análises")
    print("     - Dashboard Customizável: Layout personalizável")
    print("     - Lâmina: Detalhes de fundos")
    print("     - Histórico: Execuções anteriores")
    print()
    print("  ⌨️  Pressione CTRL+C para parar")
    print("=" * 70)

    try:
        uvicorn.run(
            app,
            host=AppConfig.HOST,
            port=port,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n")
        print("=" * 70)
        print("  ✅ Servidor encerrado com sucesso!")
        print("=" * 70)
