from helpers.criar_arquivo_log_helper import configurar_arquivo_log
from controllers.rpa_challenge_controller import RpaChallengeController


def main():
    """Função principal do RPA Challenge"""

    # Configurar logging
    logging = configurar_arquivo_log()

    try:
        logging.info("Iniciou Execução")

        # Criar e executar controller
        controller = RpaChallengeController(logging)
        controller.execute()

        logging.info("Terminou Execução")

    except Exception as e:
        logging.error(f"Erro na execução: {str(e)}")
        raise


if __name__ == "__main__":
    main()
