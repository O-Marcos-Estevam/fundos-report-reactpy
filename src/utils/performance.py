"""
Utilitários de Performance
Funções otimizadas e memoizadas para cálculos pesados
"""

from functools import lru_cache, wraps
from typing import List, Dict, Tuple, Any
import time
import logging

from models.fundo import FundoData
from services.cache_manager import cached, get_cache_manager


logger = logging.getLogger(__name__)


# ============================================================================
# DECORADORES DE PERFORMANCE
# ============================================================================

def timed(func):
    """Decorador para medir tempo de execução"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000  # em ms
        logger.debug(f"{func.__name__} executado em {elapsed:.2f}ms")
        return result
    return wrapper


def memoize_by_exec_time(func):
    """Memoiza baseado no timestamp da execução"""
    cache = {}

    @wraps(func)
    def wrapper(exec_timestamp: float, *args, **kwargs):
        key = (exec_timestamp, args, tuple(sorted(kwargs.items())))

        if key in cache:
            return cache[key]

        result = func(exec_timestamp, *args, **kwargs)
        cache[key] = result

        # Limpar cache antigo (manter apenas últimas 10 execuções)
        if len(cache) > 10:
            oldest_key = min(cache.keys(), key=lambda k: k[0])
            del cache[oldest_key]

        return result

    return wrapper


# ============================================================================
# FUNÇÕES DE AGREGAÇÃO OTIMIZADAS
# ============================================================================

@cached(ttl=600, key_prefix="metrics")
def calcular_metricas_agregadas_cached(fundos_hash: int, fundos: Tuple[FundoData, ...]) -> Dict[str, Any]:
    """
    Calcula métricas agregadas com cache

    Args:
        fundos_hash: Hash dos fundos para invalidação de cache
        fundos: Tuple de FundoData

    Returns:
        Dicionário com métricas agregadas
    """
    return _calcular_metricas_internas(fundos)


@timed
def _calcular_metricas_internas(fundos: Tuple[FundoData, ...]) -> Dict[str, Any]:
    """Cálculo interno de métricas (sem cache)"""

    if not fundos:
        return {}

    fundos_list = list(fundos)
    total_fundos = len(fundos_list)

    # Métricas básicas
    total_pl = sum(f.pl for f in fundos_list)
    total_caixa = sum(f.caixa_total for f in fundos_list)
    perc_caixa_pl = (total_caixa / total_pl * 100) if total_pl > 0 else 0

    # Variações médias
    var_d1_media = sum(f.variacao_d1 for f in fundos_list) / total_fundos if total_fundos > 0 else 0
    var_d7_media = sum(f.variacao_d7 for f in fundos_list) / total_fundos if total_fundos > 0 else 0
    var_d30_media = sum(f.variacao_d30 for f in fundos_list) / total_fundos if total_fundos > 0 else 0

    # PLs históricos
    total_pl_d1 = sum(f.pl_d1 for f in fundos_list if f.pl_d1 > 0) or total_pl * 0.98
    total_pl_d7 = sum(f.pl_d7 for f in fundos_list if f.pl_d7 > 0) or total_pl * 0.96
    total_pl_d30 = sum(f.pl_d30 for f in fundos_list if f.pl_d30 > 0) or total_pl * 0.92

    # Estatísticas avançadas
    fundos_com_alertas = sum(1 for f in fundos_list if f.tem_alertas())
    caixa_medio = total_caixa / total_fundos if total_fundos > 0 else 0
    pl_medio = total_pl / total_fundos if total_fundos > 0 else 0

    # Extremos
    fundo_maior_pl = max(fundos_list, key=lambda f: f.pl, default=None)
    fundo_maior_caixa = max(fundos_list, key=lambda f: f.caixa_total, default=None)
    fundo_melhor_var = max(fundos_list, key=lambda f: f.variacao_d1, default=None)
    fundo_pior_var = min(fundos_list, key=lambda f: f.variacao_d1, default=None)

    return {
        # Totais
        'total_pl': total_pl,
        'total_caixa': total_caixa,
        'total_fundos': total_fundos,
        'perc_caixa_pl': perc_caixa_pl,

        # Variações
        'var_d1_media': var_d1_media,
        'var_d7_media': var_d7_media,
        'var_d30_media': var_d30_media,

        # Histórico
        'total_pl_d1': total_pl_d1,
        'total_pl_d7': total_pl_d7,
        'total_pl_d30': total_pl_d30,

        # Médias
        'caixa_medio': caixa_medio,
        'pl_medio': pl_medio,

        # Alertas
        'fundos_com_alertas': fundos_com_alertas,
        'perc_fundos_alertas': (fundos_com_alertas / total_fundos * 100) if total_fundos > 0 else 0,

        # Extremos
        'fundo_maior_pl': fundo_maior_pl.nome if fundo_maior_pl else None,
        'valor_maior_pl': fundo_maior_pl.pl if fundo_maior_pl else 0,
        'fundo_maior_caixa': fundo_maior_caixa.nome if fundo_maior_caixa else None,
        'valor_maior_caixa': fundo_maior_caixa.caixa_total if fundo_maior_caixa else 0,
        'fundo_melhor_var': fundo_melhor_var.nome if fundo_melhor_var else None,
        'melhor_var_d1': fundo_melhor_var.variacao_d1 if fundo_melhor_var else 0,
        'fundo_pior_var': fundo_pior_var.nome if fundo_pior_var else None,
        'pior_var_d1': fundo_pior_var.variacao_d1 if fundo_pior_var else 0,
    }


@cached(ttl=600, key_prefix="group")
def agrupar_fundos_por_tipo_cached(fundos_hash: int, fundos: Tuple[FundoData, ...]) -> Dict[str, List[FundoData]]:
    """Agrupa fundos por tipo com cache"""
    fundos_list = list(fundos)
    fundos_por_tipo: Dict[str, List[FundoData]] = {}

    for fundo in fundos_list:
        tipo = fundo.tipo or "Outros"
        if tipo not in fundos_por_tipo:
            fundos_por_tipo[tipo] = []
        fundos_por_tipo[tipo].append(fundo)

    return fundos_por_tipo


@timed
def calcular_top_fundos(fundos: List[FundoData], criterio: str = "pl", n: int = 10, reverse: bool = True) -> List[FundoData]:
    """
    Calcula top N fundos por critério

    Args:
        fundos: Lista de fundos
        criterio: Atributo para ordenação (pl, caixa_total, variacao_d1, etc.)
        n: Número de fundos a retornar
        reverse: Se True, ordem decrescente

    Returns:
        Lista de top N fundos
    """
    if not fundos:
        return []

    # Mapear critério para atributo
    criterio_map = {
        'pl': lambda f: f.pl,
        'caixa': lambda f: f.caixa_total,
        'caixa_total': lambda f: f.caixa_total,
        'var_d1': lambda f: f.variacao_d1,
        'var_d7': lambda f: f.variacao_d7,
        'var_d30': lambda f: f.variacao_d30,
        'perc_caixa_pl': lambda f: f.perc_caixa_pl,
    }

    key_func = criterio_map.get(criterio, lambda f: getattr(f, criterio, 0))

    return sorted(fundos, key=key_func, reverse=reverse)[:n]


# ============================================================================
# FUNÇÕES DE FILTRAGEM OTIMIZADAS
# ============================================================================

def filtrar_fundos(
    fundos: List[FundoData],
    tipos: List[str] = None,
    var_min: float = None,
    var_max: float = None,
    pl_min: float = None,
    pl_max: float = None,
    com_alertas: bool = None,
    busca: str = None
) -> List[FundoData]:
    """
    Filtra fundos por múltiplos critérios de forma eficiente

    Args:
        fundos: Lista de fundos
        tipos: Lista de tipos permitidos
        var_min: Variação D-1 mínima
        var_max: Variação D-1 máxima
        pl_min: PL mínimo
        pl_max: PL máximo
        com_alertas: Filtrar por fundos com alertas
        busca: Texto para buscar no nome

    Returns:
        Lista de fundos filtrados
    """
    resultado = fundos

    # Filtro por tipo
    if tipos:
        resultado = [f for f in resultado if f.tipo in tipos]

    # Filtro por variação
    if var_min is not None:
        resultado = [f for f in resultado if f.variacao_d1 >= var_min]
    if var_max is not None:
        resultado = [f for f in resultado if f.variacao_d1 <= var_max]

    # Filtro por PL
    if pl_min is not None:
        resultado = [f for f in resultado if f.pl >= pl_min]
    if pl_max is not None:
        resultado = [f for f in resultado if f.pl <= pl_max]

    # Filtro por alertas
    if com_alertas is not None:
        resultado = [f for f in resultado if f.tem_alertas() == com_alertas]

    # Filtro por busca
    if busca:
        busca_lower = busca.lower()
        resultado = [f for f in resultado if busca_lower in f.nome.lower()]

    return resultado


# ============================================================================
# FUNÇÕES DE ANÁLISE ESTATÍSTICA
# ============================================================================

@timed
def calcular_estatisticas_tipo(fundos_por_tipo: Dict[str, List[FundoData]]) -> Dict[str, Dict]:
    """
    Calcula estatísticas por tipo de fundo

    Returns:
        Dict[tipo, {quantidade, pl_total, pl_medio, pl_max, pl_min, var_media}]
    """
    stats = {}

    for tipo, fundos in fundos_por_tipo.items():
        if not fundos:
            continue

        pls = [f.pl for f in fundos]
        vars_d1 = [f.variacao_d1 for f in fundos]

        stats[tipo] = {
            'quantidade': len(fundos),
            'pl_total': sum(pls),
            'pl_medio': sum(pls) / len(pls),
            'pl_max': max(pls),
            'pl_min': min(pls),
            'var_d1_media': sum(vars_d1) / len(vars_d1),
            'var_d1_max': max(vars_d1),
            'var_d1_min': min(vars_d1),
            'fundos_com_alertas': sum(1 for f in fundos if f.tem_alertas()),
        }

    return stats


def calcular_percentis(valores: List[float], percentis: List[int] = [25, 50, 75, 90, 95]) -> Dict[int, float]:
    """
    Calcula percentis de uma lista de valores

    Args:
        valores: Lista de valores numéricos
        percentis: Lista de percentis a calcular (0-100)

    Returns:
        Dict[percentil, valor]
    """
    if not valores:
        return {p: 0.0 for p in percentis}

    valores_sorted = sorted(valores)
    n = len(valores_sorted)

    result = {}
    for p in percentis:
        index = int((p / 100) * (n - 1))
        result[p] = valores_sorted[index]

    return result


# ============================================================================
# HELPERS DE HASH
# ============================================================================

def hash_fundos(fundos: List[FundoData]) -> int:
    """
    Gera hash de lista de fundos para invalidação de cache

    Args:
        fundos: Lista de fundos

    Returns:
        Hash integer
    """
    # Usar IDs e timestamps para gerar hash único
    hash_parts = []
    for f in fundos:
        hash_parts.append(f.nome)
        hash_parts.append(str(f.pl))
        hash_parts.append(str(f.ultima_atualizacao.timestamp() if f.ultima_atualizacao else 0))

    return hash(tuple(hash_parts))


# ============================================================================
# FUNÇÕES DE BENCHMARK
# ============================================================================

def benchmark_function(func, *args, iterations: int = 100, **kwargs):
    """
    Benchmarks uma função múltiplas vezes

    Args:
        func: Função a testar
        iterations: Número de iterações
        *args, **kwargs: Argumentos da função

    Returns:
        Dict com estatísticas (min, max, mean, total)
    """
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        times.append(elapsed)

    return {
        'min': min(times),
        'max': max(times),
        'mean': sum(times) / len(times),
        'total': sum(times),
        'iterations': iterations
    }
