"""
Script para verificar e baixar banco SQLite se necessario
"""
import os
import sqlite3
from pathlib import Path

def check_database():
    """Verifica se o banco SQLite esta OK"""
    db_path = Path("data/fundos_v2.db")

    print(f"[1] Verificando banco de dados: {db_path}")

    if not db_path.exists():
        print(f"[ERRO] Arquivo nao existe: {db_path}")
        return False

    file_size = db_path.stat().st_size
    print(f"[2] Tamanho do arquivo: {file_size / 1024 / 1024:.2f} MB")

    # Se arquivo for muito pequeno (< 1 MB), provavelmente é um pointer do Git LFS
    if file_size < 1_000_000:  # < 1 MB
        print(f"[AVISO] Arquivo muito pequeno ({file_size} bytes)")
        print(f"[AVISO] Provavelmente e um pointer do Git LFS, nao o banco real")

        # Tentar ler primeiras linhas
        with open(db_path, 'r') as f:
            first_lines = f.read(200)
            if 'version https://git-lfs.github.com' in first_lines:
                print("[ERRO] Confirmado: arquivo e um pointer Git LFS")
                print("[INFO] Git LFS nao baixou o arquivo no Railway")
                print("[INFO] Solucao: use Railway Volumes ou faça upload direto")
                return False

    # Tentar conectar
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar tabelas
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        num_tables = cursor.fetchone()[0]

        print(f"[3] Numero de tabelas: {num_tables}")

        if num_tables == 0:
            print("[ERRO] Banco vazio (0 tabelas)")
            conn.close()
            return False

        # Verificar registros
        cursor.execute("SELECT COUNT(*) FROM Patrimonio_Totais")
        num_records = cursor.fetchone()[0]

        print(f"[4] Registros em Patrimonio_Totais: {num_records:,}")

        conn.close()

        if num_records > 0:
            print("[OK] Banco de dados funcionando com dados REAIS!")
            return True
        else:
            print("[ERRO] Tabela Patrimonio_Totais vazia")
            return False

    except Exception as e:
        print(f"[ERRO] Erro ao acessar banco: {e}")
        return False

if __name__ == "__main__":
    is_ok = check_database()
    exit(0 if is_ok else 1)
