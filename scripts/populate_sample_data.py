"""
Script para popular dados de exemplo no State Manager
Para testar o dashboard sem executar um relatório real
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adicionar src ao path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from models.fundo import FundoData
from models.execucao import ExecucaoInfo
from services.state_manager import get_state_manager


def criar_dados_exemplo():
    """Cria dados de exemplo para testar"""

    # Criar fundos de exemplo
    fundos = {
        "FUNDO_A": FundoData(
            nome="Alpha Capital FIA",
            tipo="Multimercado",
            pl=15_000_000_000,
            pl_d1=14_800_000_000,
            pl_d7=14_500_000_000,
            pl_d30=14_000_000_000,
            caixa_total=3_000_000_000,
            caixa_bancario=2_500_000_000,
            caixa_reag_ii=500_000_000,
            devido_taxas=15_000_000,
        ),
        "FUNDO_B": FundoData(
            nome="Beta Investimentos FI",
            tipo="Renda Fixa",
            pl=8_500_000_000,
            pl_d1=8_450_000_000,
            pl_d7=8_300_000_000,
            pl_d30=8_100_000_000,
            caixa_total=1_200_000_000,
            caixa_bancario=1_000_000_000,
            caixa_reag_ii=200_000_000,
            devido_taxas=5_000_000,
        ),
        "FUNDO_C": FundoData(
            nome="Gamma Hedge Fund",
            tipo="Multimercado",
            pl=22_000_000_000,
            pl_d1=21_900_000_000,
            pl_d7=21_500_000_000,
            pl_d30=21_000_000_000,
            caixa_total=2_500_000_000,
            caixa_bancario=2_000_000_000,
            caixa_reag_ii=500_000_000,
            devido_taxas=20_000_000,
        ),
        "FUNDO_D": FundoData(
            nome="Delta Acoes FIA",
            tipo="Acoes",
            pl=5_000_000_000,
            pl_d1=4_950_000_000,
            pl_d7=4_800_000_000,
            pl_d30=4_600_000_000,
            caixa_total=450_000_000,
            caixa_bancario=400_000_000,
            caixa_reag_ii=50_000_000,
            devido_taxas=3_000_000,
        ),
        "FUNDO_E": FundoData(
            nome="Epsilon Credito FI",
            tipo="Credito Privado",
            pl=12_000_000_000,
            pl_d1=11_950_000_000,
            pl_d7=11_800_000_000,
            pl_d30=11_500_000_000,
            caixa_total=1_800_000_000,
            caixa_bancario=1_500_000_000,
            caixa_reag_ii=300_000_000,
            devido_taxas=8_000_000,
        ),
    }

    # Criar execução de exemplo
    execucao = ExecucaoInfo(
        data_relatorio=datetime.now() - timedelta(days=1),
        data_execucao=datetime.now(),
        status="sucesso",
        mensagem="Relatorio gerado com sucesso (dados de exemplo)",
        tempo_execucao=45.5,
        fundos_processados=len(fundos),
        fundos=fundos,
        versao_modulo="V6",
        nome_modulo="Exemplo",
        arquivos_gerados=["relatorio_exemplo.xlsx"]
    )

    # Adicionar logs de exemplo
    execucao.add_log("Iniciando processamento de dados...")
    execucao.add_log("Conectando ao banco de dados...")
    execucao.add_log("Carregando fundos...")
    execucao.add_log(f"Processados {len(fundos)} fundos")
    execucao.add_log("Gerando relatorio Excel...")
    execucao.add_log("Relatorio gerado com sucesso!")

    return execucao


def main():
    """Popula o state manager com dados de exemplo"""
    print("Populando dados de exemplo no State Manager...")
    print("=" * 60)

    # Obter state manager
    state_manager = get_state_manager()

    # Criar dados de exemplo
    execucao = criar_dados_exemplo()

    # Adicionar ao state manager
    state_manager.set_ultima_execucao(execucao)

    print(f"\n[OK] Execucao de exemplo criada:")
    print(f"  - Data: {execucao.data_relatorio.strftime('%Y-%m-%d')}")
    print(f"  - Fundos: {execucao.fundos_processados}")
    print(f"  - PL Total: R$ {execucao.total_pl:,.2f}".replace(",", "."))
    print(f"  - Caixa Total: R$ {execucao.total_caixa:,.2f}".replace(",", "."))
    print(f"  - Status: {execucao.status}")
    print("\n" + "=" * 60)
    print("Agora o dashboard deve mostrar os dados!")
    print("Acesse: http://localhost:8000")
    print("=" * 60)


if __name__ == '__main__':
    main()
