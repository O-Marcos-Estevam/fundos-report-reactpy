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
from app.config import CAMINHO_MODULO, get_modulo_config, AppConfig

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
        log_callback: Optional[Callable[[str], None]] = None,
        timeout: int = 300  # 5 minutos de timeout padrão
    ) -> ExecucaoInfo:
        """
        Executa a geração do relatório

        Args:
            data_relatorio: Data do relatório
            progress_callback: Função callback(progresso, mensagem)
            log_callback: Função callback(mensagem_log)
            timeout: Timeout em segundos (padrão: 300s = 5min)

        Returns:
            ExecucaoInfo com resultado da execução
        """
        # Verificar se está em modo DEMO (sem Access)
        if AppConfig.USE_MOCK_DATA:
            return self._executar_modo_demo(data_relatorio, progress_callback, log_callback)

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

                # 6. Coletar dados (com verificação de timeout)
                if progress_callback:
                    progress_callback(25, "Coletando dados do banco...")

                tempo_decorrido = time.time() - inicio
                if tempo_decorrido > timeout:
                    raise TimeoutError(f"Operação excedeu o tempo limite de {timeout}s")

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

    def _executar_modo_demo(
        self,
        data_relatorio: datetime,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        log_callback: Optional[Callable[[str], None]] = None
    ) -> ExecucaoInfo:
        """
        Executa relatório em modo DEMO (sem Access real)
        Retorna dados de exemplo já existentes no state_manager

        Args:
            data_relatorio: Data do relatório
            progress_callback: Função callback(progresso, mensagem)
            log_callback: Função callback(mensagem_log)

        Returns:
            ExecucaoInfo com dados de exemplo
        """
        from services.state_manager import get_state_manager

        inicio = time.time()

        # Simulação de progresso
        if progress_callback:
            progress_callback(10, "🎭 Modo Demonstração - Carregando dados de exemplo...")
            time.sleep(0.3)

        if log_callback:
            log_callback("INFO: Executando em modo DEMO")
            log_callback(f"INFO: Data do relatório: {data_relatorio.strftime('%d/%m/%Y')}")
            log_callback(f"INFO: Versão: {self.versao}")

        if progress_callback:
            progress_callback(30, "Carregando fundos de exemplo...")
            time.sleep(0.3)

        # Obter dados de exemplo do state_manager (já criados por init_data.py)
        state_manager = get_state_manager()
        execucao_exemplo = state_manager.ultima_execucao

        if log_callback:
            log_callback(f"INFO: {len(execucao_exemplo.fundos) if execucao_exemplo else 0} fundos carregados")

        if progress_callback:
            progress_callback(60, "Processando métricas...")
            time.sleep(0.3)

        if log_callback:
            log_callback("INFO: Calculando indicadores")
            log_callback("INFO: Gerando análises")

        if progress_callback:
            progress_callback(90, "Finalizando relatório...")
            time.sleep(0.3)

        # Criar execução baseada nos dados de exemplo
        execucao = ExecucaoInfo(
            data_relatorio=data_relatorio,
            data_execucao=datetime.now(),
            versao_modulo=self.versao,
            nome_modulo=f"DEMO_{self.versao}",
            status="sucesso",
            mensagem="🎭 MODO DEMONSTRAÇÃO - Relatório gerado com dados de exemplo",
            tempo_execucao=time.time() - inicio,
            fundos_processados=len(execucao_exemplo.fundos) if execucao_exemplo else 5,
            fundos=execucao_exemplo.fundos if execucao_exemplo else {},
            logs=[
                "🎭 Executado em modo DEMONSTRAÇÃO",
                f"Versão: {self.versao}",
                f"Data: {data_relatorio.strftime('%d/%m/%Y')}",
                f"Fundos: {len(execucao_exemplo.fundos) if execucao_exemplo else 5}",
                "⚠️ Para executar com dados reais, configure o banco Access localmente"
            ]
        )

        if progress_callback:
            progress_callback(100, "✅ Relatório DEMO concluído!")

        if log_callback:
            log_callback("SUCCESS: Execução concluída com sucesso")
            log_callback(f"SUCCESS: Tempo total: {execucao.tempo_execucao:.2f}s")

        return execucao

    def testar_conexao(self) -> Tuple[bool, Optional[str]]:
        """
        Testa a conexão com o banco de dados

        Returns:
            (sucesso, mensagem_erro)
        """
        # Modo demo sempre retorna sucesso
        if AppConfig.USE_MOCK_DATA:
            return True, "🎭 Modo DEMO - Usando dados de exemplo"

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
