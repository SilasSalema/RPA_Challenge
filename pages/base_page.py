from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import config


class BasePage:
    """Classe base para Page Object Model"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.DEFAULT_WAIT_TIME)

    def navigate_to(self, url: str) -> None:
        """Navega para uma URL específica"""
        self.driver.get(url)

    def find_element_by_xpath(self, xpath: str):
        """Encontra um elemento pelo XPath"""
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def click_element_by_xpath(self, xpath: str) -> None:
        """Clica em um elemento localizado pelo XPath"""
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()

    def send_keys_to_element(self, xpath: str, keys: str) -> None:
        """Envia texto para um elemento localizado pelo XPath"""
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.send_keys(keys)

    def maximize_window(self) -> None:
        """Maximiza a janela do navegador"""
        self.driver.maximize_window()
