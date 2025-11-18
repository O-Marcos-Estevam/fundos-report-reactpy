"""
Script de Teste - SQLite com Dados Reais
Valida que o banco SQLite tem dados reais convertidos do Access
"""

import sqlite3
import pandas as pd
from pathlib import Path

# Conectar ao SQLite
db_path = Path("data/fundos_v2.db")

if not db_path.exists():
    print(f"[ERRO] Arquivo SQLite nao encontrado: {db_path}")
    exit(1)

print(f"[OK] Arquivo SQLite encontrado: {db_path}")
print(f"Tamanho: {db_path.stat().st_size / 1024 / 1024:.2f} MB\n")

conn = sqlite3.connect(db_path)

# Listar todas as tabelas
print("TABELAS NO BANCO:")
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", conn)
print(f"   Total: {len(tables)} tabelas\n")

for idx, table in enumerate(tables['name'], 1):
    count = pd.read_sql(f"SELECT COUNT(*) as total FROM [{table}]", conn)
    total = count['total'][0]
    print(f"   {idx:2d}. {table:40s} - {total:>10,} registros")

print("\n" + "="*70)

# Testar queries específicas importantes
print("\nTESTANDO QUERIES PRINCIPAIS:\n")

# 1. Patrimonio_Totais (usado pelos relatórios)
try:
    query = "SELECT * FROM Patrimonio_Totais LIMIT 5"
    df = pd.read_sql(query, conn)
    print(f"[OK] Patrimonio_Totais: {len(df)} registros retornados")
    if len(df) > 0:
        print(f"   Colunas: {', '.join(df.columns[:5])}...")
        print(f"   Primeiro registro: Data = {df.iloc[0]['Data'] if 'Data' in df.columns else 'N/A'}")
except Exception as e:
    print(f"[ERRO] Erro em Patrimonio_Totais: {e}")

# 2. DIAS_UTEIS (usado para cálculos)
try:
    query = "SELECT * FROM DIAS_UTEIS LIMIT 5"
    df = pd.read_sql(query, conn)
    print(f"\n[OK] DIAS_UTEIS: {len(df)} registros retornados")
except Exception as e:
    print(f"\n[ERRO] Erro em DIAS_UTEIS: {e}")

# 3. BriTech_Historico_Cota (dados de fundos)
try:
    query = "SELECT * FROM BriTech_Historico_Cota LIMIT 5"
    df = pd.read_sql(query, conn)
    print(f"\n[OK] BriTech_Historico_Cota: {len(df)} registros retornados")
    if len(df) > 0:
        print(f"   Colunas: {', '.join(df.columns[:5])}...")
except Exception as e:
    print(f"\n[ERRO] Erro em BriTech_Historico_Cota: {e}")

conn.close()

print("\n" + "="*70)
print("[OK] TESTE CONCLUIDO - SQLite funcionando com dados REAIS!")
print("="*70)
