"""
Testes unitários para StateManager
"""

import pytest
from src.services.state_manager import StateManager, get_state_manager


def test_state_manager_singleton():
    """Testa que StateManager é singleton"""
    manager1 = get_state_manager()
    manager2 = get_state_manager()

    assert manager1 is manager2


def test_state_manager_set_get_pagina():
    """Testa set e get página"""
    manager = get_state_manager()

    manager.set_pagina("dashboard")
    assert manager.pagina_atual == "dashboard"

    manager.set_pagina("executar")
    assert manager.pagina_atual == "executar"


def test_state_manager_update_config():
    """Testa atualização de configuração"""
    manager = get_state_manager()

    manager.update_config("auto_refresh", True)
    assert manager.config_avancada.get("auto_refresh") is True

    manager.update_config("auto_refresh", False)
    assert manager.config_avancada.get("auto_refresh") is False
