from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from config.config import config


class RpaChallengePageObject(BasePage):
    """Page Object Model para o site RPA Challenge"""

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    # Propriedades dos XPaths
    @property
    def download_button_xpath(self) -> str:
        return config.XPATHS["download_button"]

    @property
    def start_button_xpath(self) -> str:
        return config.XPATHS["start_button"]

    @property
    def first_name_xpath(self) -> str:
        return config.XPATHS["first_name"]

    @property
    def last_name_xpath(self) -> str:
        return config.XPATHS["last_name"]

    @property
    def email_xpath(self) -> str:
        return config.XPATHS["email"]

    @property
    def address_xpath(self) -> str:
        return config.XPATHS["address"]

    @property
    def phone_number_xpath(self) -> str:
        return config.XPATHS["phone_number"]

    @property
    def company_name_xpath(self) -> str:
        return config.XPATHS["company_name"]

    @property
    def role_in_company_xpath(self) -> str:
        return config.XPATHS["role_in_company"]

    @property
    def submit_button_xpath(self) -> str:
        return config.XPATHS["submit_button"]

    # Métodos de ação
    def navigate_to_rpa_challenge(self) -> None:
        """Navega para o site RPA Challenge"""
        self.navigate_to(config.RPA_CHALLENGE_URL)

    def click_download_button(self) -> None:
        """Clica no botão de download"""
        self.click_element_by_xpath(self.download_button_xpath)

    def click_start_button(self) -> None:
        """Clica no botão de início"""
        self.click_element_by_xpath(self.start_button_xpath)

    def fill_first_name(self, first_name: str) -> None:
        """Preenche o campo de primeiro nome"""
        self.send_keys_to_element(self.first_name_xpath, first_name)

    def fill_last_name(self, last_name: str) -> None:
        """Preenche o campo de sobrenome"""
        self.send_keys_to_element(self.last_name_xpath, last_name)

    def fill_email(self, email: str) -> None:
        """Preenche o campo de email"""
        self.send_keys_to_element(self.email_xpath, email)

    def fill_address(self, address: str) -> None:
        """Preenche o campo de endereço"""
        self.send_keys_to_element(self.address_xpath, address)

    def fill_phone_number(self, phone_number: str) -> None:
        """Preenche o campo de número de telefone"""
        self.send_keys_to_element(self.phone_number_xpath, phone_number)

    def fill_company_name(self, company_name: str) -> None:
        """Preenche o campo de nome da empresa"""
        self.send_keys_to_element(self.company_name_xpath, company_name)

    def fill_role_in_company(self, role_in_company: str) -> None:
        """Preenche o campo de função na empresa"""
        self.send_keys_to_element(self.role_in_company_xpath, role_in_company)

    def click_submit_button(self) -> None:
        """Clica no botão de envio"""
        self.click_element_by_xpath(self.submit_button_xpath)

    def fill_employee_form(self, employee) -> None:
        """Preenche o formulário com dados de um funcionário"""
        self.fill_first_name(employee.first_name)
        self.fill_last_name(employee.last_name)
        self.fill_email(employee.email)
        self.fill_address(employee.address)
        self.fill_phone_number(employee.phone_number)
        self.fill_company_name(employee.company_name)
        self.fill_role_in_company(employee.role_in_company)
