import os
import requests
import json

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from helpers.tratar_erro_helper import *
from urllib3.exceptions import ProtocolError


class BrowserService:
    def __init__(self) -> None:
        pass

    def _get_remote_url(self):
        return os.getenv("Remote_Url") or "http://selenium-hub:4444/wd/hub"

    def _get_environment(self):
        return os.getenv("Environment")

    def _get_browser(self):
        return os.getenv("Browser")

    def _get_browser_options(self):
        match self._get_browser():
            case "firefox":
                return webdriver.FirefoxOptions()
            case default:
                return webdriver.ChromeOptions()

    def _get_manager_options(self, options_browser):
        match self._get_environment():
            case "local":
                return self._get_options_local(options_browser)
            case "docker":
                return self._get_options_docker(options_browser)
            case "remote":
                return self._get_options_remote(options_browser)
            case default:
                return options_browser

    def _get_options_general(self, options_browser):
        options_browser.add_argument("--lang=en-US")
        options_browser.add_argument("--disable-infobars")
        options_browser.add_argument("--no-sandbox")
        options_browser.add_argument("--disable-dev-shm-usage")
        options_browser.add_argument("--disable-extensions")
        options_browser.add_argument("--disable-gpu")

        chrome_prefs = {}
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        options_browser.experimental_options["prefs"] = chrome_prefs
        return options_browser

    def _get_options_local(self, options_browser):
        options_browser.add_argument("--start-maximized")
        options_browser.add_argument("--disk-cache-size=1")
        options_browser.add_argument("--media-cache-size=1")
        options_browser.add_argument("--disable-application-cache")
        options_browser.add_argument("--force-device-scale-factor=1.0")

        # Configurar a pasta de download apenas para o ambiente local
        download_directory = os.getenv(
            "Caminho_Pasta_Downloads"
        )  # Altere para o caminho desejado
        chrome_prefs = {
            "download.default_directory": download_directory,  # Define a pasta de download
            "download.prompt_for_download": False,  # Desativa o prompt de download
            "download.directory_upgrade": True,  # Permite a atualização do diretório
            "safebrowsing.enabled": True,  # Habilita o modo de navegação segura
        }
        options_browser.experimental_options["prefs"] = chrome_prefs
        return options_browser

    def _get_options_docker(self, options_browser):
        options_browser.add_argument("--headless")
        return options_browser

    def _get_options_remote(self, options_browser):
        options_browser.add_argument("--start-maximized")
        options_browser.add_argument("--disk-cache-size=1")
        options_browser.add_argument("--media-cache-size=1")
        options_browser.add_argument("--disable-application-cache")
        options_browser.add_argument("--force-device-scale-factor=1.0")
        cloud_options = {
            "name": f"Bot",
        }
        options_browser.set_capability("cloud:options", cloud_options)
        return options_browser

    def _get_driver_remote_with_retry(
        self, options_browser, max_retries=3, backoff_factor=1
    ):
        for attempt in range(max_retries):
            try:
                match self._get_environment():
                    case "local":
                        return self._get_driver_local(options_browser)
                    case "docker":
                        return self._get_driver_docker(options_browser)
                    case "remote":
                        return self._get_driver_remote(options_browser)
                    case default:
                        return None
            except ProtocolError as e:
                self.inserir_info_banco_de_dados(
                    f"Tentativa {attempt + 1} falhou com erro: {e}"
                )
                time.sleep(backoff_factor * (2**attempt))  # Exponential backoff
            except Exception as e:
                print(f"Um erro inesperado aconteceu: {e}")
                break

    def _get_manager_driver(self, options_browser):
        match self._get_environment():
            case "local":
                return self._get_driver_local(options_browser)
            case "docker":
                return self._get_driver_docker(options_browser)
            case "remote":
                return self._get_driver_remote(options_browser)
            case default:
                return None

    def _get_driver_local(self, options_browser):
        match self._get_browser():
            case "firefox":
                return webdriver.Firefox(options=options_browser)
            case default:
                return webdriver.Chrome(options=options_browser)

    def _get_driver_docker(self, options_browser):
        match self._get_browser():
            case "firefox":
                return webdriver.Firefox(options=options_browser)
            case default:
                return webdriver.Chrome(options=options_browser)

    def _get_driver_remote(self, options_browser):
        try:
            remote_url = self._get_remote_url()
            return webdriver.Remote(
                command_executor=remote_url,
                options=options_browser,
            )
        except:
            self.finalizar_todas_as_sessoes_selenium_grid()
            return Exception("Sessão selenium grid indisponível ")

    def abrir_navegador(self) -> WebDriver:
        options_browser = self._get_browser_options()
        options_browser = self._get_options_general(options_browser)
        options_browser = self._get_manager_options(options_browser)
        driver = self._get_driver_remote_with_retry(options_browser)
        driver.set_page_load_timeout(120)
        return driver

    def abrir_nova_aba(self, driver) -> None:
        driver.switch_to.new_window("tab")

    def focar_na_aba(self, driver, numero_aba: int) -> None:
        driver.switch_to.window(driver.window_handles[numero_aba])

    def fechar_aba(self, driver) -> None:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    def fechar_navegador(self, driver) -> None:
        driver.quit()
