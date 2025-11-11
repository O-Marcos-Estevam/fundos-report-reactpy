"""
Serviço de Execução de Relatórios
Responsável por importar e executar os módulos V4/V5/V6
"""

import sys
import importlib
import logging
import time
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from typing import Optional, Tuple, Callable, Any
from pathlib import Path

from models.execucao import ExecucaoInfo
from models.fundo import FundoData
from app.config import CAMINHO_MODULO, get_modulo_config

logger = logging.getLogger(__name__)


class LogCapture(io.StringIO):
    """Captura logs de stdout/stderr"""

    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        super().__init__()
        self.callback = callback
        self.logs = []

    def write(self, text: str) -> int:
        if text and text.strip():
            self.logs.append(text.strip())
            if self.callback:
                try:
                    self.callback(text.strip())
                except Exception:
                    pass
        return super().write(text)


class ReportExecutor:
    """Executor de relatórios com suporte a V4/V5/V6"""

    def __init__(self, versao: str = 'V6'):
        """
        Inicializa o executor

        Args:
            versao: Versão do módulo ('V4', 'V5' ou 'V6')
        """
        self.versao = versao
        self.config = get_modulo_config(versao)
        self.modulo = None
        self.ReportClass = None

        # Adicionar caminho dos módulos ao sys.path
        if CAMINHO_MODULO not in sys.path:
            sys.path.append(CAMINHO_MODULO)

    def importar_modulo(self) -> Tuple[bool, Optional[str]]:
        """
        Importa o módulo de relatório

        Returns:
            (sucesso, mensagem_erro)
        """
        for nome_possivel in self.config.nomes_possiveis:
            try:
                # Recarregar se já estiver importado
                if nome_possivel in sys.modules:
                    self.modulo = importlib.reload(sys.modules[nome_possivel])
                else:
                    self.modulo = importlib.import_module(nome_possivel)

                # Tentar obter a classe
                self.ReportClass = getattr(self.modulo, self.config.nome_classe)

                logger.info(f"Módulo {nome_possivel} importado com sucesso")
                return True, None

            except ImportError as e:
                logger.debug(f"Tentativa de importar {nome_possivel} falhou: {e}")
                continue
            except AttributeError as e:
                logger.error(f"Classe {self.config.nome_classe} não encontrada em {nome_possivel}: {e}")
                return False, f"Classe {self.config.nome_classe} não encontrada"

        # Nenhum módulo funcionou
        erro = f"Não foi possível importar nenhuma variação do módulo {self.versao}"
        logger.error(erro)
        return False, erro

    def executar(
        self,
        data_relatorio: datetime,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        log_callback: Optional[Callable[[str], None]] = None
    ) -> ExecucaoInfo:
        """
        Executa a geração do relatório

        Args:
            data_relatorio: Data do relatório
            progress_callback: Função callback(progresso, mensagem)
            log_callback: Função callback(mensagem_log)

        Returns:
            ExecucaoInfo com resultado da execução
        """
        execucao = ExecucaoInfo(
            data_relatorio=data_relatorio,
            versao_modulo=self.versao,
            status="iniciado"
        )

        inicio = time.time()

        try:
            # 1. Importar módulo
            if progress_callback:
                progress_callback(5, "Importando módulo...")

            sucesso, erro = self.importar_modulo()
            if not sucesso:
                raise Exception(f"Erro ao importar módulo: {erro}")

            execucao.nome_modulo = self.modulo.__name__
            execucao.status = "processando"

            # 2. Capturar logs
            log_capture = LogCapture(log_callback)

            with redirect_stdout(log_capture), redirect_stderr(log_capture):
                # 3. Criar instância do relatório
                if progress_callback:
                    progress_callback(10, "Criando instância do relatório...")

                report = self.ReportClass()

                # 4. Configurar data
                report.input_date = data_relatorio
                report.input_date_str = data_relatorio.strftime("%m/%d/%Y")

                # 5. Validar ambiente
                if progress_callback:
                    progress_callback(15, "Validando ambiente...")

                if not report.validar_ambiente():
                    raise Exception("Falha na validação do ambiente")

                # 6. Coletar dados
                if progress_callback:
                    progress_callback(25, "Coletando dados do banco...")

                report.coletar_dados_completos()
                execucao.fundos_processados = len(report.fundos_dados)

                # Converter fundos_dados para FundoData
                for nome, dados in report.fundos_dados.items():
                    execucao.fundos[nome] = FundoData.from_dict({'nome': nome, **dados})

                if progress_callback:
                    progress_callback(45, f"{execucao.fundos_processados} fundos coletados")

                # 7. Criar workbook
                if progress_callback:
                    progress_callback(50, "Criando estrutura do relatório...")

                report.criar_workbook()

                # 8. Fluxo específico por versão
                if self.versao == 'V6':
                    self._executar_fluxo_v6(report, progress_callback)
                elif self.versao == 'V5':
                    self._executar_fluxo_v5(report, progress_callback)
                else:  # V4
                    self._executar_fluxo_v4(report, progress_callback)

                # 9. Finalizar
                if progress_callback:
                    progress_callback(100, "Relatório gerado com sucesso!")

                execucao.status = "sucesso"
                execucao.report = report

                # Obter arquivos gerados
                execucao.arquivos_gerados = self._obter_arquivos_gerados(report)

            # Copiar logs
            execucao.logs = log_capture.logs

        except Exception as e:
            execucao.status = "erro"
            execucao.mensagem = str(e)
            execucao.logs.append(f"ERRO: {str(e)}")
            execucao.logs.append(traceback.format_exc())
            logger.error(f"Erro na execução do relatório: {e}", exc_info=True)

            if progress_callback:
                progress_callback(0, f"Erro: {str(e)}")

        finally:
            execucao.tempo_execucao = time.time() - inicio

        return execucao

    def _executar_fluxo_v6(self, report: Any, progress_callback: Optional[Callable]):
        """Executa fluxo específico do V6"""
        if progress_callback:
            progress_callback(55, "Executando análise preditiva...")
        report.analisar_fundos()

        if progress_callback:
            progress_callback(60, "Criando resumo executivo V6...")
        report.criar_resumo_executivo_v6()

        if progress_callback:
            progress_callback(70, "Escrevendo dados detalhados...")
        report.escrever_dados_detalhados_v6()

        if progress_callback:
            progress_callback(85, "Gerando alertas e anomalias...")
        report.criar_aba_alertas()

        if progress_callback:
            progress_callback(95, "Salvando arquivos...")
        report.salvar_relatorio()

    def _executar_fluxo_v5(self, report: Any, progress_callback: Optional[Callable]):
        """Executa fluxo específico do V5"""
        if progress_callback:
            progress_callback(55, "Criando resumo executivo...")
        report.criar_resumo_executivo()

        if progress_callback:
            progress_callback(60, "Escrevendo cabeçalhos...")
        report.escrever_headers_dados()

        if progress_callback:
            progress_callback(70, "Processando dados dos fundos...")
        report.escrever_dados_fundos_enhanced()

        if progress_callback:
            progress_callback(80, "Aplicando formatação condicional...")
        report.aplicar_formatacao_condicional()

        if progress_callback:
            progress_callback(85, "Criando análise por tipo...")
        report.criar_analise_por_tipo()

        if progress_callback:
            progress_callback(95, "Salvando arquivos...")
        report.salvar_relatorio()

    def _executar_fluxo_v4(self, report: Any, progress_callback: Optional[Callable]):
        """Executa fluxo específico do V4"""
        if progress_callback:
            progress_callback(60, "Escrevendo cabeçalhos...")
        report.escrever_headers()

        if progress_callback:
            progress_callback(70, "Processando dados dos fundos...")
        report.escrever_dados_fundos()

        if progress_callback:
            progress_callback(90, "Aplicando formatação...")
        report.aplicar_formatacao()

        if progress_callback:
            progress_callback(95, "Salvando arquivos...")
        report.salvar_relatorio()

    def _obter_arquivos_gerados(self, report: Any) -> list[str]:
        """Obtém lista de arquivos gerados"""
        arquivos = []

        # Arquivo principal
        if hasattr(report, 'OUTPUT_PATH'):
            arquivos.append(report.OUTPUT_PATH)
        elif hasattr(report, 'config'):
            arquivos.append(report.config['output']['main_path'])

        # Arquivo backup
        if hasattr(report, 'REPORTS_DIR'):
            reports_dir = report.REPORTS_DIR
        elif hasattr(report, 'config'):
            reports_dir = report.config['output']['reports_dir']
        else:
            reports_dir = None

        if reports_dir:
            from pathlib import Path
            # Procurar arquivos recentes no diretório
            reports_path = Path(reports_dir)
            if reports_path.exists():
                for arquivo in reports_path.glob(f"Daily_Report_{self.versao}_*.xlsx"):
                    arquivos.append(str(arquivo))

        return arquivos

    def testar_conexao(self) -> Tuple[bool, Optional[str]]:
        """
        Testa a conexão com o banco de dados

        Returns:
            (sucesso, mensagem_erro)
        """
        try:
            sucesso, erro = self.importar_modulo()
            if not sucesso:
                return False, erro

            report = self.ReportClass()

            if self.versao == 'V6':
                # V6 usa DatabaseManager
                return True, "Conexão V6 OK (DatabaseManager)"
            else:
                # V4/V5 testam conexão diretamente
                conn = report.conectar_access()
                conn.close()
                return True, "Conexão testada com sucesso"

        except Exception as e:
            return False, str(e)
