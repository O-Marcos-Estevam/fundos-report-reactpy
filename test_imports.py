"""
Script de teste para verificar imports e funcionalidades básicas
"""
import sys
from pathlib import Path

# Adicionar diretório src ao path
ROOT_DIR = Path(__file__).resolve().parent / "src"
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

print("=" * 70)
print("TESTE DE IMPORTS E FUNCIONALIDADES")
print("=" * 70)
print()

# Teste 1: Config
try:
    from app.config import AppConfig
    print(f"[OK] Config - Versao: {AppConfig.APP_VERSION}")
except Exception as e:
    print(f"[ERRO] Config: {e}")
    sys.exit(1)

# Teste 2: StateManager
try:
    from services.state_manager import get_state_manager
    sm = get_state_manager()
    print(f"[OK] StateManager - Pagina: {sm.pagina_atual}, Versao: {sm.versao_modulo}")
except Exception as e:
    print(f"[ERRO] StateManager: {e}")
    sys.exit(1)

# Teste 3: Componentes Layout
try:
    from components.layout import header, navegacao
    print("[OK] Componentes layout")
except Exception as e:
    print(f"[ERRO] Componentes layout: {e}")
    sys.exit(1)

# Teste 4: Página Executar
try:
    from pages.executar_modern import pagina_executar_moderna
    print("[OK] Pagina executar")
except Exception as e:
    print(f"[ERRO] Pagina executar: {e}")
    sys.exit(1)

# Teste 5: Página Dashboard
try:
    from pages.dashboard_modern import pagina_dashboard_moderna
    print("[OK] Pagina dashboard")
except Exception as e:
    print(f"[ERRO] Pagina dashboard: {e}")
    sys.exit(1)

# Teste 6: Página Lâmina
try:
    from pages.lamina_fundos_modern import pagina_lamina_fundos_moderna
    print("[OK] Pagina lamina")
except Exception as e:
    print(f"[ERRO] Pagina lamina: {e}")
    sys.exit(1)

# Teste 7: Página Histórico
try:
    from pages.historico_modern import pagina_historico_moderna
    print("[OK] Pagina historico")
except Exception as e:
    print(f"[ERRO] Pagina historico: {e}")
    sys.exit(1)

# Teste 8: App Root
try:
    from app.main import app_root, app
    print("[OK] App main")
except Exception as e:
    print(f"[ERRO] App main: {e}")
    sys.exit(1)

print()
print("=" * 70)
print("[OK] TODOS OS TESTES PASSARAM!")
print("=" * 70)
print()
print("A aplicação está pronta para executar.")
print("Execute: python src/app/main.py")

