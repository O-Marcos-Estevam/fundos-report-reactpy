"""
Teste simples para verificar se o SQLite esta acessivel no Railway
"""
import sqlite3
from pathlib import Path

db_path = Path("data/fundos_v2.db")

print(f"[1] Verificando arquivo SQLite: {db_path}")
print(f"[2] Arquivo existe? {db_path.exists()}")

if db_path.exists():
    print(f"[3] Tamanho do arquivo: {db_path.stat().st_size / 1024 / 1024:.2f} MB")

    # Conectar e testar
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Listar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"[4] Numero de tabelas: {len(tables)}")

    # Testar query em Patrimonio_Totais
    cursor.execute("SELECT COUNT(*) FROM Patrimonio_Totais")
    count = cursor.fetchone()[0]
    print(f"[5] Registros em Patrimonio_Totais: {count:,}")

    # Listar alguns fundos
    cursor.execute("SELECT DISTINCT CARTEIRA FROM Patrimonio_Totais LIMIT 10")
    fundos = cursor.fetchall()
    print(f"[6] Primeiros fundos encontrados:")
    for fundo in fundos:
        print(f"    - {fundo[0]}")

    conn.close()
    print("[OK] SQLite funcionando com DADOS REAIS!")
else:
    print("[ERRO] Arquivo SQLite nao encontrado!")
    print("      Git LFS pode nao ter baixado o arquivo corretamente")
