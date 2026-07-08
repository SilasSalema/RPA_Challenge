import unittest
import os
from unittest.mock import patch
from config.config import Config


class TestConfigInitialization(unittest.TestCase):
    """Testes de inicialização da classe Config"""

    def test_config_has_required_attributes(self):
        """Testa se Config possui todos os atributos necessários"""
        config = Config()

        # URLs
        self.assertTrue(hasattr(config, "RPA_CHALLENGE_URL"))
        self.assertTrue(hasattr(config, "REMOTE_URL"))

        # Paths
        self.assertTrue(hasattr(config, "DOWNLOAD_PATH"))
        self.assertTrue(hasattr(config, "EVIDENCE_PATH"))
        self.assertTrue(hasattr(config, "EXCEL_FILE_PATH"))

        # Browser
        self.assertTrue(hasattr(config, "ENVIRONMENT"))
        self.assertTrue(hasattr(config, "BROWSER"))

        # Timeouts
        self.assertTrue(hasattr(config, "DEFAULT_WAIT_TIME"))
        self.assertTrue(hasattr(config, "FILE_DOWNLOAD_WAIT"))

        # XPaths
        self.assertTrue(hasattr(config, "XPATHS"))
        self.assertIsInstance(config.XPATHS, dict)

    def test_config_default_values(self):
        """Testa valores padrão da configuração"""
        config = Config()

        # Verificar valores padrão
        self.assertEqual(config.RPA_CHALLENGE_URL, "https://rpachallenge.com/")
        self.assertEqual(config.BROWSER, "chrome")
        # ENVIRONMENT pode ser 'docker' ou 'local' conforme .env
        self.assertIn(config.ENVIRONMENT, ["local", "docker", "remote"])
        self.assertEqual(config.DEFAULT_WAIT_TIME, 60)
        self.assertEqual(config.FILE_DOWNLOAD_WAIT, 5)

    def test_config_xpaths_dictionary(self):
        """Testa se XPATHS contém as chaves esperadas"""
        config = Config()

        expected_keys = [
            "download_button",
            "start_button",
            "first_name",
            "last_name",
            "email",
            "address",
            "phone_number",
            "company_name",
            "role_in_company",
            "submit_button",
        ]

        for key in expected_keys:
            self.assertIn(key, config.XPATHS)
            self.assertIsInstance(config.XPATHS[key], str)
            self.assertTrue(len(config.XPATHS[key]) > 0)


class TestConfigEnvironmentVariables(unittest.TestCase):
    """Testes para leitura de variáveis de ambiente"""

    @patch.dict(
        os.environ,
        {
            "RPA_CHALLENGE_URL": "https://custom-url.com/",
            "Caminho_Pasta_Downloads": "/custom/downloads",
            "Default_Wait_Time": "120",
        },
    )
    def test_config_reads_environment_variables(self):
        """Testa se Config lê variáveis de ambiente"""
        config = Config()

        self.assertEqual(config.RPA_CHALLENGE_URL, "https://custom-url.com/")
        self.assertEqual(config.DOWNLOAD_PATH, "/custom/downloads")
        self.assertEqual(config.DEFAULT_WAIT_TIME, 120)

    def test_config_uses_defaults_when_env_not_set(self):
        """Testa se Config usa valores padrão quando variável não está definida"""
        # Remove a variável de ambiente se existir
        os.environ.pop("RPA_CHALLENGE_URL", None)

        config = Config()

        # Deve usar o valor padrão
        self.assertEqual(config.RPA_CHALLENGE_URL, "https://rpachallenge.com/")


class TestConfigFilePathConstruction(unittest.TestCase):
    """Testes para construção de caminhos de arquivo"""

    def test_excel_file_path_construction(self):
        """Testa construção do caminho do arquivo Excel"""
        config = Config()

        # O caminho deve ser construído como DOWNLOAD_PATH/EXCEL_FILE_NAME
        expected_path = os.path.join(config.DOWNLOAD_PATH, config.EXCEL_FILE_NAME)
        self.assertEqual(config.EXCEL_FILE_PATH, expected_path)

    def test_excel_file_name_default(self):
        """Testa nome padrão do arquivo Excel"""
        config = Config()

        self.assertEqual(config.EXCEL_FILE_NAME, "challenge.xlsx")


class TestConfigTypeConversion(unittest.TestCase):
    """Testes para conversão de tipos de variáveis de ambiente"""

    @patch.dict(os.environ, {"Default_Wait_Time": "90", "File_Download_Wait": "3"})
    def test_timeout_values_are_integers(self):
        """Testa se timeouts são convertidos para inteiros"""
        config = Config()

        self.assertIsInstance(config.DEFAULT_WAIT_TIME, int)
        self.assertIsInstance(config.FILE_DOWNLOAD_WAIT, int)
        self.assertEqual(config.DEFAULT_WAIT_TIME, 90)
        self.assertEqual(config.FILE_DOWNLOAD_WAIT, 3)

    @patch.dict(os.environ, {"Default_Wait_Time": "invalid"})
    def test_invalid_timeout_raises_error(self):
        """Testa se timeout inválido levanta exceção"""
        with self.assertRaises(ValueError):
            config = Config()


if __name__ == "__main__":
    unittest.main()
