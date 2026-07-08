import os
from dotenv import load_dotenv


class Config:
    """Classe para centralizar todas as configurações do projeto

    Todas as variáveis são lidas do arquivo .env ou de variáveis de ambiente
    com valores padrão como fallback.
    """

    def __init__(self):
        load_dotenv()
        self._load_configuration()

    def _load_configuration(self):
        """Carrega todas as configurações do .env ou variáveis de ambiente"""

        # URLs
        self.RPA_CHALLENGE_URL = os.getenv(
            "RPA_CHALLENGE_URL", "https://rpachallenge.com/"
        )

        # Paths
        self.DOWNLOAD_PATH = os.getenv("Caminho_Pasta_Downloads", "./downloads")
        self.EVIDENCE_PATH = os.getenv("caminho_evidencias", "./logs")

        # Browser
        self.REMOTE_URL = os.getenv("Remote_Url", "http://selenium-hub:4444/wd/hub")
        self.ENVIRONMENT = os.getenv("Environment", "local")
        self.BROWSER = os.getenv("Browser", "chrome")

        # Files
        self.EXCEL_FILE_NAME = os.getenv("Excel_File_Name", "challenge.xlsx")
        self.EXCEL_FILE_PATH = os.path.join(self.DOWNLOAD_PATH, self.EXCEL_FILE_NAME)

        # Timeouts
        self.DEFAULT_WAIT_TIME = int(os.getenv("Default_Wait_Time", "60"))
        self.FILE_DOWNLOAD_WAIT = int(os.getenv("File_Download_Wait", "5"))

        # XPaths (podem ser sobrescritos via .env com prefixo XPATH_)
        self.XPATHS = {
            "download_button": os.getenv(
                "XPATH_download_button",
                "/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/a",
            ),
            "start_button": os.getenv(
                "XPATH_start_button",
                "/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button",
            ),
            "first_name": os.getenv(
                "XPATH_first_name",
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "First Name")]/div/input',
            ),
            "last_name": os.getenv(
                "XPATH_last_name",
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Last Name")]/div/input',
            ),
            "email": os.getenv(
                "XPATH_email",
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Email")]/div/input',
            ),
            "address": os.getenv(
                "XPATH_address",
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Address")]/div/input',
            ),
            "phone_number": os.getenv(
                "XPATH_phone_number",
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Phone Number")]/div/input',
            ),
            "company_name": os.getenv(
                "XPATH_company_name",
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Company Name")]/div/input',
            ),
            "role_in_company": os.getenv(
                "XPATH_role_in_company",
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Role in Company")]/div/input',
            ),
            "submit_button": os.getenv(
                "XPATH_submit_button", "//input[contains(@type, 'submit')]"
            ),
        }


# Instância única de Config para ser importada em todo o projeto
config = Config()
