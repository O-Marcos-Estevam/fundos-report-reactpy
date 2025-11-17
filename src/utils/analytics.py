"""
Utilitários de Analytics
Cálculos de KPIs avançados e métricas financeiras
"""

import math
from typing import List, Dict, Optional, Tuple
from models.fundo import FundoData


def calcular_sharpe_ratio(
    retornos: List[float],
    taxa_livre_risco: float = 0.0
) -> float:
    """
    Calcula o Sharpe Ratio

    Args:
        retornos: Lista de retornos percentuais
        taxa_livre_risco: Taxa livre de risco (default 0)

    Returns:
        Sharpe Ratio (retorno ajustado ao risco)
    """
    if not retornos or len(retornos) < 2:
        return 0.0

    # Retorno médio
    retorno_medio = sum(retornos) / len(retornos)

    # Desvio padrão
    variancia = sum((r - retorno_medio) ** 2 for r in retornos) / (len(retornos) - 1)
    desvio_padrao = math.sqrt(variancia)

    if desvio_padrao == 0:
        return 0.0

    # Sharpe Ratio
    sharpe = (retorno_medio - taxa_livre_risco) / desvio_padrao

    return round(sharpe, 2)


def calcular_volatilidade(retornos: List[float]) -> float:
    """
    Calcula a volatilidade (desvio padrão dos retornos)

    Args:
        retornos: Lista de retornos percentuais

    Returns:
        Volatilidade em percentual
    """
    if not retornos or len(retornos) < 2:
        return 0.0

    media = sum(retornos) / len(retornos)
    variancia = sum((r - media) ** 2 for r in retornos) / (len(retornos) - 1)
    volatilidade = math.sqrt(variancia)

    return round(volatilidade, 2)


def calcular_maximum_drawdown(valores: List[float]) -> Tuple[float, int, int]:
    """
    Calcula o Maximum Drawdown

    Args:
        valores: Lista de valores (PL ao longo do tempo)

    Returns:
        (drawdown_percentual, indice_pico, indice_vale)
    """
    if not valores or len(valores) < 2:
        return 0.0, 0, 0

    max_drawdown = 0.0
    pico = valores[0]
    indice_pico = 0
    indice_vale = 0

    for i, valor in enumerate(valores):
        if valor > pico:
            pico = valor
            indice_pico = i

        drawdown = ((valor - pico) / pico) * 100 if pico > 0 else 0

        if drawdown < max_drawdown:
            max_drawdown = drawdown
            indice_vale = i

    return round(max_drawdown, 2), indice_pico, indice_vale


def calcular_sortino_ratio(
    retornos: List[float],
    taxa_livre_risco: float = 0.0,
    target_return: float = 0.0
) -> float:
    """
    Calcula o Sortino Ratio (penaliza apenas volatilidade negativa)

    Args:
        retornos: Lista de retornos
        taxa_livre_risco: Taxa livre de risco
        target_return: Retorno alvo

    Returns:
        Sortino Ratio
    """
    if not retornos or len(retornos) < 2:
        return 0.0

    retorno_medio = sum(retornos) / len(retornos)

    # Desvio padrão descendente (apenas retornos abaixo do target)
    retornos_negativos = [r - target_return for r in retornos if r < target_return]

    if not retornos_negativos:
        return float('inf')  # Sem retornos negativos

    variancia_negativa = sum(r ** 2 for r in retornos_negativos) / len(retornos)
    desvio_negativo = math.sqrt(variancia_negativa)

    if desvio_negativo == 0:
        return 0.0

    sortino = (retorno_medio - taxa_livre_risco) / desvio_negativo

    return round(sortino, 2)


def calcular_information_ratio(
    retornos_fundo: List[float],
    retornos_benchmark: List[float]
) -> float:
    """
    Calcula o Information Ratio (excesso de retorno vs tracking error)

    Args:
        retornos_fundo: Retornos do fundo
        retornos_benchmark: Retornos do benchmark

    Returns:
        Information Ratio
    """
    if not retornos_fundo or not retornos_benchmark:
        return 0.0

    if len(retornos_fundo) != len(retornos_benchmark):
        return 0.0

    # Excesso de retorno
    excessos = [rf - rb for rf, rb in zip(retornos_fundo, retornos_benchmark)]

    excesso_medio = sum(excessos) / len(excessos)

    # Tracking error (desvio padrão do excesso)
    variancia = sum((e - excesso_medio) ** 2 for e in excessos) / (len(excessos) - 1)
    tracking_error = math.sqrt(variancia)

    if tracking_error == 0:
        return 0.0

    ir = excesso_medio / tracking_error

    return round(ir, 2)


def calcular_var(
    retornos: List[float],
    confianca: float = 0.95
) -> float:
    """
    Calcula o Value at Risk (VaR) histórico

    Args:
        retornos: Lista de retornos
        confianca: Nível de confiança (0.95 = 95%)

    Returns:
        VaR em percentual (valor positivo indica perda)
    """
    if not retornos:
        return 0.0

    retornos_sorted = sorted(retornos)
    index = int((1 - confianca) * len(retornos_sorted))

    if index >= len(retornos_sorted):
        index = len(retornos_sorted) - 1

    var = abs(retornos_sorted[index])

    return round(var, 2)


def calcular_cvar(
    retornos: List[float],
    confianca: float = 0.95
) -> float:
    """
    Calcula o Conditional Value at Risk (CVaR / Expected Shortfall)

    Args:
        retornos: Lista de retornos
        confianca: Nível de confiança

    Returns:
        CVaR em percentual
    """
    if not retornos:
        return 0.0

    var = calcular_var(retornos, confianca)

    # Média dos retornos piores que o VaR
    retornos_piores = [r for r in retornos if r <= -var]

    if not retornos_piores:
        return var

    cvar = abs(sum(retornos_piores) / len(retornos_piores))

    return round(cvar, 2)


def calcular_calmar_ratio(
    retorno_anual: float,
    max_drawdown: float
) -> float:
    """
    Calcula o Calmar Ratio (retorno anual / max drawdown)

    Args:
        retorno_anual: Retorno anualizado em %
        max_drawdown: Maximum drawdown em % (valor absoluto)

    Returns:
        Calmar Ratio
    """
    if max_drawdown == 0:
        return 0.0

    calmar = retorno_anual / abs(max_drawdown)

    return round(calmar, 2)


def calcular_metricas_fundo(fundo: FundoData) -> Dict[str, float]:
    """
    Calcula todas as métricas avançadas para um fundo

    Args:
        fundo: Dados do fundo

    Returns:
        Dicionário com todas as métricas
    """
    # Preparar série de retornos
    retornos = []
    if fundo.variacao_d30 != 0:
        retornos.append(fundo.variacao_d30)
    if fundo.variacao_d7 != 0:
        retornos.append(fundo.variacao_d7)
    if fundo.variacao_d1 != 0:
        retornos.append(fundo.variacao_d1)

    # Preparar série de valores
    valores = []
    if fundo.pl_d30 > 0:
        valores.append(fundo.pl_d30)
    if fundo.pl_d7 > 0:
        valores.append(fundo.pl_d7)
    if fundo.pl_d1 > 0:
        valores.append(fundo.pl_d1)
    valores.append(fundo.pl)

    # Calcular métricas
    metricas = {
        'sharpe_ratio': calcular_sharpe_ratio(retornos) if retornos else 0.0,
        'volatilidade': calcular_volatilidade(retornos) if retornos else 0.0,
        'sortino_ratio': calcular_sortino_ratio(retornos) if retornos else 0.0,
        'var_95': calcular_var(retornos, 0.95) if retornos else 0.0,
        'cvar_95': calcular_cvar(retornos, 0.95) if retornos else 0.0,
    }

    # Maximum Drawdown
    if len(valores) >= 2:
        max_dd, _, _ = calcular_maximum_drawdown(valores)
        metricas['max_drawdown'] = max_dd

        # Calmar Ratio (usando retorno médio como proxy)
        retorno_medio = sum(retornos) / len(retornos) if retornos else 0
        metricas['calmar_ratio'] = calcular_calmar_ratio(retorno_medio * 252, abs(max_dd))  # Anualizar
    else:
        metricas['max_drawdown'] = 0.0
        metricas['calmar_ratio'] = 0.0

    return metricas


def classificar_risco(volatilidade: float, max_drawdown: float) -> str:
    """
    Classifica o nível de risco baseado em volatilidade e drawdown

    Args:
        volatilidade: Volatilidade em %
        max_drawdown: Maximum drawdown em %

    Returns:
        Classificação: "Baixo", "Moderado", "Alto", "Muito Alto"
    """
    # Score de risco (0-100)
    score_vol = min(volatilidade * 10, 50)  # 0-50 pontos
    score_dd = min(abs(max_drawdown) * 5, 50)  # 0-50 pontos

    score_total = score_vol + score_dd

    if score_total < 20:
        return "Baixo"
    elif score_total < 40:
        return "Moderado"
    elif score_total < 70:
        return "Alto"
    else:
        return "Muito Alto"


def calcular_health_score(fundo: FundoData) -> int:
    """
    Calcula um score de saúde de 0-100 para o fundo

    Args:
        fundo: Dados do fundo

    Returns:
        Score de 0 a 100
    """
    score = 50  # Base

    # Performance positiva (+20 pontos)
    if fundo.variacao_d1 > 0:
        score += min(fundo.variacao_d1 * 2, 10)
    else:
        score += max(fundo.variacao_d1 * 2, -10)

    if fundo.variacao_d7 > 0:
        score += min(fundo.variacao_d7, 5)
    else:
        score += max(fundo.variacao_d7, -5)

    if fundo.variacao_d30 > 0:
        score += min(fundo.variacao_d30 / 2, 5)
    else:
        score += max(fundo.variacao_d30 / 2, -5)

    # Caixa adequado (±10 pontos)
    perc_caixa = fundo.perc_caixa_pl
    if 5 <= perc_caixa <= 15:
        score += 10  # Ideal
    elif 15 < perc_caixa <= 25:
        score += 5  # Aceitável
    elif perc_caixa > 25:
        score -= 10  # Alto demais
    elif perc_caixa < 5:
        score += 5  # Baixo, mas ok

    # Sem alertas (+10 pontos)
    if not fundo.tem_alertas():
        score += 10
    else:
        score -= len(fundo.get_alertas()) * 5

    # Limitar entre 0 e 100
    score = max(0, min(100, score))

    return int(score)


def get_health_score_label(score: int) -> str:
    """Retorna label textual do health score"""
    if score >= 80:
        return "Excelente"
    elif score >= 60:
        return "Bom"
    elif score >= 40:
        return "Regular"
    elif score >= 20:
        return "Ruim"
    else:
        return "Crítico"


def get_health_score_color(score: int) -> str:
    """Retorna cor do health score"""
    if score >= 80:
        return "#10b981"  # Green
    elif score >= 60:
        return "#84cc16"  # Lime
    elif score >= 40:
        return "#f59e0b"  # Amber
    elif score >= 20:
        return "#ef4444"  # Red
    else:
        return "#991b1b"  # Dark red
