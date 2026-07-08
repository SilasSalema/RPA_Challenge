import unittest
from models.employee import Employee


class TestEmployeeCreation(unittest.TestCase):
    """Testes de criação e inicialização de Employee"""

    def test_employee_creation_with_valid_data(self):
        """Testa criação de Employee com dados válidos"""
        emp = Employee(
            first_name="João",
            last_name="Silva",
            email="joao@example.com",
            address="Rua A, 123",
            phone_number="11 9999-9999",
            company_name="Tech Corp",
            role_in_company="Developer",
        )

        self.assertEqual(emp.first_name, "João")
        self.assertEqual(emp.last_name, "Silva")
        self.assertEqual(emp.email, "joao@example.com")
        self.assertEqual(emp.address, "Rua A, 123")
        self.assertEqual(emp.phone_number, "11 9999-9999")
        self.assertEqual(emp.company_name, "Tech Corp")
        self.assertEqual(emp.role_in_company, "Developer")

    def test_employee_string_representation(self):
        """Testa representação em string de Employee"""
        emp = Employee(
            first_name="Maria",
            last_name="Santos",
            email="maria@example.com",
            address="Rua B, 456",
            phone_number="11 8888-8888",
            company_name="Tech Corp",
            role_in_company="QA",
        )

        self.assertEqual(str(emp), "Maria Santos")

    def test_employee_with_empty_fields(self):
        """Testa criação de Employee com campos vazios"""
        emp = Employee(
            first_name="",
            last_name="",
            email="",
            address="",
            phone_number="",
            company_name="",
            role_in_company="",
        )

        self.assertEqual(emp.first_name, "")
        self.assertEqual(emp.last_name, "")
        self.assertEqual(str(emp), " ")


class TestEmployeeFromExcelRow(unittest.TestCase):
    """Testes para o método from_excel_row"""

    def test_from_excel_row_with_valid_data(self):
        """Testa conversão de linha Excel para Employee"""
        row = {
            "First Name": "Pedro",
            "Last Name ": "Costa",
            "Email": "pedro@example.com",
            "Address": "Rua C, 789",
            "Phone Number": "11 7777-7777",
            "Company Name": "Tech Solutions",
            "Role in Company": "Manager",
        }

        emp = Employee.from_excel_row(row)

        self.assertEqual(emp.first_name, "Pedro")
        self.assertEqual(emp.last_name, "Costa")
        self.assertEqual(emp.email, "pedro@example.com")
        self.assertEqual(emp.address, "Rua C, 789")
        self.assertEqual(emp.phone_number, "11 7777-7777")
        self.assertEqual(emp.company_name, "Tech Solutions")
        self.assertEqual(emp.role_in_company, "Manager")

    def test_from_excel_row_with_missing_keys(self):
        """Testa conversão com chaves ausentes (usa valores padrão vazios)"""
        row = {
            "First Name": "Ana",
            "Email": "ana@example.com",
        }

        emp = Employee.from_excel_row(row)

        self.assertEqual(emp.first_name, "Ana")
        self.assertEqual(emp.email, "ana@example.com")
        self.assertEqual(emp.last_name, "")
        self.assertEqual(emp.address, "")

    def test_from_excel_row_with_extra_keys(self):
        """Testa conversão ignorando chaves extras"""
        row = {
            "First Name": "Carlos",
            "Last Name ": "Oliveira",
            "Email": "carlos@example.com",
            "Address": "Rua D, 999",
            "Phone Number": "11 6666-6666",
            "Company Name": "Tech Inc",
            "Role in Company": "Analyst",
            "Extra Field": "Should be ignored",
            "Another Extra": "Also ignored",
        }

        emp = Employee.from_excel_row(row)

        self.assertEqual(emp.first_name, "Carlos")
        self.assertEqual(emp.last_name, "Oliveira")
        # Verifica que não tem atributos extras
        self.assertFalse(hasattr(emp, "Extra Field"))
        self.assertFalse(hasattr(emp, "Another Extra"))

    def test_from_excel_row_with_whitespace(self):
        """Testa conversão com dados contendo espaços"""
        row = {
            "First Name": "  Lucas  ",
            "Last Name ": "  Ferreira  ",
            "Email": "lucas@example.com",
            "Address": "Rua E, 555",
            "Phone Number": "11 5555-5555",
            "Company Name": "Tech Group",
            "Role in Company": "Architect",
        }

        emp = Employee.from_excel_row(row)

        # Nota: Não há limpeza de espaços em branco no método atual
        self.assertEqual(emp.first_name, "  Lucas  ")
        self.assertEqual(emp.last_name, "  Ferreira  ")


class TestEmployeeEquality(unittest.TestCase):
    """Testes de igualdade entre objetos Employee"""

    def test_employees_with_same_data_are_equal(self):
        """Testa igualdade entre dois Employees com mesmos dados"""
        emp1 = Employee(
            first_name="teste",
            last_name="usuario",
            email="teste@example.com",
            address="Rua teste",
            phone_number="11 1111-1111",
            company_name="Test Corp",
            role_in_company="Tester",
        )

        emp2 = Employee(
            first_name="teste",
            last_name="usuario",
            email="teste@example.com",
            address="Rua teste",
            phone_number="11 1111-1111",
            company_name="Test Corp",
            role_in_company="Tester",
        )

        self.assertEqual(emp1, emp2)

    def test_employees_with_different_data_are_not_equal(self):
        """Testa desigualdade entre dois Employees com dados diferentes"""
        emp1 = Employee(
            first_name="João",
            last_name="Silva",
            email="joao@example.com",
            address="Rua A",
            phone_number="11 1111-1111",
            company_name="Corp A",
            role_in_company="Dev",
        )

        emp2 = Employee(
            first_name="Maria",
            last_name="Santos",
            email="maria@example.com",
            address="Rua B",
            phone_number="11 2222-2222",
            company_name="Corp B",
            role_in_company="QA",
        )

        self.assertNotEqual(emp1, emp2)


if __name__ == "__main__":
    unittest.main()
