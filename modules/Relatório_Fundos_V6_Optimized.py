"""
Módulo V6 - Versão Mock para Deploy em Nuvem
Simula a execução do relatório sem necessidade de banco Access
"""

import time
import os
from datetime import datetime
from pathlib import Path


class ReportDiarioFundosV6:
    """Classe simulada do relatório V6"""

    def __init__(self, data_relatorio=None):
        """Inicializa o relatório"""
        self.data_relatorio = data_relatorio or datetime.now()
        self.fundos_processados = []
        self.arquivos_gerados = []

    def executar(self, callback=None):
        """
        Simula a execução do relatório

        Args:
            callback: Função de callback para progresso (opcional)
        """
        # Simular processamento com passos realistas
        passos = [
            (10, "Conectando ao banco de dados..."),
            (20, "Carregando dados dos fundos..."),
            (30, "Processando Fundo ABC Master FIC FIM"),
            (40, "Processando Fundo XYZ Multimercado FIC FIM"),
            (50, "Processando Fundo DEF Renda Fixa FIC FI"),
            (60, "Calculando métricas e indicadores..."),
            (70, "Gerando planilha Excel..."),
            (80, "Aplicando formatação..."),
            (90, "Salvando arquivo..."),
            (100, "Relatório gerado com sucesso!")
        ]

        for progresso, mensagem in passos:
            if callback:
                callback(progresso, mensagem)
            time.sleep(0.3)  # Simular tempo de processamento

        # Simular fundos processados
        self.fundos_processados = [
            "Fundo ABC Master FIC FIM",
            "Fundo XYZ Multimercado FIC FIM",
            "Fundo DEF Renda Fixa FIC FI",
            "Fundo GHI Ações FIC FIA",
            "Fundo JKL Previdência FIC FIM"
        ]

        # Simular arquivo gerado (sem criar arquivo real)
        data_str = self.data_relatorio.strftime("%Y%m%d")
        nome_arquivo = f"Relatorio_Fundos_V6_{data_str}.xlsx"
        self.arquivos_gerados = [nome_arquivo]

        return {
            'sucesso': True,
            'fundos': len(self.fundos_processados),
            'arquivo': nome_arquivo,
            'mensagem': f'Relatório V6 gerado com sucesso! {len(self.fundos_processados)} fundos processados.'
        }

    def get_fundos_processados(self):
        """Retorna lista de fundos processados"""
        return self.fundos_processados

    def get_arquivo_gerado(self):
        """Retorna caminho do arquivo gerado (simulado)"""
        return self.arquivos_gerados[0] if self.arquivos_gerados else None


# Para compatibilidade com código antigo
def gerar_relatorio(data_relatorio=None, callback=None):
    """Função wrapper para compatibilidade"""
    relatorio = ReportDiarioFundosV6(data_relatorio)
    return relatorio.executar(callback)
