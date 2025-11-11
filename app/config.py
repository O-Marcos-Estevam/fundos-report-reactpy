"""
Configurações Centralizadas da Aplicação
Gerencia caminhos, constantes e configurações do sistema
"""

import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass

# ============================================================================
# CAMINHOS BASE
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_MODULO = r"C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\0. Python"
DB_PATH = r"C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\03. Arquivos Rotina\09. Base_de_Dados\Base Fundos_V2.accdb"

# Diretórios da aplicação
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"
CSS_DIR = STATIC_DIR / "css"

# Arquivo de histórico
HISTORICO_FILE = DATA_DIR / "historico.json"

# Criar diretórios se não existirem
DATA_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
CSS_DIR.mkdir(exist_ok=True)

# ============================================================================
# CONFIGURAÇÕES DE MÓDULOS DE RELATÓRIO
# ============================================================================

@dataclass
class ModuloConfig:
    """Configuração de um módulo de relatório"""
    versao: str
    nome_arquivo: str
    nome_classe: str
    nomes_possiveis: list[str]
    descricao: str

MODULOS_RELATORIO: Dict[str, ModuloConfig] = {
    'V6': ModuloConfig(
        versao='V6',
        nome_arquivo='Relatório_Fundos_V6_Optimized.py',
        nome_classe='ReportDiarioFundosV6',
        nomes_possiveis=[
            "Relatório_Fundos_V6_Optimized",
            "relatorio_fundos_v6_optimized",
            "RelatórioFundosV6Optimized",
        ],
        descricao='V6 Optimized - Performance 70% mais rápida, análise preditiva'
    ),
    'V5': ModuloConfig(
        versao='V5',
        nome_arquivo='Relatório_Fundos_V5_Enhanced.py',
        nome_classe='ReportDiarioFundosV5',
        nomes_possiveis=[
            "Relatório_Fundos_V5_Enhanced",
            "relatorio_fundos_v5_enhanced",
            "RelatórioFundosV5Enhanced",
        ],
        descricao='V5 Enhanced - Relatório com 3 abas e formatação avançada'
    ),
    'V4': ModuloConfig(
        versao='V4',
        nome_arquivo='Relatório_Fundos_V4.py',
        nome_classe='ReportDiarioFundosV4',
        nomes_possiveis=[
            "Relatório_Fundos_V4",
            "relatorio_fundos_v4",
            "RelatórioFundosV4",
            "report_diario_v4",
            "relatorio_v4"
        ],
        descricao='V4 Legacy - Versão anterior para compatibilidade'
    )
}

VERSAO_PADRAO = 'V6'

# ============================================================================
# CONFIGURAÇÕES DA APLICAÇÃO
# ============================================================================

class AppConfig:
    """Configurações gerais da aplicação"""

    # Informações da aplicação
    APP_TITLE = "Relatório Diário de Fundos"
    APP_VERSION = "7.0"
    APP_SUBTITLE = "Sistema Modular com ReactPy"

    # Configurações de servidor
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 8000))  # Suporta variável de ambiente para deploy
    DEBUG = os.environ.get("DEBUG", "true").lower() == "true"

    # Modo de dados (para deploy em nuvem sem Access)
    USE_MOCK_DATA = os.environ.get("USE_MOCK_DATA", "false").lower() == "true"

    # Configurações de UI
    THEME_COLORS = {
        'primary': '#667eea',
        'secondary': '#764ba2',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'info': '#3b82f6'
    }

    # Configurações de histórico
    MAX_HISTORICO_ENTRIES = 50

    # Configurações de cache
    CACHE_TTL = 300  # 5 minutos

    # Configurações de email
    EMAIL_CAMINHO_BASE = r"C:\bloko\Fundos - Documentos"

    @classmethod
    def get_color(cls, name: str) -> str:
        """Retorna cor do tema"""
        return cls.THEME_COLORS.get(name, '#667eea')

# ============================================================================
# CONFIGURAÇÕES DE ESTADO
# ============================================================================

def get_default_state() -> Dict[str, Any]:
    """Retorna estado padrão da aplicação"""
    return {
        'historico': [],
        'modo_escuro': False,
        'logs_execucao': [],
        'ultima_execucao': None,
        'versao_modulo': VERSAO_PADRAO,
        'pagina_atual': 'executar',
        'config_avancada': {
            'auto_refresh': False,
            'notificacoes': True,
            'backup_automatico': True
        }
    }

# ============================================================================
# VALIDAÇÕES
# ============================================================================

def validar_ambiente() -> tuple[bool, list[str]]:
    """
    Valida se o ambiente está configurado corretamente

    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []

    # Verificar banco de dados
    if not os.path.exists(DB_PATH):
        errors.append(f"Banco de dados não encontrado: {DB_PATH}")

    # Verificar diretório de módulos
    if not os.path.exists(CAMINHO_MODULO):
        errors.append(f"Diretório de módulos não encontrado: {CAMINHO_MODULO}")

    # Verificar pelo menos um módulo de relatório
    modulo_encontrado = False
    for config in MODULOS_RELATORIO.values():
        caminho = os.path.join(CAMINHO_MODULO, config.nome_arquivo)
        if os.path.exists(caminho):
            modulo_encontrado = True
            break

    if not modulo_encontrado:
        errors.append("Nenhum módulo de relatório encontrado")

    return len(errors) == 0, errors

# ============================================================================
# UTILITÁRIOS
# ============================================================================

def get_modulo_config(versao: str) -> ModuloConfig:
    """Retorna configuração do módulo por versão"""
    return MODULOS_RELATORIO.get(versao, MODULOS_RELATORIO[VERSAO_PADRAO])

def get_caminho_modulo(versao: str) -> str:
    """Retorna caminho completo do módulo"""
    config = get_modulo_config(versao)
    return os.path.join(CAMINHO_MODULO, config.nome_arquivo)
