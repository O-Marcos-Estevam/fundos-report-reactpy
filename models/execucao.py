"""
Modelo de Dados: Execução de Relatório
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from .fundo import FundoData


@dataclass
class ExecucaoInfo:
    """Informações de uma execução de relatório"""

    # Identificação
    data_relatorio: datetime
    data_execucao: datetime = field(default_factory=datetime.now)

    # Status
    status: str = "iniciado"  # iniciado, processando, sucesso, erro
    mensagem: Optional[str] = None

    # Métricas
    tempo_execucao: float = 0.0
    fundos_processados: int = 0

    # Dados
    fundos: Dict[str, FundoData] = field(default_factory=dict)
    logs: list[str] = field(default_factory=list)

    # Módulo usado
    versao_modulo: str = "V6"
    nome_modulo: Optional[str] = None

    # Arquivos gerados
    arquivos_gerados: list[str] = field(default_factory=list)

    # Report object (para compatibilidade)
    report: Optional[Any] = None

    @property
    def sucesso(self) -> bool:
        """Verifica se a execução foi bem sucedida"""
        return self.status == "sucesso"

    @property
    def total_pl(self) -> float:
        """PL total de todos os fundos"""
        return sum(f.pl for f in self.fundos.values())

    @property
    def total_caixa(self) -> float:
        """Caixa total de todos os fundos"""
        return sum(f.caixa_total for f in self.fundos.values())

    @property
    def perc_caixa_pl(self) -> float:
        """Percentual médio de caixa/PL"""
        if self.total_pl > 0:
            return (self.total_caixa / self.total_pl) * 100
        return 0.0

    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'data_relatorio': self.data_relatorio.isoformat(),
            'data_execucao': self.data_execucao.isoformat(),
            'status': self.status,
            'mensagem': self.mensagem,
            'tempo_execucao': self.tempo_execucao,
            'fundos_processados': self.fundos_processados,
            'versao_modulo': self.versao_modulo,
            'nome_modulo': self.nome_modulo,
            'arquivos_gerados': self.arquivos_gerados,
            'total_pl': self.total_pl,
            'total_caixa': self.total_caixa,
            'perc_caixa_pl': self.perc_caixa_pl,
        }

    def add_log(self, mensagem: str):
        """Adiciona uma linha ao log"""
        self.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {mensagem}")

    def get_fundos_por_tipo(self) -> Dict[str, list[FundoData]]:
        """Agrupa fundos por tipo"""
        result = {}
        for fundo in self.fundos.values():
            tipo = fundo.tipo
            if tipo not in result:
                result[tipo] = []
            result[tipo].append(fundo)
        return result

    def get_top_fundos(self, n: int = 10, ordenar_por: str = 'pl') -> list[FundoData]:
        """Retorna top N fundos ordenados por critério"""
        return sorted(
            self.fundos.values(),
            key=lambda f: getattr(f, ordenar_por, 0),
            reverse=True
        )[:n]

    def get_fundos_com_alertas(self) -> list[FundoData]:
        """Retorna fundos que possuem alertas"""
        return [f for f in self.fundos.values() if f.tem_alertas()]

    def __repr__(self) -> str:
        return f"ExecucaoInfo(data={self.data_relatorio.strftime('%Y-%m-%d')}, status='{self.status}', fundos={self.fundos_processados})"
