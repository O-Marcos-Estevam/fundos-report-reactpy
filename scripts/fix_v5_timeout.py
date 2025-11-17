"""
Script para adicionar timeout na conexão do V5
"""

import sys
sys.path.insert(0, r'C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\0. Python')

# Importar e patchear o módulo V5
try:
    import Relatório_Fundos_V5_Enhanced as v5_module

    # Salvar o método original
    original_conectar = v5_module.ReportDiarioFundosV5.conectar_access

    # Criar versão com timeout
    def conectar_access_with_timeout(self):
        """Conecta ao banco Access com timeout"""
        import pyodbc
        try:
            conn_str = (
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                f'DBQ={self.DB_PATH};'
            )
            # Adicionar timeout de 30 segundos
            conn = pyodbc.connect(conn_str, timeout=30)
            conn.timeout = 30  # Query timeout
            self.print_success("Conexão com banco Access estabelecida (com timeout 30s)")
            return conn
        except Exception as e:
            self.print_error(f"Erro ao conectar ao Access: {e}")
            raise

    # Aplicar patch
    v5_module.ReportDiarioFundosV5.conectar_access = conectar_access_with_timeout

    print("✓ Patch aplicado com sucesso ao módulo V5!")
    print("  - Timeout de conexão: 30s")
    print("  - Timeout de query: 30s")

except Exception as e:
    print(f"✗ Erro ao aplicar patch: {e}")
    import traceback
    traceback.print_exc()
