"""
Script de Conversão: Microsoft Access → SQLite
Converte o banco de dados Access (.accdb) para SQLite (.db)
"""

import sys
import sqlite3
import pyodbc
import logging
from pathlib import Path
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AccessToSQLiteConverter:
    """Conversor de Access para SQLite"""

    def __init__(self, access_db_path: str, sqlite_db_path: str):
        """
        Inicializa o conversor

        Args:
            access_db_path: Caminho para o arquivo .accdb
            sqlite_db_path: Caminho para o arquivo .db de destino
        """
        self.access_db_path = Path(access_db_path)
        self.sqlite_db_path = Path(sqlite_db_path)

        if not self.access_db_path.exists():
            raise FileNotFoundError(f"Arquivo Access não encontrado: {self.access_db_path}")

    def get_access_connection(self) -> pyodbc.Connection:
        """Cria conexão com banco Access"""
        conn_str = (
            f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};"
            f"DBQ={self.access_db_path};"
        )
        logger.info(f"Conectando ao Access: {self.access_db_path}")
        return pyodbc.connect(conn_str)

    def get_sqlite_connection(self) -> sqlite3.Connection:
        """Cria conexão com banco SQLite"""
        logger.info(f"Conectando ao SQLite: {self.sqlite_db_path}")
        return sqlite3.connect(self.sqlite_db_path)

    def get_table_names(self, access_conn: pyodbc.Connection) -> List[str]:
        """Lista todas as tabelas do Access"""
        cursor = access_conn.cursor()
        tables = []

        for table_info in cursor.tables(tableType='TABLE'):
            table_name = table_info.table_name
            # Ignorar tabelas do sistema
            if not table_name.startswith('MSys'):
                tables.append(table_name)

        logger.info(f"Encontradas {len(tables)} tabelas no Access")
        return tables

    def convert_access_type_to_sqlite(self, access_type: str) -> str:
        """
        Converte tipos de dados do Access para SQLite

        Args:
            access_type: Tipo de dados do Access

        Returns:
            str: Tipo de dados do SQLite
        """
        type_mapping = {
            'int': 'INTEGER',
            'long': 'INTEGER',
            'short': 'INTEGER',
            'byte': 'INTEGER',
            'single': 'REAL',
            'double': 'REAL',
            'currency': 'REAL',
            'decimal': 'REAL',
            'datetime': 'TEXT',
            'date': 'TEXT',
            'time': 'TEXT',
            'text': 'TEXT',
            'varchar': 'TEXT',
            'memo': 'TEXT',
            'longtext': 'TEXT',
            'bit': 'INTEGER',
            'yesno': 'INTEGER',
            'binary': 'BLOB',
            'varbinary': 'BLOB',
        }

        access_type_lower = access_type.lower()

        for key, value in type_mapping.items():
            if key in access_type_lower:
                return value

        # Padrão: TEXT
        return 'TEXT'

    def get_table_schema(self, access_conn: pyodbc.Connection, table_name: str) -> List[Dict[str, Any]]:
        """
        Obtém o schema de uma tabela do Access

        Args:
            access_conn: Conexão com o Access
            table_name: Nome da tabela

        Returns:
            List[Dict]: Lista de colunas com metadados
        """
        cursor = access_conn.cursor()
        columns = []

        for col in cursor.columns(table=table_name):
            columns.append({
                'name': col.column_name,
                'type': col.type_name,
                'nullable': col.nullable == 1,
                'size': col.column_size
            })

        return columns

    def create_sqlite_table(self, sqlite_conn: sqlite3.Connection, table_name: str, columns: List[Dict[str, Any]]):
        """
        Cria tabela no SQLite baseada no schema do Access

        Args:
            sqlite_conn: Conexão com SQLite
            table_name: Nome da tabela
            columns: Lista de colunas
        """
        cursor = sqlite_conn.cursor()

        # Construir DDL
        col_definitions = []
        for col in columns:
            sqlite_type = self.convert_access_type_to_sqlite(col['type'])
            nullable = "" if col['nullable'] else "NOT NULL"
            col_definitions.append(f'"{col["name"]}" {sqlite_type} {nullable}'.strip())

        ddl = f'CREATE TABLE IF NOT EXISTS "{table_name}" (\n  ' + ',\n  '.join(col_definitions) + '\n);'

        logger.debug(f"DDL: {ddl}")
        cursor.execute(ddl)
        sqlite_conn.commit()
        logger.info(f"✓ Tabela criada: {table_name} ({len(columns)} colunas)")

    def copy_table_data(self, access_conn: pyodbc.Connection, sqlite_conn: sqlite3.Connection, table_name: str):
        """
        Copia dados de uma tabela do Access para SQLite

        Args:
            access_conn: Conexão com Access
            sqlite_conn: Conexão com SQLite
            table_name: Nome da tabela
        """
        access_cursor = access_conn.cursor()
        sqlite_cursor = sqlite_conn.cursor()

        # Ler dados do Access
        try:
            access_cursor.execute(f'SELECT * FROM "{table_name}"')
            rows = access_cursor.fetchall()

            if not rows:
                logger.info(f"  ⚠ Tabela vazia: {table_name}")
                return

            # Obter nomes de colunas
            column_names = [desc[0] for desc in access_cursor.description]

            # Preparar INSERT
            placeholders = ','.join(['?' for _ in column_names])
            columns_str = ','.join([f'"{col}"' for col in column_names])
            insert_sql = f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})'

            # Inserir dados
            row_count = 0
            errors = 0
            for row in rows:
                try:
                    # Converter valores (especialmente datas)
                    converted_row = []
                    for value in row:
                        if isinstance(value, datetime):
                            converted_row.append(value.isoformat())
                        elif isinstance(value, Decimal):
                            # Converter Decimal para float
                            converted_row.append(float(value))
                        elif isinstance(value, bytes):
                            # Tentar decodificar bytes, se falhar, usar None
                            try:
                                converted_row.append(value.decode('utf-8', errors='replace'))
                            except:
                                converted_row.append(None)
                        else:
                            converted_row.append(value)

                    sqlite_cursor.execute(insert_sql, converted_row)
                    row_count += 1
                except Exception as row_error:
                    errors += 1
                    if errors <= 5:  # Mostrar apenas primeiros 5 erros
                        logger.warning(f"  ⚠ Erro em registro {row_count + errors}: {str(row_error)[:100]}")

            sqlite_conn.commit()
            if errors > 0:
                logger.warning(f"  ⚠ Copiados {row_count} registros para {table_name} ({errors} erros ignorados)")
            else:
                logger.info(f"  ✓ Copiados {row_count} registros para {table_name}")

        except Exception as e:
            logger.error(f"  ✗ Erro ao copiar dados de {table_name}: {e}")
            # Não propagar erro - continuar com próxima tabela

    def convert(self, tables_to_convert: List[str] = None) -> bool:
        """
        Executa a conversão completa

        Args:
            tables_to_convert: Lista de tabelas específicas (None = todas)

        Returns:
            bool: True se conversão bem-sucedida
        """
        try:
            # Conectar aos bancos
            access_conn = self.get_access_connection()
            sqlite_conn = self.get_sqlite_connection()

            # Listar tabelas
            all_tables = self.get_table_names(access_conn)

            # Filtrar tabelas se especificado
            if tables_to_convert:
                tables = [t for t in all_tables if t in tables_to_convert]
                logger.info(f"Convertendo {len(tables)} tabelas específicas")
            else:
                tables = all_tables
                logger.info(f"Convertendo TODAS as {len(tables)} tabelas")

            # Converter cada tabela
            success_count = 0
            error_count = 0

            for i, table_name in enumerate(tables, 1):
                try:
                    logger.info(f"\n[{i}/{len(tables)}] Processando: {table_name}")

                    # Obter schema
                    columns = self.get_table_schema(access_conn, table_name)

                    # Criar tabela no SQLite
                    self.create_sqlite_table(sqlite_conn, table_name, columns)

                    # Copiar dados
                    self.copy_table_data(access_conn, sqlite_conn, table_name)

                    success_count += 1

                except Exception as e:
                    error_count += 1
                    logger.error(f"  ✗ Falha ao processar tabela {table_name}: {e}")
                    logger.info("  → Continuando com próxima tabela...")

            # Fechar conexões
            access_conn.close()
            sqlite_conn.close()

            logger.info("\n" + "="*70)
            if error_count == 0:
                logger.info("✅ CONVERSÃO CONCLUÍDA COM SUCESSO!")
            else:
                logger.info("⚠️  CONVERSÃO CONCLUÍDA COM AVISOS")
            logger.info(f"   Arquivo SQLite: {self.sqlite_db_path}")
            logger.info(f"   Tamanho: {self.sqlite_db_path.stat().st_size / 1024 / 1024:.2f} MB")
            logger.info(f"   Tabelas convertidas: {success_count}/{len(tables)}")
            if error_count > 0:
                logger.info(f"   Tabelas com erros: {error_count}")
            logger.info("="*70)

            return True

        except Exception as e:
            logger.error(f"\n❌ ERRO NA CONVERSÃO: {e}")
            return False


def main():
    """Função principal do script"""
    # Configurar encoding UTF-8 para Windows
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("="*70)
    print("  CONVERSOR: Microsoft Access → SQLite")
    print("  Fundos Report ReactPy")
    print("="*70)
    print()

    # Configurações padrão
    DEFAULT_ACCESS_PATH = r"C:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\03. Arquivos Rotina\09. Base_de_Dados\Base Fundos_V2.accdb"
    DEFAULT_SQLITE_PATH = r"data\fundos_v2.db"

    # Verificar argumentos
    if len(sys.argv) > 1:
        access_path = sys.argv[1]
    else:
        access_path = DEFAULT_ACCESS_PATH

    if len(sys.argv) > 2:
        sqlite_path = sys.argv[2]
    else:
        sqlite_path = DEFAULT_SQLITE_PATH

    print(f"📂 Access:  {access_path}")
    print(f"💾 SQLite:  {sqlite_path}")
    print()

    # Confirmar
    response = input("Deseja continuar? (s/n): ")
    if response.lower() not in ['s', 'sim', 'y', 'yes']:
        print("❌ Operação cancelada.")
        return

    print()
    logger.info("Iniciando conversão...")

    # Executar conversão
    converter = AccessToSQLiteConverter(access_path, sqlite_path)

    # Tabelas principais do sistema (você pode customizar)
    # None = converter TODAS as tabelas
    # ['Tabela1', 'Tabela2'] = converter apenas específicas
    success = converter.convert(tables_to_convert=None)

    if success:
        print()
        print("🎉 Pronto! Você pode agora:")
        print("   1. Atualizar database_manager_v6.py para usar SQLite")
        print("   2. Testar consultas com o novo banco")
        print("   3. Fazer deploy para Railway com o arquivo .db")
    else:
        print()
        print("⚠️  A conversão encontrou erros. Verifique os logs acima.")
        sys.exit(1)


if __name__ == "__main__":
    main()
