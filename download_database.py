"""
Script para baixar banco SQLite de uma URL externa
"""
import os
import sys
import urllib.request
from pathlib import Path

# URL do banco SQLite (você vai precisar hospedar em algum lugar)
# Opções: GitHub Releases, Dropbox, Google Drive, AWS S3, etc.
DATABASE_URL = os.getenv("DATABASE_URL", "")

def download_database():
    """Baixa banco SQLite de uma URL"""

    if not DATABASE_URL:
        print("[AVISO] DATABASE_URL não configurada")
        print("[INFO] Configure a variável de ambiente DATABASE_URL no Railway")
        print("[INFO] Exemplo: https://github.com/user/repo/releases/download/v1.0/fundos_v2.db")
        return False

    db_path = Path("data/fundos_v2.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[1] Baixando banco de dados de: {DATABASE_URL}")
    print(f"[2] Destino: {db_path}")

    try:
        # Baixar com progress
        def reporthook(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\r[DOWNLOAD] {percent}% ({count * block_size / 1024 / 1024:.1f} MB)")
            sys.stdout.flush()

        urllib.request.urlretrieve(DATABASE_URL, db_path, reporthook)
        print()  # Nova linha após progress

        file_size = db_path.stat().st_size
        print(f"[3] Download concluído: {file_size / 1024 / 1024:.2f} MB")

        # Verificar se é um banco válido
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        num_tables = cursor.fetchone()[0]
        conn.close()

        print(f"[4] Banco válido com {num_tables} tabelas")
        return True

    except Exception as e:
        print(f"[ERRO] Falha ao baixar banco: {e}")
        return False

if __name__ == "__main__":
    success = download_database()

    if not success:
        print("\n" + "="*70)
        print("INSTRUÇÕES PARA CONFIGURAR DOWNLOAD DO BANCO:")
        print("="*70)
        print()
        print("1. Hospede o arquivo fundos_v2.db (408 MB) em um dos serviços:")
        print("   - GitHub Releases (gratuito, público)")
        print("   - Dropbox (gerar link direto)")
        print("   - Google Drive (gerar link direto)")
        print("   - AWS S3 / DigitalOcean Spaces")
        print()
        print("2. No Railway Dashboard, adicione variável de ambiente:")
        print("   DATABASE_URL = https://sua-url-aqui/fundos_v2.db")
        print()
        print("3. Faça redeploy")
        print()
        print("="*70)

    exit(0 if success else 1)
