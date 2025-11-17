"""
Gerenciador de Estado da Aplicação
Centraliza e gerencia o estado reativo da aplicação
"""

import threading
from typing import Optional, Dict, Any, List
from datetime import datetime

from models.execucao import ExecucaoInfo
from models.historico import HistoricoEntry
from app.config import get_default_state


class StateManager:
    """Gerenciador centralizado de estado thread-safe"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Implementa Singleton"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Inicializa o estado"""
        if self._initialized:
            return

        self._state = get_default_state()
        self._callbacks = []
        self._initialized = True

    # ========================================================================
    # GETTERS
    # ========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Retorna cópia do estado completo"""
        with self._lock:
            return self._state.copy()

    def get(self, key: str, default: Any = None) -> Any:
        """Retorna valor de uma chave do estado"""
        with self._lock:
            return self._state.get(key, default)

    @property
    def pagina_atual(self) -> str:
        """Página atual"""
        return self.get('pagina_atual', 'executar')

    @property
    def versao_modulo(self) -> str:
        """Versão do módulo selecionada"""
        return self.get('versao_modulo', 'V6')

    @property
    def modo_escuro(self) -> bool:
        """Modo escuro ativo"""
        return self.get('modo_escuro', False)

    @property
    def historico(self) -> List[HistoricoEntry]:
        """Histórico de execuções"""
        return self.get('historico', [])

    @property
    def ultima_execucao(self) -> Optional[ExecucaoInfo]:
        """Última execução realizada"""
        return self.get('ultima_execucao')

    @property
    def logs_execucao(self) -> List[str]:
        """Logs da execução atual"""
        return self.get('logs_execucao', [])

    @property
    def config_avancada(self) -> Dict[str, Any]:
        """Configurações avançadas"""
        return self.get('config_avancada', {})

    # ========================================================================
    # SETTERS
    # ========================================================================

    def set(self, key: str, value: Any):
        """Define valor de uma chave"""
        with self._lock:
            self._state[key] = value
            self._notify_callbacks(key, value)

    def update(self, updates: Dict[str, Any]):
        """Atualiza múltiplas chaves"""
        with self._lock:
            self._state.update(updates)
            for key, value in updates.items():
                self._notify_callbacks(key, value)

    def set_pagina(self, pagina: str):
        """Define página atual"""
        self.set('pagina_atual', pagina)

    def set_versao_modulo(self, versao: str):
        """Define versão do módulo"""
        self.set('versao_modulo', versao)

    def toggle_modo_escuro(self):
        """Alterna modo escuro"""
        self.set('modo_escuro', not self.modo_escuro)

    def set_ultima_execucao(self, execucao: Optional[ExecucaoInfo]):
        """Define última execução"""
        self.set('ultima_execucao', execucao)

    def set_historico(self, historico: List[HistoricoEntry]):
        """Define histórico completo"""
        self.set('historico', historico)

    def add_log(self, mensagem: str):
        """Adiciona linha ao log"""
        with self._lock:
            logs = self._state.get('logs_execucao', [])
            timestamp = datetime.now().strftime('%H:%M:%S')
            logs.append(f"[{timestamp}] {mensagem}")
            self._state['logs_execucao'] = logs
            self._notify_callbacks('logs_execucao', logs)

    def clear_logs(self):
        """Limpa logs de execução"""
        self.set('logs_execucao', [])

    def update_config(self, key: str, value: Any):
        """Atualiza configuração avançada"""
        with self._lock:
            config = self._state.get('config_avancada', {})
            config[key] = value
            self._state['config_avancada'] = config
            self._notify_callbacks('config_avancada', config)

    # ========================================================================
    # CALLBACKS E NOTIFICAÇÕES
    # ========================================================================

    def subscribe(self, callback):
        """
        Inscreve callback para notificações de mudança

        Args:
            callback: função(key, value) chamada quando estado muda
        """
        with self._lock:
            if callback not in self._callbacks:
                self._callbacks.append(callback)

    def unsubscribe(self, callback):
        """Remove callback das notificações"""
        with self._lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)

    def _notify_callbacks(self, key: str, value: Any):
        """Notifica todos os callbacks (deve ser chamado dentro de lock)"""
        for callback in self._callbacks:
            try:
                callback(key, value)
            except Exception:
                pass  # Ignora erros em callbacks

    # ========================================================================
    # UTILIDADES
    # ========================================================================

    def reset(self):
        """Reseta estado para valores padrão"""
        with self._lock:
            self._state = get_default_state()
            self._notify_callbacks('reset', None)

    def clear_execucao(self):
        """Limpa dados da última execução"""
        with self._lock:
            self._state['ultima_execucao'] = None
            self._state['logs_execucao'] = []

    def get_estatisticas_rapidas(self) -> Dict[str, Any]:
        """Retorna estatísticas rápidas do estado"""
        historico = self.historico
        ultima_exec = self.ultima_execucao

        total_exec = len(historico)
        sucessos = sum(1 for e in historico if e.sucesso)

        result = {
            'total_execucoes': total_exec,
            'taxa_sucesso': (sucessos / total_exec * 100) if total_exec > 0 else 0,
            'tem_execucao': ultima_exec is not None,
        }

        if ultima_exec:
            result.update({
                'fundos_processados': ultima_exec.fundos_processados,
                'tempo_ultima': ultima_exec.tempo_execucao,
                'data_ultima': ultima_exec.data_relatorio
            })

        return result

    def __repr__(self) -> str:
        return f"StateManager(pagina={self.pagina_atual}, versao={self.versao_modulo})"


# Instância global
_state_manager = StateManager()


def get_state_manager() -> StateManager:
    """Retorna instância global do StateManager"""
    return _state_manager
