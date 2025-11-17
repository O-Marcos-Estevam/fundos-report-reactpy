"""
Gerenciador de Preferências do Usuário
Salva layouts, configurações e personalizações
"""

import json
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class PreferencesManager:
    """
    Gerenciador singleton de preferências do usuário

    Funcionalidades:
    - Salvar/carregar layouts de dashboard
    - Preferências de widgets
    - Configurações de visualização
    - Persistência em arquivo JSON
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._preferences_file = Path(__file__).parent.parent.parent / "data" / "user_preferences.json"
            self._preferences: Dict[str, Any] = {}
            self._load_preferences()

    def _ensure_data_dir(self):
        """Garante que o diretório de dados existe"""
        self._preferences_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_preferences(self):
        """Carrega preferências do arquivo"""
        try:
            if self._preferences_file.exists():
                with open(self._preferences_file, 'r', encoding='utf-8') as f:
                    self._preferences = json.load(f)
                print(f"[INFO] Preferências carregadas de {self._preferences_file}")
            else:
                self._preferences = self._get_default_preferences()
                self._save_preferences()
        except Exception as e:
            print(f"[WARNING] Erro ao carregar preferências: {e}")
            self._preferences = self._get_default_preferences()

    def _save_preferences(self):
        """Salva preferências no arquivo"""
        try:
            self._ensure_data_dir()
            with open(self._preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self._preferences, f, indent=2, ensure_ascii=False)
            print(f"[INFO] Preferências salvas em {self._preferences_file}")
        except Exception as e:
            print(f"[ERROR] Erro ao salvar preferências: {e}")

    def _get_default_preferences(self) -> Dict[str, Any]:
        """Retorna preferências padrão"""
        return {
            "version": "1.0",
            "last_updated": datetime.now().isoformat(),
            "dashboard": {
                "layout": "default",  # default, compact, detailed
                "widgets": [
                    {"id": "resumo", "type": "resumo_executivo", "enabled": True, "position": 0},
                    {"id": "alertas", "type": "alertas", "enabled": True, "position": 1},
                    {"id": "top_pl", "type": "top_fundos", "enabled": True, "position": 2, "config": {"criterio": "pl"}},
                    {"id": "dist_tipo", "type": "grafico_pizza", "enabled": True, "position": 3},
                    {"id": "health", "type": "health_score", "enabled": True, "position": 4},
                ],
                "grid_columns": 3,  # Número de colunas no grid
                "auto_refresh": False,
                "refresh_interval": 300  # segundos
            },
            "visualization": {
                "theme": "light",  # light, dark
                "chart_palette": "default",  # default, vibrant, monochrome
                "show_animations": True,
                "compact_mode": False
            },
            "filters": {
                "remember_last": True,
                "last_filters": {
                    "tipos": [],
                    "var_range": [-20.0, 20.0],
                    "pl_range": [0.0, 100_000_000_000.0],
                    "apenas_alertas": False
                }
            },
            "export": {
                "default_format": "xlsx",  # xlsx, csv
                "include_advanced_metrics": True,
                "include_alerts": True
            }
        }

    # ========================================================================
    # DASHBOARD LAYOUT
    # ========================================================================

    def get_dashboard_layout(self) -> str:
        """Retorna o layout atual do dashboard"""
        return self._preferences.get("dashboard", {}).get("layout", "default")

    def set_dashboard_layout(self, layout: str):
        """Define o layout do dashboard"""
        if "dashboard" not in self._preferences:
            self._preferences["dashboard"] = {}
        self._preferences["dashboard"]["layout"] = layout
        self._save_preferences()

    def get_dashboard_widgets(self) -> List[Dict[str, Any]]:
        """Retorna lista de widgets configurados"""
        widgets = self._preferences.get("dashboard", {}).get("widgets", [])
        # Ordenar por posição
        return sorted(widgets, key=lambda w: w.get("position", 999))

    def update_widget_config(self, widget_id: str, config: Dict[str, Any]):
        """Atualiza configuração de um widget"""
        if "dashboard" not in self._preferences:
            self._preferences["dashboard"] = {}

        widgets = self._preferences["dashboard"].get("widgets", [])

        # Encontrar e atualizar widget
        for widget in widgets:
            if widget.get("id") == widget_id:
                widget.update(config)
                break
        else:
            # Widget não encontrado, adicionar
            widgets.append({"id": widget_id, **config})

        self._preferences["dashboard"]["widgets"] = widgets
        self._save_preferences()

    def toggle_widget(self, widget_id: str, enabled: bool):
        """Ativa/desativa um widget"""
        widgets = self._preferences.get("dashboard", {}).get("widgets", [])

        for widget in widgets:
            if widget.get("id") == widget_id:
                widget["enabled"] = enabled
                break

        self._preferences["dashboard"]["widgets"] = widgets
        self._save_preferences()

    def reorder_widgets(self, widget_order: List[str]):
        """Reordena widgets baseado em lista de IDs"""
        widgets = self._preferences.get("dashboard", {}).get("widgets", [])

        # Criar mapa de widgets
        widget_map = {w["id"]: w for w in widgets}

        # Reordenar
        new_widgets = []
        for idx, widget_id in enumerate(widget_order):
            if widget_id in widget_map:
                widget = widget_map[widget_id]
                widget["position"] = idx
                new_widgets.append(widget)

        self._preferences["dashboard"]["widgets"] = new_widgets
        self._save_preferences()

    def get_grid_columns(self) -> int:
        """Retorna número de colunas do grid"""
        return self._preferences.get("dashboard", {}).get("grid_columns", 3)

    def set_grid_columns(self, columns: int):
        """Define número de colunas do grid"""
        if "dashboard" not in self._preferences:
            self._preferences["dashboard"] = {}
        self._preferences["dashboard"]["grid_columns"] = max(1, min(columns, 4))
        self._save_preferences()

    # ========================================================================
    # VISUALIZAÇÃO
    # ========================================================================

    def get_theme(self) -> str:
        """Retorna tema atual"""
        return self._preferences.get("visualization", {}).get("theme", "light")

    def set_theme(self, theme: str):
        """Define tema"""
        if "visualization" not in self._preferences:
            self._preferences["visualization"] = {}
        self._preferences["visualization"]["theme"] = theme
        self._save_preferences()

    def get_chart_palette(self) -> str:
        """Retorna paleta de cores dos gráficos"""
        return self._preferences.get("visualization", {}).get("chart_palette", "default")

    def set_chart_palette(self, palette: str):
        """Define paleta de cores"""
        if "visualization" not in self._preferences:
            self._preferences["visualization"] = {}
        self._preferences["visualization"]["chart_palette"] = palette
        self._save_preferences()

    def is_compact_mode(self) -> bool:
        """Verifica se modo compacto está ativo"""
        return self._preferences.get("visualization", {}).get("compact_mode", False)

    def toggle_compact_mode(self):
        """Alterna modo compacto"""
        if "visualization" not in self._preferences:
            self._preferences["visualization"] = {}
        current = self._preferences["visualization"].get("compact_mode", False)
        self._preferences["visualization"]["compact_mode"] = not current
        self._save_preferences()

    # ========================================================================
    # FILTROS
    # ========================================================================

    def should_remember_filters(self) -> bool:
        """Verifica se deve lembrar últimos filtros"""
        return self._preferences.get("filters", {}).get("remember_last", True)

    def get_last_filters(self) -> Dict[str, Any]:
        """Retorna últimos filtros utilizados"""
        return self._preferences.get("filters", {}).get("last_filters", {})

    def save_last_filters(self, filters: Dict[str, Any]):
        """Salva filtros utilizados"""
        if not self.should_remember_filters():
            return

        if "filters" not in self._preferences:
            self._preferences["filters"] = {}
        self._preferences["filters"]["last_filters"] = filters
        self._save_preferences()

    # ========================================================================
    # EXPORTAÇÃO
    # ========================================================================

    def get_export_preferences(self) -> Dict[str, Any]:
        """Retorna preferências de exportação"""
        return self._preferences.get("export", {
            "default_format": "xlsx",
            "include_advanced_metrics": True,
            "include_alerts": True
        })

    def update_export_preferences(self, preferences: Dict[str, Any]):
        """Atualiza preferências de exportação"""
        if "export" not in self._preferences:
            self._preferences["export"] = {}
        self._preferences["export"].update(preferences)
        self._save_preferences()

    # ========================================================================
    # UTILITÁRIOS
    # ========================================================================

    def reset_to_defaults(self):
        """Reseta para preferências padrão"""
        self._preferences = self._get_default_preferences()
        self._save_preferences()

    def export_preferences(self) -> str:
        """Exporta preferências como JSON string"""
        return json.dumps(self._preferences, indent=2, ensure_ascii=False)

    def import_preferences(self, json_str: str):
        """Importa preferências de JSON string"""
        try:
            new_prefs = json.loads(json_str)
            self._preferences = new_prefs
            self._save_preferences()
            return True
        except Exception as e:
            print(f"[ERROR] Erro ao importar preferências: {e}")
            return False


# ============================================================================
# INSTÂNCIA GLOBAL
# ============================================================================

_preferences_manager = PreferencesManager()


def get_preferences_manager() -> PreferencesManager:
    """Retorna instância global do PreferencesManager"""
    return _preferences_manager
