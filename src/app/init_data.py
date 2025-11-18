"""
Módulo de Inicialização de Dados
Gerencia a criação de dados de exemplo para a aplicação
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


def should_load_sample_data() -> bool:
    """
    Verifica se deve carregar dados de exemplo

    Returns:
        bool: True se deve carregar dados de exemplo
    """
    # Verificar variável de ambiente
    load_sample = os.getenv('LOAD_SAMPLE_DATA', 'true').lower()
    return load_sample in ('true', '1', 'yes', 'sim')


def init_sample_data(force: bool = False) -> Optional[dict]:
    """
    Inicializa dados de exemplo se não houver execução

    Args:
        force: Se True, força a criação de dados mesmo se já existirem

    Returns:
        dict: Informações sobre a inicialização ou None se não foi necessária
    """
    from models.fundo import FundoData
    from models.execucao import ExecucaoInfo
    from services.state_manager import get_state_manager

    state_manager = get_state_manager()

    # Verificar se deve carregar dados de exemplo
    if not should_load_sample_data() and not force:
        logger.info("Carregamento de dados de exemplo desabilitado via configuração")
        return None

    # Verificar se já existe execução
    if state_manager.ultima_execucao is not None and not force:
        logger.info("Dados de execução já existem, pulando inicialização de exemplo")
        return None

    try:
        # Criar fundos de exemplo com dados realistas
        fundos = {
            "FUNDO_A": FundoData(
                nome="Alpha Capital FIA",
                tipo="Multimercado",
                pl=15_234_567_890,
                pl_d1=15_189_432_120,
                caixa_total=3_045_123_456,
            ),
            "FUNDO_B": FundoData(
                nome="Beta Investimentos FIRF",
                tipo="Renda Fixa",
                pl=8_567_234_120,
                pl_d1=8_542_198_340,
                caixa_total=1_245_678_901,
            ),
            "FUNDO_C": FundoData(
                nome="Gamma Hedge Fund FIM",
                tipo="Multimercado",
                pl=22_345_678_901,
                pl_d1=22_198_765_432,
                caixa_total=2_567_890_123,
            ),
            "FUNDO_D": FundoData(
                nome="Delta Crédito Privado FI",
                tipo="Renda Fixa",
                pl=5_890_123_456,
                pl_d1=5_876_543_210,
                caixa_total=890_234_567,
            ),
            "FUNDO_E": FundoData(
                nome="Epsilon Long Short FIA",
                tipo="Multimercado",
                pl=12_456_789_012,
                pl_d1=12_401_234_567,
                caixa_total=1_890_456_789,
            ),
        }

        # Criar execução de exemplo
        execucao = ExecucaoInfo(
            data_relatorio=datetime.now() - timedelta(days=1),
            data_execucao=datetime.now(),
            status="sucesso",
            mensagem="🎭 MODO DEMONSTRAÇÃO - Dados de exemplo realistas para preview",
            tempo_execucao=8.7,  # Tempo realista do V6
            fundos_processados=len(fundos),
            fundos=fundos,
            versao_modulo="V6",
        )

        state_manager.set_ultima_execucao(execucao)

        logger.info("Dados de exemplo carregados com sucesso")
        logger.info(f"  - {len(fundos)} fundos criados")
        logger.info(f"  - Execução: {execucao.status}")

        return {
            "fundos_count": len(fundos),
            "execucao_status": execucao.status,
            "data_execucao": execucao.data_execucao,
        }

    except Exception as e:
        logger.error(f"Erro ao inicializar dados de exemplo: {e}")
        return None


def clear_sample_data() -> bool:
    """
    Remove dados de exemplo do state manager

    Returns:
        bool: True se os dados foram removidos com sucesso
    """
    from services.state_manager import get_state_manager

    try:
        state_manager = get_state_manager()
        state_manager.set_ultima_execucao(None)
        logger.info("Dados de exemplo removidos")
        return True
    except Exception as e:
        logger.error(f"Erro ao remover dados de exemplo: {e}")
        return False
