import unittest
from unittest.mock import Mock, MagicMock, patch
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.rpa_challenge_page import RpaChallengePageObject
from config.config import Config


class TestBasePageInitialization(unittest.TestCase):
    """Testes de inicialização da classe BasePage"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.mock_driver = Mock(spec=WebDriver)

    def test_base_page_initialization(self):
        """Testa inicialização de BasePage"""
        page = BasePage(self.mock_driver)

        self.assertEqual(page.driver, self.mock_driver)
        self.assertIsNotNone(page.wait)

    def test_base_page_has_wait_timeout(self):
        """Testa se BasePage tem WebDriverWait configurado"""
        page = BasePage(self.mock_driver)

        # O wait deve ter um timeout
        self.assertIsNotNone(page.wait)
        self.assertEqual(page.wait._timeout, Config().DEFAULT_WAIT_TIME)


class TestRpaChallengePageObjectProperties(unittest.TestCase):
    """Testes das propriedades XPath do RpaChallengePageObject"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.mock_driver = Mock(spec=WebDriver)
        self.page = RpaChallengePageObject(self.mock_driver)

    def test_page_has_all_xpath_properties(self):
        """Testa se RpaChallengePageObject tem todas as propriedades de XPath"""
        xpath_properties = [
            "download_button_xpath",
            "start_button_xpath",
            "first_name_xpath",
            "last_name_xpath",
            "email_xpath",
            "address_xpath",
            "phone_number_xpath",
            "company_name_xpath",
            "role_in_company_xpath",
            "submit_button_xpath",
        ]

        for prop in xpath_properties:
            self.assertTrue(
                hasattr(self.page, prop), f"Page deve ter propriedade {prop}"
            )
            xpath_value = getattr(self.page, prop)
            self.assertIsInstance(xpath_value, str)
            self.assertTrue(len(xpath_value) > 0)

    def test_xpaths_are_from_config(self):
        """Testa se XPaths vêm da configuração"""
        config = Config()

        self.assertEqual(
            self.page.download_button_xpath, config.XPATHS["download_button"]
        )
        self.assertEqual(self.page.start_button_xpath, config.XPATHS["start_button"])
        self.assertEqual(self.page.first_name_xpath, config.XPATHS["first_name"])
        self.assertEqual(self.page.last_name_xpath, config.XPATHS["last_name"])


class TestRpaChallengePageObjectMethods(unittest.TestCase):
    """Testes dos métodos do RpaChallengePageObject"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.mock_driver = Mock(spec=WebDriver)
        self.page = RpaChallengePageObject(self.mock_driver)

    def test_page_has_action_methods(self):
        """Testa se page tem todos os métodos de ação"""
        action_methods = [
            "navigate_to_rpa_challenge",
            "click_download_button",
            "click_start_button",
            "fill_first_name",
            "fill_last_name",
            "fill_email",
            "fill_address",
            "fill_phone_number",
            "fill_company_name",
            "fill_role_in_company",
            "click_submit_button",
            "fill_employee_form",
        ]

        for method in action_methods:
            self.assertTrue(
                hasattr(self.page, method), f"Page deve ter método {method}"
            )
            self.assertTrue(
                callable(getattr(self.page, method)), f"{method} deve ser callable"
            )

    @patch("pages.base_page.WebDriverWait")
    def test_navigate_to_rpa_challenge_calls_driver(self, mock_wait):
        """Testa se navigate_to_rpa_challenge chama o driver corretamente"""
        self.page.navigate_to_rpa_challenge()

        self.mock_driver.get.assert_called_once_with(Config().RPA_CHALLENGE_URL)

    def test_fill_first_name_calls_send_keys(self):
        """Testa se fill_first_name funciona"""
        with patch.object(self.page, "send_keys_to_element") as mock_send_keys:
            self.page.fill_first_name("João")

            mock_send_keys.assert_called_once()

    def test_fill_last_name_calls_send_keys(self):
        """Testa se fill_last_name funciona"""
        with patch.object(self.page, "send_keys_to_element") as mock_send_keys:
            self.page.fill_last_name("Silva")

            mock_send_keys.assert_called_once()

    def test_fill_email_calls_send_keys(self):
        """Testa se fill_email funciona"""
        with patch.object(self.page, "send_keys_to_element") as mock_send_keys:
            self.page.fill_email("test@example.com")

            mock_send_keys.assert_called_once()

    def test_fill_address_calls_send_keys(self):
        """Testa se fill_address funciona"""
        with patch.object(self.page, "send_keys_to_element") as mock_send_keys:
            self.page.fill_address("Rua A, 123")

            mock_send_keys.assert_called_once()


class TestRpaChallengePageObjectIntegration(unittest.TestCase):
    """Testes de integração do RpaChallengePageObject"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.mock_driver = Mock(spec=WebDriver)
        self.page = RpaChallengePageObject(self.mock_driver)

    def test_fill_employee_form_calls_all_fill_methods(self):
        """Testa se fill_employee_form chama todos os métodos de preenchimento"""
        from models.employee import Employee

        employee = Employee(
            first_name="João",
            last_name="Silva",
            email="joao@example.com",
            address="Rua A, 123",
            phone_number="11 9999-9999",
            company_name="Tech Corp",
            role_in_company="Developer",
        )

        with patch.object(
            self.page, "fill_first_name"
        ) as mock_fill_first, patch.object(
            self.page, "fill_last_name"
        ) as mock_fill_last, patch.object(
            self.page, "fill_email"
        ) as mock_fill_email, patch.object(
            self.page, "fill_address"
        ) as mock_fill_address, patch.object(
            self.page, "fill_phone_number"
        ) as mock_fill_phone, patch.object(
            self.page, "fill_company_name"
        ) as mock_fill_company, patch.object(
            self.page, "fill_role_in_company"
        ) as mock_fill_role:

            self.page.fill_employee_form(employee)

            mock_fill_first.assert_called_once_with(employee.first_name)
            mock_fill_last.assert_called_once_with(employee.last_name)
            mock_fill_email.assert_called_once_with(employee.email)
            mock_fill_address.assert_called_once_with(employee.address)
            mock_fill_phone.assert_called_once_with(employee.phone_number)
            mock_fill_company.assert_called_once_with(employee.company_name)
            mock_fill_role.assert_called_once_with(employee.role_in_company)


if __name__ == "__main__":
    unittest.main()
