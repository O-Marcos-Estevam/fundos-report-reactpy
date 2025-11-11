"""
Serviço de Gerenciamento de Histórico
Responsável por carregar, salvar e manipular o histórico de execuções
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

from models.historico import HistoricoEntry
from app.config import HISTORICO_FILE, AppConfig

logger = logging.getLogger(__name__)


class HistoricoService:
    """Serviço para gerenciar histórico de execuções"""

    def __init__(self, arquivo: Optional[Path] = None):
        """
        Inicializa o serviço de histórico

        Args:
            arquivo: Caminho do arquivo JSON (opcional, usa padrão se não fornecido)
        """
        self.arquivo = arquivo or HISTORICO_FILE
        self._cache: Optional[List[HistoricoEntry]] = None

    def carregar(self) -> List[HistoricoEntry]:
        """
        Carrega histórico do arquivo JSON

        Returns:
            Lista de entradas do histórico
        """
        if self._cache is not None:
            return self._cache

        if not self.arquivo.exists():
            logger.info(f"Arquivo de histórico não existe, criando: {self.arquivo}")
            self._cache = []
            return self._cache

        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._cache = [HistoricoEntry.from_dict(entry) for entry in data]
            logger.info(f"Histórico carregado: {len(self._cache)} entradas")
            return self._cache

        except Exception as e:
            logger.error(f"Erro ao carregar histórico: {e}")
            self._cache = []
            return self._cache

    def salvar(self, historico: List[HistoricoEntry]) -> bool:
        """
        Salva histórico no arquivo JSON

        Args:
            historico: Lista de entradas a salvar

        Returns:
            True se salvou com sucesso
        """
        try:
            # Garantir que o diretório existe
            self.arquivo.parent.mkdir(parents=True, exist_ok=True)

            # Converter para dicionários
            data = [entry.to_dict() for entry in historico]

            # Salvar com formatação
            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self._cache = historico
            logger.info(f"Histórico salvo: {len(historico)} entradas")
            return True

        except Exception as e:
            logger.error(f"Erro ao salvar histórico: {e}")
            return False

    def adicionar(
        self,
        data_relatorio: str,
        status: str,
        tempo_execucao: float,
        fundos_processados: int,
        detalhes: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Adiciona nova entrada ao histórico

        Args:
            data_relatorio: Data do relatório (YYYY-MM-DD)
            status: Status da execução (sucesso/erro)
            tempo_execucao: Tempo em segundos
            fundos_processados: Número de fundos processados
            detalhes: Detalhes adicionais (opcional)

        Returns:
            True se adicionou com sucesso
        """
        historico = self.carregar()

        # Criar nova entrada
        nova_entrada = HistoricoEntry(
            timestamp=datetime.now(),
            data_relatorio=data_relatorio,
            status=status,
            tempo_execucao=tempo_execucao,
            fundos_processados=fundos_processados,
            detalhes=detalhes or {}
        )

        # Adicionar no início
        historico.insert(0, nova_entrada)

        # Manter apenas últimas N entradas
        historico = historico[:AppConfig.MAX_HISTORICO_ENTRIES]

        # Salvar
        return self.salvar(historico)

    def limpar(self) -> bool:
        """
        Limpa todo o histórico

        Returns:
            True se limpou com sucesso
        """
        return self.salvar([])

    def obter_estatisticas(self) -> Dict[str, Any]:
        """
        Calcula estatísticas do histórico

        Returns:
            Dicionário com estatísticas
        """
        historico = self.carregar()

        if not historico:
            return {
                'total': 0,
                'sucessos': 0,
                'erros': 0,
                'taxa_sucesso': 0.0,
                'tempo_medio': 0.0,
                'tempo_total': 0.0
            }

        sucessos = [e for e in historico if e.sucesso]
        erros = [e for e in historico if not e.sucesso]

        tempo_medio = (
            sum(e.tempo_execucao for e in sucessos) / len(sucessos)
            if sucessos else 0.0
        )

        return {
            'total': len(historico),
            'sucessos': len(sucessos),
            'erros': len(erros),
            'taxa_sucesso': len(sucessos) / len(historico) * 100 if historico else 0.0,
            'tempo_medio': tempo_medio,
            'tempo_total': sum(e.tempo_execucao for e in historico)
        }

    def obter_ultimas(self, n: int = 20) -> List[HistoricoEntry]:
        """
        Retorna últimas N entradas

        Args:
            n: Número de entradas

        Returns:
            Lista de entradas
        """
        historico = self.carregar()
        return historico[:n]

    def obter_por_data(self, data: str) -> List[HistoricoEntry]:
        """
        Retorna entradas de uma data específica

        Args:
            data: Data no formato YYYY-MM-DD

        Returns:
            Lista de entradas
        """
        historico = self.carregar()
        return [e for e in historico if e.data_relatorio == data]

    def obter_por_periodo(self, data_inicio: datetime, data_fim: datetime) -> List[HistoricoEntry]:
        """
        Retorna entradas em um período

        Args:
            data_inicio: Data inicial
            data_fim: Data final

        Returns:
            Lista de entradas
        """
        historico = self.carregar()
        return [
            e for e in historico
            if data_inicio <= e.timestamp <= data_fim
        ]

    def agrupar_por_data(self) -> Dict[str, int]:
        """
        Agrupa execuções por data

        Returns:
            Dicionário {data: quantidade}
        """
        historico = self.carregar()
        resultado = {}

        for entry in historico:
            data = entry.timestamp.date().isoformat()
            resultado[data] = resultado.get(data, 0) + 1

        return resultado

    def invalidar_cache(self):
        """Invalida o cache forçando reload na próxima leitura"""
        self._cache = None
