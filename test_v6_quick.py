"""
Teste rápido do V6
"""
import sys
sys.path.insert(0, r'c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy\src')
sys.path.insert(0, r'C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\0. Python')

from datetime import datetime, timedelta
from services.report_executor import ReportExecutor

print("=" * 70)
print("TESTE RÁPIDO V6")
print("=" * 70)

try:
    # Data de ontem
    data = datetime.now() - timedelta(days=1)
    print(f"\nData do relatório: {data.strftime('%d/%m/%Y')}")

    # Criar executor V6
    print("\n1. Criando executor V6...")
    executor = ReportExecutor('V6')

    # Importar módulo
    print("2. Importando módulo...")
    sucesso, erro = executor.importar_modulo()
    if not sucesso:
        print(f"   ERRO: {erro}")
        sys.exit(1)
    print(f"   OK - Módulo: {executor.modulo.__name__}")

    # Testar conexão
    print("3. Testando conexão...")
    sucesso_conn, msg = executor.testar_conexao()
    if not sucesso_conn:
        print(f"   ERRO: {msg}")
        sys.exit(1)
    print(f"   OK - {msg}")

    print("\n" + "=" * 70)
    print("TODOS OS TESTES PASSARAM!")
    print("=" * 70)
    print("\nO V6 está pronto para uso na interface web.")
    print("Recarregue a página e selecione V6 para executar.")

except Exception as e:
    print(f"\nERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
