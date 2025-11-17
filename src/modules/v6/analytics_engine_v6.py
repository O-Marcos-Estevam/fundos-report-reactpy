"""
ANALYTICS ENGINE V6 - Motor de Análise e Inteligência
Sistema de análise preditiva, alertas e métricas avançadas
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Níveis de alerta"""
    OK = "✓ OK"
    INFO = "ℹ Info"
    WARNING = "⚠ Alerta"
    CRITICAL = "✗ Crítico"


@dataclass
class FundoMetrics:
    """Métricas calculadas para um fundo"""
    fundo: str
    tipo: str

    # Patrimônio
    pl_atual: float
    pl_d1: float
    pl_d7: float
    pl_d30: float

    # Variações
    var_d1: Optional[float]
    var_d7: Optional[float]
    var_d30: Optional[float]

    # Caixa
    caixa_total: float
    caixa_bancario: float
    fundos_di: float

    # Passivo
    devido_taxas: float
    ncg: float

    # Indicadores
    perc_caixa_pl: Optional[float]
    liquidez_dias: Optional[float]
    vol_pl_30d: Optional[float]  # Volatilidade

    # Status
    status: AlertLevel
    alertas: List[str]

    # Score (0-100)
    health_score: float


class AnalyticsEngine:
    """Motor de análise e inteligência"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.alerts_config = config.get('alerts', {})

        # Thresholds
        self.pl_drop_critical = self.alerts_config.get('pl_drop_critical', -0.05)
        self.pl_drop_warning = self.alerts_config.get('pl_drop_warning', -0.02)
        self.caixa_high = self.alerts_config.get('caixa_high_threshold', 0.30)
        self.liquidez_critical = self.alerts_config.get('liquidez_critical', 30)

        logger.info("AnalyticsEngine inicializado")

    def calcular_variacao(self, atual: float, anterior: float) -> Optional[float]:
        """Calcula variação percentual segura"""
        if not anterior or anterior == 0:
            return None

        if anterior < 0:
            if atual > 0:
                return None
            else:
                return round(1 - atual / anterior, 4)
        else:
            if atual < 0:
                return None
            else:
                return round(atual / anterior - 1, 4)

    def calcular_ncg(self, devido_taxas: float, caixa_total: float) -> float:
        """Calcula Necessidade de Capital de Giro"""
        if -devido_taxas > caixa_total:
            return -(devido_taxas + caixa_total)
        return 0

    def calcular_liquidez_dias(self, caixa_total: float, devido_taxas: float) -> Optional[float]:
        """Calcula quantos dias de operação o caixa suporta"""
        if devido_taxas >= 0:
            return None

        dias_operacao = abs(caixa_total / devido_taxas) if devido_taxas != 0 else 999
        return round(dias_operacao, 1)

    def calcular_volatilidade(self, pl_atual: float, pl_d7: float, pl_d30: float) -> Optional[float]:
        """Calcula volatilidade do PL (desvio padrão simplificado)"""
        valores = [v for v in [pl_atual, pl_d7, pl_d30] if v and v > 0]

        if len(valores) < 2:
            return None

        return round(np.std(valores) / np.mean(valores) * 100, 2)

    def determinar_status_e_alertas(self, metrics: Dict[str, Any]) -> Tuple[AlertLevel, List[str]]:
        """
        Determina status e lista de alertas baseado em regras de negócio

        Returns:
            Tuple com (AlertLevel, List[str] de alertas)
        """
        alertas = []
        nivel = AlertLevel.OK

        # Regra 1: Queda de PL
        if metrics.get('var_d1'):
            var_d1 = metrics['var_d1']

            if var_d1 < self.pl_drop_critical:
                alertas.append(f"PL caiu {abs(var_d1)*100:.1f}% em D-1")
                nivel = AlertLevel.CRITICAL

            elif var_d1 < self.pl_drop_warning:
                alertas.append(f"PL caiu {abs(var_d1)*100:.1f}% em D-1")
                if nivel.value < AlertLevel.WARNING.value:
                    nivel = AlertLevel.WARNING

        # Regra 2: Liquidez baixa
        liquidez = metrics.get('liquidez_dias')
        if liquidez and liquidez < self.liquidez_critical:
            alertas.append(f"Liquidez baixa: {liquidez:.0f} dias")
            if liquidez < self.liquidez_critical / 2:
                nivel = AlertLevel.CRITICAL
            elif nivel.value < AlertLevel.WARNING.value:
                nivel = AlertLevel.WARNING

        # Regra 3: Caixa insuficiente vs taxas
        devido_taxas = metrics.get('devido_taxas', 0)
        caixa_total = metrics.get('caixa_total', 0)

        if devido_taxas < 0:
            if abs(devido_taxas) > caixa_total:
                alertas.append("Caixa insuficiente para taxas")
                nivel = AlertLevel.CRITICAL

            elif abs(devido_taxas) > caixa_total * 0.8:
                alertas.append("Caixa próximo do limite de taxas")
                if nivel.value < AlertLevel.WARNING.value:
                    nivel = AlertLevel.WARNING

        # Regra 4: Caixa muito alto (ocioso)
        perc_caixa = metrics.get('perc_caixa_pl')
        if perc_caixa and perc_caixa > self.caixa_high:
            alertas.append(f"Caixa elevado: {perc_caixa*100:.1f}% do PL")
            if nivel == AlertLevel.OK:
                nivel = AlertLevel.INFO

        # Regra 5: Volatilidade alta
        vol = metrics.get('vol_pl_30d')
        if vol and vol > 15:
            alertas.append(f"Alta volatilidade: {vol:.1f}%")
            if nivel == AlertLevel.OK:
                nivel = AlertLevel.INFO

        # Regra 6: NCG positiva (precisa de capital)
        ncg = metrics.get('ncg', 0)
        if ncg > 0:
            alertas.append(f"NCG positiva: R$ {ncg:,.0f}")
            if nivel.value < AlertLevel.WARNING.value:
                nivel = AlertLevel.WARNING

        return nivel, alertas

    def calcular_health_score(self, metrics: Dict[str, Any], alertas: List[str],
                             nivel: AlertLevel) -> float:
        """
        Calcula score de saúde do fundo (0-100)

        Componentes:
        - 40 pts: Performance (variação PL)
        - 30 pts: Liquidez
        - 20 pts: Estabilidade (volatilidade)
        - 10 pts: Conformidade (alertas)
        """
        score = 100.0

        # 1. Performance (40 pontos)
        var_d1 = metrics.get('var_d1')
        if var_d1 is not None:
            if var_d1 < -0.10:
                score -= 40
            elif var_d1 < -0.05:
                score -= 30
            elif var_d1 < -0.02:
                score -= 15
            elif var_d1 < 0:
                score -= 5
            elif var_d1 > 0.05:
                score += 5  # Bônus

        # 2. Liquidez (30 pontos)
        liquidez = metrics.get('liquidez_dias')
        if liquidez is not None:
            if liquidez < 15:
                score -= 30
            elif liquidez < 30:
                score -= 20
            elif liquidez < 60:
                score -= 10
            # > 60 dias = sem penalidade

        # 3. Estabilidade (20 pontos)
        vol = metrics.get('vol_pl_30d')
        if vol is not None:
            if vol > 20:
                score -= 20
            elif vol > 15:
                score -= 15
            elif vol > 10:
                score -= 10
            elif vol > 5:
                score -= 5

        # 4. Conformidade (10 pontos)
        if nivel == AlertLevel.CRITICAL:
            score -= 10
        elif nivel == AlertLevel.WARNING:
            score -= 5

        # Normalizar entre 0-100
        return max(0, min(100, score))

    def analisar_fundo(self, fundo: str, dados: Dict[str, Any], tipo: str) -> FundoMetrics:
        """
        Analisa um fundo e retorna métricas completas

        Args:
            fundo: Nome do fundo
            dados: Dados do fundo
            tipo: Tipo (FIP, FIDC, FIM, etc)

        Returns:
            FundoMetrics com todas as métricas calculadas
        """
        # Extrair valores
        pl_atual = dados.get('pl', 0) or 0
        pl_d1 = dados.get('pl_d1', 0) or 0
        pl_d7 = dados.get('pl_d7', 0) or 0
        pl_d30 = dados.get('pl_d30', 0) or 0

        caixa_bancario = dados.get('caixa_bancario', 0) or 0
        fundos_di = dados.get('fundos_di', 0) or 0
        caixa_total = dados.get('caixa_total', 0) or caixa_bancario + fundos_di

        devido_taxas = dados.get('devido_taxas', 0) or 0

        # Calcular métricas
        var_d1 = self.calcular_variacao(pl_atual, pl_d1)
        var_d7 = self.calcular_variacao(pl_atual, pl_d7)
        var_d30 = self.calcular_variacao(pl_atual, pl_d30)

        ncg = self.calcular_ncg(devido_taxas, caixa_total)

        perc_caixa_pl = (caixa_total / pl_atual) if pl_atual > 0 else None
        liquidez_dias = self.calcular_liquidez_dias(caixa_total, devido_taxas)
        vol_pl_30d = self.calcular_volatilidade(pl_atual, pl_d7, pl_d30)

        # Dict para análise
        metrics_dict = {
            'var_d1': var_d1,
            'var_d7': var_d7,
            'var_d30': var_d30,
            'caixa_total': caixa_total,
            'devido_taxas': devido_taxas,
            'liquidez_dias': liquidez_dias,
            'perc_caixa_pl': perc_caixa_pl,
            'vol_pl_30d': vol_pl_30d,
            'ncg': ncg
        }

        # Determinar status e alertas
        status, alertas = self.determinar_status_e_alertas(metrics_dict)

        # Calcular health score
        health_score = self.calcular_health_score(metrics_dict, alertas, status)

        return FundoMetrics(
            fundo=fundo,
            tipo=tipo,
            pl_atual=pl_atual,
            pl_d1=pl_d1,
            pl_d7=pl_d7,
            pl_d30=pl_d30,
            var_d1=var_d1,
            var_d7=var_d7,
            var_d30=var_d30,
            caixa_total=caixa_total,
            caixa_bancario=caixa_bancario,
            fundos_di=fundos_di,
            devido_taxas=devido_taxas,
            ncg=ncg,
            perc_caixa_pl=perc_caixa_pl,
            liquidez_dias=liquidez_dias,
            vol_pl_30d=vol_pl_30d,
            status=status,
            alertas=alertas,
            health_score=health_score
        )

    def analisar_carteira_completa(self, fundos_dados: Dict[str, Dict[str, Any]],
                                   tipo_mapping: Dict[str, str]) -> List[FundoMetrics]:
        """
        Analisa todos os fundos da carteira

        Args:
            fundos_dados: Dicionário com dados de todos os fundos
            tipo_mapping: Mapeamento fundo -> tipo

        Returns:
            Lista de FundoMetrics ordenada por health_score
        """
        logger.info(f"Analisando {len(fundos_dados)} fundos...")

        metricas = []
        for fundo, dados in fundos_dados.items():
            tipo = tipo_mapping.get(fundo, self._determinar_tipo(fundo))
            metrics = self.analisar_fundo(fundo, dados, tipo)
            metricas.append(metrics)

        # Ordenar por health score (piores primeiro para alertar)
        metricas.sort(key=lambda m: m.health_score)

        # Log de resumo
        criticos = sum(1 for m in metricas if m.status == AlertLevel.CRITICAL)
        alertas = sum(1 for m in metricas if m.status == AlertLevel.WARNING)

        logger.info(f"Análise concluída: {criticos} críticos, {alertas} alertas")

        return metricas

    def _determinar_tipo(self, fundo: str) -> str:
        """Determina tipo do fundo pelo nome"""
        fundo_upper = fundo.upper()
        if 'FIDC' in fundo_upper:
            return 'FIDC'
        elif 'FIP' in fundo_upper:
            return 'FIP'
        elif 'FIM' in fundo_upper:
            return 'FIM'
        else:
            return 'OUTROS'

    def gerar_relatorio_executivo(self, metricas: List[FundoMetrics]) -> Dict[str, Any]:
        """
        Gera relatório executivo consolidado

        Returns:
            Dict com estatísticas agregadas
        """
        if not metricas:
            return {}

        total_fundos = len(metricas)

        # Agregações por tipo
        por_tipo = {}
        for m in metricas:
            if m.tipo not in por_tipo:
                por_tipo[m.tipo] = {
                    'count': 0,
                    'pl_total': 0,
                    'caixa_total': 0,
                    'devido_total': 0,
                    'health_avg': []
                }

            por_tipo[m.tipo]['count'] += 1
            por_tipo[m.tipo]['pl_total'] += m.pl_atual
            por_tipo[m.tipo]['caixa_total'] += m.caixa_total
            por_tipo[m.tipo]['devido_total'] += m.devido_taxas
            por_tipo[m.tipo]['health_avg'].append(m.health_score)

        # Calcular médias
        for tipo_data in por_tipo.values():
            tipo_data['health_avg'] = np.mean(tipo_data['health_avg'])

        # Totais gerais
        pl_total = sum(m.pl_atual for m in metricas)
        caixa_total = sum(m.caixa_total for m in metricas)
        devido_total = sum(m.devido_taxas for m in metricas)

        # Contadores de status
        status_counts = {
            'ok': sum(1 for m in metricas if m.status == AlertLevel.OK),
            'info': sum(1 for m in metricas if m.status == AlertLevel.INFO),
            'warning': sum(1 for m in metricas if m.status == AlertLevel.WARNING),
            'critical': sum(1 for m in metricas if m.status == AlertLevel.CRITICAL)
        }

        # Top 10 melhores e piores
        top_10_melhores = sorted(metricas, key=lambda m: m.health_score, reverse=True)[:10]
        top_10_piores = sorted(metricas, key=lambda m: m.health_score)[:10]

        # Fundos com alertas críticos
        criticos = [m for m in metricas if m.status == AlertLevel.CRITICAL]

        return {
            'total_fundos': total_fundos,
            'pl_total': pl_total,
            'caixa_total': caixa_total,
            'devido_total': devido_total,
            'perc_caixa_pl': (caixa_total / pl_total) if pl_total > 0 else 0,
            'health_score_medio': np.mean([m.health_score for m in metricas]),
            'por_tipo': por_tipo,
            'status_counts': status_counts,
            'top_10_melhores': [asdict(m) for m in top_10_melhores],
            'top_10_piores': [asdict(m) for m in top_10_piores],
            'fundos_criticos': [asdict(m) for m in criticos],
            'timestamp': datetime.now().isoformat()
        }

    def detectar_anomalias(self, metricas: List[FundoMetrics]) -> List[Dict[str, Any]]:
        """
        Detecta anomalias estatísticas na carteira

        Returns:
            Lista de anomalias detectadas
        """
        anomalias = []

        # Calcular z-scores para PL
        pls = [m.pl_atual for m in metricas if m.pl_atual > 0]
        if len(pls) > 3:
            pl_mean = np.mean(pls)
            pl_std = np.std(pls)

            for m in metricas:
                if m.pl_atual > 0 and pl_std > 0:
                    z_score = (m.pl_atual - pl_mean) / pl_std

                    if abs(z_score) > 3:  # Outlier
                        anomalias.append({
                            'fundo': m.fundo,
                            'tipo': 'PL_OUTLIER',
                            'descricao': f"PL anormal: z-score={z_score:.2f}",
                            'valor': m.pl_atual,
                            'severidade': 'high' if abs(z_score) > 4 else 'medium'
                        })

        # Detectar variações extremas
        for m in metricas:
            if m.var_d1 and abs(m.var_d1) > 0.20:  # Variação > 20%
                anomalias.append({
                    'fundo': m.fundo,
                    'tipo': 'VARIACAO_EXTREMA',
                    'descricao': f"Variação D-1: {m.var_d1*100:.1f}%",
                    'valor': m.var_d1,
                    'severidade': 'high'
                })

        # Detectar fundos zerados inesperadamente
        for m in metricas:
            if m.pl_atual == 0 and m.pl_d1 > 0:
                anomalias.append({
                    'fundo': m.fundo,
                    'tipo': 'FUNDO_ZERADO',
                    'descricao': "Fundo zerado inesperadamente",
                    'valor': m.pl_d1,
                    'severidade': 'critical'
                })

        logger.info(f"Detectadas {len(anomalias)} anomalias")
        return anomalias
