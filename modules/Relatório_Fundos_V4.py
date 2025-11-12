"""
Módulo V4 - Versão Mock para Deploy em Nuvem
Simula a execução do relatório sem necessidade de banco Access
"""

import time
from datetime import datetime


class ReportDiarioFundosV4:
    """Classe simulada do relatório V4"""

    def __init__(self, data_relatorio=None):
        """Inicializa o relatório"""
        self.data_relatorio = data_relatorio or datetime.now()
        self.fundos_processados = []
        self.arquivos_gerados = []

    def executar(self, callback=None):
        """
        Simula a execução do relatório V4

        Args:
            callback: Função de callback para progresso (opcional)
        """
        passos = [
            (15, "Iniciando relatório V4..."),
            (30, "Lendo dados..."),
            (50, "Processando fundos..."),
            (75, "Gerando planilha..."),
            (100, "Finalizado!")
        ]

        for progresso, mensagem in passos:
            if callback:
                callback(progresso, mensagem)
            time.sleep(0.2)

        # Simular fundos processados
        self.fundos_processados = [
            "Fundo ABC Master FIC FIM",
            "Fundo XYZ Multimercado FIC FIM"
        ]

        # Simular arquivo gerado
        data_str = self.data_relatorio.strftime("%Y%m%d")
        nome_arquivo = f"Relatorio_Fundos_V4_{data_str}.xlsx"
        self.arquivos_gerados = [nome_arquivo]

        return {
            'sucesso': True,
            'fundos': len(self.fundos_processados),
            'arquivo': nome_arquivo,
            'mensagem': f'Relatório V4 gerado! {len(self.fundos_processados)} fundos processados.'
        }

    def get_fundos_processados(self):
        """Retorna lista de fundos processados"""
        return self.fundos_processados

    def get_arquivo_gerado(self):
        """Retorna caminho do arquivo gerado (simulado)"""
        return self.arquivos_gerados[0] if self.arquivos_gerados else None


def gerar_relatorio(data_relatorio=None, callback=None):
    """Função wrapper para compatibilidade"""
    relatorio = ReportDiarioFundosV4(data_relatorio)
    return relatorio.executar(callback)
