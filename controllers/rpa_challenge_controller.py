import os
import time
from logging import Logger

from selenium.webdriver.remote.webdriver import WebDriver

from config.config import config
from models.employee import Employee
from pages.rpa_challenge_page import RpaChallengePageObject
from services.browser_service import BrowserService
from helpers.excel_helper import (
    verificar_se_arquivo_excel_existe,
    excluir_arquivo_excel,
    obter_data_frame_do_arquivo_excel,
)


class RpaChallengeController(BrowserService):
    """Controller que orquestra a lógica de negócio do RPA Challenge"""

    def __init__(self, logger: Logger):
        """
        Inicializa o controller

        Args:
            logger: Logger para registrar eventos
        """
        super().__init__()
        self.logger = logger
        self.driver: WebDriver = None
        self.page_object: RpaChallengePageObject = None
        self.employees: list[Employee] = []

    def execute(self) -> None:
        """Executa todo o fluxo do RPA Challenge"""
        try:
            self.logger.info("Iniciando execução do RPA Challenge")

            # Inicializar browser
            self._initialize_browser()

            # Navegar para o site
            self._navigate_to_site()

            # Baixar arquivo Excel
            self._download_and_prepare_excel()

            # Processar dados e preencher formulário
            self._process_employee_data()

            self.logger.info("Execução concluída com sucesso")

        except Exception as e:
            self.logger.error(f"Erro durante a execução: {str(e)}")
            raise
        finally:
            self._cleanup()

    def _initialize_browser(self) -> None:
        """Inicializa o browser e o Page Object Model"""
        self.logger.info("Inicializando navegador")
        self.driver = self.abrir_navegador()
        self.page_object = RpaChallengePageObject(self.driver)

    def _navigate_to_site(self) -> None:
        """Navega para o site RPA Challenge"""
        self.logger.info(f"Navegando para {config.RPA_CHALLENGE_URL}")
        self.page_object.navigate_to_rpa_challenge()

    def _download_and_prepare_excel(self) -> None:
        """Baixa o arquivo Excel e prepara para processamento"""
        self.logger.info("Excluindo arquivo Excel anterior (se existir)")
        excluir_arquivo_excel()

        self.logger.info("Clicando no botão de download")
        self.page_object.click_download_button()

        self.logger.info(
            f"Aguardando download do arquivo por {config.FILE_DOWNLOAD_WAIT}s"
        )
        time.sleep(config.FILE_DOWNLOAD_WAIT)

        # Verificar se o arquivo foi baixado
        if not verificar_se_arquivo_excel_existe():
            raise Exception("Arquivo Excel não foi baixado")

        self.logger.info("Arquivo Excel baixado com sucesso")

    def _load_employees_from_excel(self) -> None:
        """Carrega dados de funcionários do arquivo Excel"""
        self.logger.info("Carregando dados de funcionários do Excel")

        data_frame = obter_data_frame_do_arquivo_excel()
        self.employees = []

        for numero_linha, dados_linha in data_frame.iterrows():
            employee = Employee.from_excel_row(dados_linha)
            self.employees.append(employee)
            self.logger.info(f"Funcionário carregado: {employee}")

    def _process_employee_data(self) -> None:
        """Processa dados de funcionários e preenche o formulário"""
        self.logger.info("Iniciando clique no botão de início")
        self.page_object.click_start_button()

        # Carregar funcionários do Excel
        self._load_employees_from_excel()

        # Processar cada funcionário
        for idx, employee in enumerate(self.employees, 1):
            self.logger.info(
                f"Processando funcionário {idx}/{len(self.employees)}: {employee}"
            )

            try:
                self._fill_and_submit_form(employee)
            except Exception as e:
                self.logger.error(f"Erro ao processar funcionário {employee}: {str(e)}")
                raise

    def _fill_and_submit_form(self, employee: Employee) -> None:
        """Preenche e envia o formulário com dados de um funcionário"""
        self.logger.info(
            f"Preenchendo formulário para {employee.first_name} {employee.last_name}"
        )

        # Preencher formulário
        self.page_object.fill_employee_form(employee)

        # Enviar formulário
        self.logger.info("Clicando no botão de envio")
        self.page_object.click_submit_button()

    def _cleanup(self) -> None:
        """Limpa recursos (fecha o navegador)"""
        self.logger.info("Fechando navegador")
        if self.driver:
            self.fechar_navegador(self.driver)
