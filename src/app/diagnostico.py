"""
Endpoint de diagnóstico para verificar configurações no Railway
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pathlib import Path
import os
import sys

router = APIRouter()

@router.get("/api/diagnostico")
async def diagnostico():
    """Retorna informações de diagnóstico do ambiente"""

    from app.config import (
        is_cloud_environment,
        is_windows,
        CAMINHO_MODULO,
        DB_PATH,
        AppConfig
    )

    # Verificar arquivo SQLite
    db_path = Path("data/fundos_v2.db")
    db_exists = db_path.exists()
    db_size = db_path.stat().st_size / 1024 / 1024 if db_exists else 0

    # Verificar módulos
    modulo_exists = Path(CAMINHO_MODULO).exists() if CAMINHO_MODULO else False

    info = {
        "ambiente": {
            "IS_CLOUD": is_cloud_environment(),
            "IS_WINDOWS": is_windows(),
            "RAILWAY_ENV": os.getenv("RAILWAY_ENVIRONMENT"),
            "platform": sys.platform,
        },
        "configuracao": {
            "USE_MOCK_DATA": AppConfig.USE_MOCK_DATA,
            "LOAD_SAMPLE_DATA": os.getenv("LOAD_SAMPLE_DATA"),
            "CAMINHO_MODULO": CAMINHO_MODULO,
            "modulo_exists": modulo_exists,
            "DB_PATH": str(DB_PATH) if DB_PATH else None,
        },
        "banco_dados": {
            "sqlite_path": str(db_path),
            "sqlite_exists": db_exists,
            "sqlite_size_mb": round(db_size, 2),
        },
        "variaveis_env": {
            "USE_MOCK_DATA": os.getenv("USE_MOCK_DATA"),
            "LOAD_SAMPLE_DATA": os.getenv("LOAD_SAMPLE_DATA"),
            "PORT": os.getenv("PORT"),
        }
    }

    # Se SQLite existe, testar queries
    if db_exists:
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Contar tabelas
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            num_tables = cursor.fetchone()[0]

            # Contar registros em Patrimonio_Totais
            cursor.execute("SELECT COUNT(*) FROM Patrimonio_Totais")
            num_registros = cursor.fetchone()[0]

            # Listar fundos
            cursor.execute("SELECT DISTINCT CARTEIRA FROM Patrimonio_Totais LIMIT 5")
            fundos = [row[0] for row in cursor.fetchall()]

            conn.close()

            info["banco_dados"]["teste_query"] = {
                "num_tabelas": num_tables,
                "num_registros_patrimonio": num_registros,
                "fundos_exemplo": fundos,
                "status": "OK - Dados REAIS encontrados!" if num_registros > 0 else "ERRO - Sem dados"
            }
        except Exception as e:
            info["banco_dados"]["teste_query"] = {
                "status": "ERRO",
                "erro": str(e)
            }

    return JSONResponse(content=info)
