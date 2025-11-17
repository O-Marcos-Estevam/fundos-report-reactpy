"""
Modelo de Dados: Fundo de Investimento
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class FundoData:
    """Representa os dados de um fundo de investimento"""

    # Identificação
    nome: str
    tipo: str = "-"

    # Patrimônio Líquido
    pl: float = 0.0
    pl_d1: float = 0.0
    pl_d7: float = 0.0
    pl_d30: float = 0.0
    pl_posicao_ativos: float = 0.0

    # Caixa
    caixa_total: float = 0.0
    caixa_bancario: float = 0.0
    caixa_reag_ii: float = 0.0

    # Taxas
    devido_taxas: float = 0.0

    # Cotista
    cotista: Optional[str] = None

    # Valores JCOT
    vl_bruto: float = 0.0
    vl_liquido: float = 0.0

    # Metadata
    data_referencia: Optional[datetime] = None
    ultima_atualizacao: datetime = field(default_factory=datetime.now)

    @property
    def perc_caixa_pl(self) -> float:
        """Percentual de caixa sobre PL"""
        if self.pl > 0:
            return (self.caixa_total / self.pl) * 100
        return 0.0

    @property
    def variacao_d1(self) -> float:
        """Variação percentual em relação a D-1"""
        if self.pl_d1 > 0:
            return ((self.pl - self.pl_d1) / self.pl_d1) * 100
        return 0.0

    @property
    def variacao_d7(self) -> float:
        """Variação percentual em relação a D-7"""
        if self.pl_d7 > 0:
            return ((self.pl - self.pl_d7) / self.pl_d7) * 100
        return 0.0

    @property
    def variacao_d30(self) -> float:
        """Variação percentual em relação a D-30"""
        if self.pl_d30 > 0:
            return ((self.pl - self.pl_d30) / self.pl_d30) * 100
        return 0.0

    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'nome': self.nome,
            'tipo': self.tipo,
            'pl': self.pl,
            'pl_d1': self.pl_d1,
            'pl_d7': self.pl_d7,
            'pl_d30': self.pl_d30,
            'pl_posicao_ativos': self.pl_posicao_ativos,
            'caixa_total': self.caixa_total,
            'caixa_bancario': self.caixa_bancario,
            'caixa_reag_ii': self.caixa_reag_ii,
            'devido_taxas': self.devido_taxas,
            'cotista': self.cotista,
            'vl_bruto': self.vl_bruto,
            'vl_liquido': self.vl_liquido,
            'perc_caixa_pl': self.perc_caixa_pl,
            'variacao_d1': self.variacao_d1,
            'variacao_d7': self.variacao_d7,
            'variacao_d30': self.variacao_d30,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'FundoData':
        """Cria instância a partir de dicionário"""
        # Filtrar apenas campos válidos
        valid_fields = {k: v for k, v in data.items() if k in cls.__annotations__}
        return cls(**valid_fields)

    def tem_alertas(self) -> bool:
        """Verifica se o fundo tem algum alerta"""
        alertas = []

        # Caixa alto
        if self.perc_caixa_pl > 20:
            alertas.append(True)

        # Variação negativa significativa
        if self.variacao_d1 < -5:
            alertas.append(True)
        elif self.variacao_d1 < -2:
            alertas.append(True)

        # Taxas devidas significativas
        if self.devido_taxas > 0 and self.pl > 0:
            perc_taxas = (self.devido_taxas / self.pl) * 100
            if perc_taxas > 1:
                alertas.append(True)

        return len(alertas) > 0

    def get_alertas(self) -> list[tuple[str, str]]:
        """Retorna lista de alertas (nivel, mensagem)"""
        alertas = []

        # Caixa alto
        perc_caixa = self.perc_caixa_pl
        if perc_caixa > 20:
            alertas.append(("warning", f"Percentual de caixa elevado: {perc_caixa:.2f}%"))

        # Variação negativa
        if self.variacao_d1 < -5:
            alertas.append(("error", f"Queda significativa no PL: {self.variacao_d1:.2f}% em D-1"))
        elif self.variacao_d1 < -2:
            alertas.append(("warning", f"Queda no PL: {self.variacao_d1:.2f}% em D-1"))

        # Taxas devidas
        if self.devido_taxas > 0 and self.pl > 0:
            perc_taxas = (self.devido_taxas / self.pl) * 100
            if perc_taxas > 1:
                alertas.append(("info", f"Taxas devidas: {perc_taxas:.2f}% do PL"))

        return alertas

    def __repr__(self) -> str:
        return f"FundoData(nome='{self.nome}', tipo='{self.tipo}', pl={self.pl:,.2f})"
