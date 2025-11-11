"""
Modelo de Dados: Histórico de Execuções
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class HistoricoEntry:
    """Entrada no histórico de execuções"""

    # Timestamp
    timestamp: datetime
    data_relatorio: str  # YYYY-MM-DD

    # Status
    status: str  # sucesso, erro
    tempo_execucao: float
    fundos_processados: int

    # Detalhes opcionais
    detalhes: Dict[str, Any] = field(default_factory=dict)

    @property
    def sucesso(self) -> bool:
        """Verifica se foi bem sucedido"""
        return self.status == "sucesso"

    @property
    def data_formatada(self) -> str:
        """Retorna data formatada"""
        return self.timestamp.strftime("%d/%m/%Y %H:%M:%S")

    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'data_relatorio': self.data_relatorio,
            'status': self.status,
            'tempo_execucao': self.tempo_execucao,
            'fundos_processados': self.fundos_processados,
            'detalhes': self.detalhes
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'HistoricoEntry':
        """Cria instância a partir de dicionário"""
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            timestamp=timestamp,
            data_relatorio=data.get('data_relatorio', ''),
            status=data.get('status', 'erro'),
            tempo_execucao=data.get('tempo_execucao', 0.0),
            fundos_processados=data.get('fundos_processados', 0),
            detalhes=data.get('detalhes', {})
        )

    def __repr__(self) -> str:
        return f"HistoricoEntry(data={self.data_relatorio}, status='{self.status}', tempo={self.tempo_execucao:.1f}s)"
