"""
Teste do fluxo completo de execução
"""
import sys
sys.path.insert(0, r'c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy\src')

from datetime import datetime, timedelta
from services.report_executor import ReportExecutor

print("=" * 70)
print("TESTE DE EXECUÇÃO COMPLETA")
print("=" * 70)

try:
    # Data
    data = datetime.now() - timedelta(days=1)
    print(f"\n1. Data do relatório: {data.strftime('%d/%m/%Y')}")

    # Criar executor
    print("\n2. Criando executor V6...")
    executor = ReportExecutor('V6')
    print("   ✓ Executor criado")

    # Importar módulo
    print("\n3. Importando módulo...")
    sucesso, erro = executor.importar_modulo()
    if not sucesso:
        print(f"   ✗ ERRO: {erro}")
        sys.exit(1)
    print(f"   ✓ Módulo importado: {executor.modulo.__name__}")
    print(f"   ✓ Classe: {executor.ReportClass.__name__}")

    # Testar criação de instância
    print("\n4. Criando instância do relatório...")
    try:
        report = executor.ReportClass()
        print("   ✓ Instância criada")
    except Exception as e:
        print(f"   ✗ ERRO ao criar instância: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Testar validação de ambiente
    print("\n5. Testando validação de ambiente...")
    try:
        valido = report.validar_ambiente()
        if valido:
            print("   ✓ Ambiente validado")
        else:
            print("   ✗ Ambiente inválido")
            sys.exit(1)
    except Exception as e:
        print(f"   ✗ ERRO na validação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "=" * 70)
    print("TODOS OS TESTES PASSARAM!")
    print("=" * 70)
    print("\nO sistema está pronto para executar relatórios.")
    print("Se o botão não funciona na interface, pode ser um problema de JavaScript/ReactPy.")

except Exception as e:
    print(f"\n✗ ERRO GERAL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
