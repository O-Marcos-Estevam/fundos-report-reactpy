"""
Gerenciador de Cache com TTL
Sistema de cache inteligente para otimização de performance
"""

import threading
import time
from typing import Any, Optional, Dict, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import wraps


@dataclass
class CacheEntry:
    """Entrada do cache com metadados"""
    value: Any
    timestamp: float
    ttl: float  # Time to live em segundos
    hits: int = 0

    def is_expired(self) -> bool:
        """Verifica se a entrada expirou"""
        return (time.time() - self.timestamp) > self.ttl

    def is_valid(self) -> bool:
        """Verifica se a entrada é válida"""
        return not self.is_expired()


class CacheManager:
    """
    Gerenciador de cache thread-safe com TTL

    Features:
    - TTL configurável por chave
    - Limpeza automática de entradas expiradas
    - Thread-safe
    - Estatísticas de uso (hits/misses)
    - Namespace support
    """

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

    def __init__(self, default_ttl: float = 300):
        """
        Inicializa o cache manager

        Args:
            default_ttl: TTL padrão em segundos (5 minutos)
        """
        if self._initialized:
            return

        self._cache: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
        self._initialized = True

    def get(self, key: str, default: Any = None) -> Optional[Any]:
        """
        Busca valor no cache

        Args:
            key: Chave do cache
            default: Valor padrão se não encontrado

        Returns:
            Valor armazenado ou default
        """
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]

                # Verificar se expirou
                if entry.is_expired():
                    del self._cache[key]
                    self._stats['evictions'] += 1
                    self._stats['misses'] += 1
                    return default

                # Cache hit
                entry.hits += 1
                self._stats['hits'] += 1
                return entry.value

            # Cache miss
            self._stats['misses'] += 1
            return default

    def set(self, key: str, value: Any, ttl: Optional[float] = None):
        """
        Armazena valor no cache

        Args:
            key: Chave do cache
            value: Valor a armazenar
            ttl: Time to live em segundos (usa default se None)
        """
        with self._lock:
            ttl = ttl if ttl is not None else self._default_ttl

            self._cache[key] = CacheEntry(
                value=value,
                timestamp=time.time(),
                ttl=ttl
            )

    def delete(self, key: str) -> bool:
        """
        Remove chave do cache

        Args:
            key: Chave a remover

        Returns:
            True se removeu, False se não existia
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self):
        """Limpa todo o cache"""
        with self._lock:
            self._cache.clear()
            self._stats['evictions'] += len(self._cache)

    def clear_expired(self):
        """Remove todas as entradas expiradas"""
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]

            for key in expired_keys:
                del self._cache[key]
                self._stats['evictions'] += 1

    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do cache

        Returns:
            Dicionário com estatísticas
        """
        with self._lock:
            total_requests = self._stats['hits'] + self._stats['misses']
            hit_rate = (self._stats['hits'] / total_requests * 100) if total_requests > 0 else 0

            return {
                'size': len(self._cache),
                'hits': self._stats['hits'],
                'misses': self._stats['misses'],
                'evictions': self._stats['evictions'],
                'hit_rate': round(hit_rate, 2),
                'total_requests': total_requests
            }

    def get_keys(self) -> list:
        """Retorna lista de chaves no cache"""
        with self._lock:
            return list(self._cache.keys())

    def has_key(self, key: str) -> bool:
        """Verifica se chave existe e é válida"""
        with self._lock:
            if key in self._cache:
                return self._cache[key].is_valid()
            return False

    def __repr__(self) -> str:
        stats = self.get_stats()
        return f"CacheManager(size={stats['size']}, hit_rate={stats['hit_rate']}%)"


# Instância global
_cache_manager = CacheManager()


def get_cache_manager() -> CacheManager:
    """Retorna instância global do CacheManager"""
    return _cache_manager


# ============================================================================
# DECORADOR PARA CACHE DE FUNÇÕES
# ============================================================================

def cached(ttl: float = 300, key_prefix: str = ""):
    """
    Decorador para cache automático de funções

    Args:
        ttl: Time to live em segundos
        key_prefix: Prefixo para a chave do cache

    Example:
        @cached(ttl=60, key_prefix="metrics")
        def calcular_metricas(fundos):
            # expensive calculation
            return result
    """
    def decorator(func: Callable) -> Callable:
        cache = get_cache_manager()

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Gerar chave baseada em argumentos
            key_parts = [key_prefix, func.__name__]

            # Adicionar args à chave (apenas valores hasheáveis)
            for arg in args:
                try:
                    key_parts.append(str(hash(arg)))
                except TypeError:
                    key_parts.append(str(id(arg)))

            # Adicionar kwargs à chave
            for k, v in sorted(kwargs.items()):
                try:
                    key_parts.append(f"{k}={hash(v)}")
                except TypeError:
                    key_parts.append(f"{k}={id(v)}")

            cache_key = ":".join(key_parts)

            # Tentar buscar do cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Executar função e armazenar resultado
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl)

            return result

        return wrapper
    return decorator


# ============================================================================
# CACHE ESPECIALIZADO PARA DASHBOARD
# ============================================================================

class DashboardCache:
    """Cache especializado para dados de dashboard"""

    def __init__(self):
        self.cache = get_cache_manager()
        self.namespace = "dashboard"

    def _make_key(self, key: str) -> str:
        """Cria chave com namespace"""
        return f"{self.namespace}:{key}"

    def get_metricas_agregadas(self, exec_timestamp: float) -> Optional[Dict]:
        """Busca métricas agregadas do cache"""
        key = self._make_key(f"metricas:{exec_timestamp}")
        return self.cache.get(key)

    def set_metricas_agregadas(self, exec_timestamp: float, metricas: Dict, ttl: float = 600):
        """Armazena métricas agregadas no cache"""
        key = self._make_key(f"metricas:{exec_timestamp}")
        self.cache.set(key, metricas, ttl=ttl)

    def get_fundos_por_tipo(self, exec_timestamp: float) -> Optional[Dict]:
        """Busca agrupamento por tipo do cache"""
        key = self._make_key(f"por_tipo:{exec_timestamp}")
        return self.cache.get(key)

    def set_fundos_por_tipo(self, exec_timestamp: float, fundos_por_tipo: Dict, ttl: float = 600):
        """Armazena agrupamento por tipo no cache"""
        key = self._make_key(f"por_tipo:{exec_timestamp}")
        self.cache.set(key, fundos_por_tipo, ttl=ttl)

    def get_top_fundos(self, exec_timestamp: float, criterio: str, n: int = 10) -> Optional[list]:
        """Busca top fundos do cache"""
        key = self._make_key(f"top:{criterio}:{n}:{exec_timestamp}")
        return self.cache.get(key)

    def set_top_fundos(self, exec_timestamp: float, criterio: str, fundos: list, n: int = 10, ttl: float = 600):
        """Armazena top fundos no cache"""
        key = self._make_key(f"top:{criterio}:{n}:{exec_timestamp}")
        self.cache.set(key, fundos, ttl=ttl)

    def invalidate_all(self):
        """Invalida todo o cache do dashboard"""
        keys = self.cache.get_keys()
        for key in keys:
            if key.startswith(self.namespace):
                self.cache.delete(key)

    def __repr__(self) -> str:
        return f"DashboardCache(namespace={self.namespace})"


# Instância global do dashboard cache
_dashboard_cache = DashboardCache()


def get_dashboard_cache() -> DashboardCache:
    """Retorna instância global do DashboardCache"""
    return _dashboard_cache
