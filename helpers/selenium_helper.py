from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from helpers.tratar_erro_helper import *


def navegar_site_rpa_challenge(driver: WebDriver) -> None:
    driver.get("https://rpachallenge.com/")


def baixar_excel(driver: WebDriver) -> None:
    wait = WebDriverWait(driver, 60)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/a",
            )
        )
    ).click()


def clicar_botao_iniciar(driver: WebDriver) -> None:
    wait = WebDriverWait(driver, 60)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button",
            )
        )
    ).click()


def inserir_primeiro_nome(driver: WebDriver, primeiro_nome: str) -> None:
    wait = WebDriverWait(driver, 60)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "First Name")]/div/input',
            )
        )
    ).send_keys(primeiro_nome)


def inserir_sobrenome(driver: WebDriver, sobrenome: str) -> None:
    wait = WebDriverWait(driver, 60)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Last Name")]/div/input',
            )
        )
    ).send_keys(sobrenome)


def inserir_endereco(driver: WebDriver, endereco: str) -> None:
    wait = WebDriverWait(driver, 60)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Address")]/div/input',
            )
        )
    ).send_keys(endereco)


def inserir_numero_telefone(driver: WebDriver, numero_telefone: str) -> None:
    wait = WebDriverWait(driver, 60)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Phone Number")]/div/input',
            )
        )
    ).send_keys(numero_telefone)


def inserir_email(driver: WebDriver, email: str) -> None:
    wait = WebDriverWait(driver, 60)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Email")]/div/input',
            )
        )
    ).send_keys(email)


def inserir_nome_empresa(driver: WebDriver, nome_empresa: str) -> None:
    wait = WebDriverWait(driver, 60)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Company Name")]/div/input',
            )
        )
    ).send_keys(nome_empresa)


def inserir_funcao_empresa(driver: WebDriver, funcao_empresa: str) -> None:
    wait = WebDriverWait(driver, 60)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//rpa1-field[contains(@ng-reflect-dictionary-value, "Role in Company")]/div/input',
            )
        )
    ).send_keys(funcao_empresa)


def clicar_botao_enviar(driver: WebDriver) -> None:
    wait = WebDriverWait(driver, 60)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//input[contains(@type, 'submit')]",
            )
        )
    ).click()
