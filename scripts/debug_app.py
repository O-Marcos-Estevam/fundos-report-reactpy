"""
Script de debug para verificar o estado da aplicação
"""
import sys
from pathlib import Path

# Adicionar src ao path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from services.state_manager import get_state_manager

def main():
    print("=" * 60)
    print("DEBUG: Estado do State Manager")
    print("=" * 60)

    state_manager = get_state_manager()

    print(f"\nPagina atual: {state_manager.pagina_atual}")
    print(f"Versao modulo: {state_manager.versao_modulo}")
    print(f"Modo escuro: {state_manager.modo_escuro}")

    ultima_exec = state_manager.ultima_execucao
    print(f"\nUltima execucao: {ultima_exec}")

    if ultima_exec:
        print(f"  - Data: {ultima_exec.data_relatorio}")
        print(f"  - Status: {ultima_exec.status}")
        print(f"  - Fundos processados: {ultima_exec.fundos_processados}")
        print(f"  - Total fundos: {len(ultima_exec.fundos)}")
        print(f"  - PL Total: R$ {ultima_exec.total_pl:,.2f}")
        print(f"  - Caixa Total: R$ {ultima_exec.total_caixa:,.2f}")

        if ultima_exec.fundos:
            print(f"\n  Fundos:")
            for nome in list(ultima_exec.fundos.keys())[:3]:
                fundo = ultima_exec.fundos[nome]
                print(f"    - {fundo.nome}: R$ {fundo.pl:,.2f}")
    else:
        print("  [AVISO] Nenhuma execucao encontrada!")
        print("  Execute: python fundos_report_reactpy/populate_sample_data.py")

    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
