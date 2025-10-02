from concurrent.futures import *
from dotenv import load_dotenv


from services.browser_service import BrowserService
from helpers.criar_arquivo_log_helper import configurar_arquivo_log
from helpers.tratar_erro_helper import *
from helpers.selenium_helper import *
from helpers.excel_helper import *


class RpaChallengeService(BrowserService):
    @tratar_erro
    def __init__(self) -> None:
        load_dotenv()
        self.logging = configurar_arquivo_log()
        self.logging.info("Iniciou Execução")
        self.execucao()
        self.logging.info("Terminou Execução")

    def execucao(self) -> None:
        driver = self.abrir_navegador()
        navegar_site_rpa_challenge(driver)
        excluir_arquivo_excel()
        baixar_excel(driver)
        existe = verificar_se_arquivo_excel_existe()
        if existe:
            data_frame = obter_data_frame_do_arquivo_excel()
            clicar_botao_iniciar(driver)
            for numero_linha, dados_linha in data_frame.iterrows():
                inserir_primeiro_nome(driver, dados_linha["First Name"])
                inserir_sobrenome(driver, dados_linha["Last Name "])
                inserir_email(driver, dados_linha["Email"])
                inserir_endereco(driver, dados_linha["Address"])
                inserir_numero_telefone(driver, dados_linha["Phone Number"])
                inserir_nome_empresa(driver, dados_linha["Company Name"])
                inserir_funcao_empresa(driver, dados_linha["Role in Company"])
                clicar_botao_enviar(driver)
