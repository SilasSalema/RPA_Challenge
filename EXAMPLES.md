# Exemplos Práticos - Estendendo o Projeto

Este arquivo contém exemplos práticos de como estender o projeto com a nova estrutura MVC + POM.

---

## Exemplo 1: Adicionar Validação ao Modelo Employee

**Arquivo: `models/employee.py`** (Atualizado)

```python
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Employee:
    """Modelo de dados para representar um funcionário com validação"""
    
    first_name: str
    last_name: str
    email: str
    address: str
    phone_number: str
    company_name: str
    role_in_company: str
    
    @classmethod
    def from_excel_row(cls, row: dict) -> 'Employee':
        """
        Cria uma instância de Employee a partir de uma linha do DataFrame do Excel
        
        Args:
            row: Dicionário contendo os dados da linha
            
        Returns:
            Instância de Employee
        """
        return cls(
            first_name=row.get("First Name", "").strip(),
            last_name=row.get("Last Name ", "").strip(),
            email=row.get("Email", "").strip(),
            address=row.get("Address", "").strip(),
            phone_number=row.get("Phone Number", "").strip(),
            company_name=row.get("Company Name", "").strip(),
            role_in_company=row.get("Role in Company", "").strip()
        )
    
    def is_valid(self) -> bool:
        """Valida se todos os campos obrigatórios estão preenchidos"""
        return all([
            self.first_name,
            self.last_name,
            self.email,
            self.address,
            self.phone_number,
            self.company_name,
            self.role_in_company
        ])
    
    def is_email_valid(self) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.email) is not None
    
    def is_phone_valid(self) -> bool:
        """Valida formato de telefone"""
        # Remove caracteres não numéricos
        phone_digits = re.sub(r'\D', '', self.phone_number)
        # Verifica se tem entre 10 e 15 dígitos
        return 10 <= len(phone_digits) <= 15
    
    def validate_all(self) -> tuple[bool, list[str]]:
        """
        Valida todos os campos e retorna erros
        
        Returns:
            (é_válido, lista_de_erros)
        """
        errors = []
        
        if not self.is_valid():
            errors.append("Campos obrigatórios não preenchidos")
        
        if not self.is_email_valid():
            errors.append(f"Email inválido: {self.email}")
        
        if not self.is_phone_valid():
            errors.append(f"Telefone inválido: {self.phone_number}")
        
        return len(errors) == 0, errors
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


# Exemplo de uso:
if __name__ == "__main__":
    # Válido
    emp1 = Employee(
        first_name="João",
        last_name="Silva",
        email="joao@example.com",
        address="Rua A, 123",
        phone_number="11 9 9999-9999",
        company_name="Tech Corp",
        role_in_company="Developer"
    )
    
    is_valid, errors = emp1.validate_all()
    print(f"Employee 1 válido: {is_valid}")
    
    # Inválido
    emp2 = Employee(
        first_name="Maria",
        last_name="Santos",
        email="maria@invalid",  # Email inválido
        address="Rua B, 456",
        phone_number="123",  # Telefone inválido
        company_name="Tech Corp",
        role_in_company="QA"
    )
    
    is_valid, errors = emp2.validate_all()
    print(f"Employee 2 válido: {is_valid}")
    for error in errors:
        print(f"  - {error}")
```

---

## Exemplo 2: Adicionar Página de Login

**Arquivo: `pages/login_page.py`** (Novo)

```python
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from config.config import config


class LoginPageObject(BasePage):
    """Page Object para página de login"""
    
    @property
    def username_field_xpath(self) -> str:
        return "//input[@id='username']"
    
    @property
    def password_field_xpath(self) -> str:
        return "//input[@id='password']"
    
    @property
    def login_button_xpath(self) -> str:
        return "//button[@type='submit']"
    
    @property
    def error_message_xpath(self) -> str:
        return "//div[@class='error-message']"
    
    def enter_username(self, username: str) -> None:
        """Insere o nome de usuário"""
        self.send_keys_to_element(self.username_field_xpath, username)
    
    def enter_password(self, password: str) -> None:
        """Insere a senha"""
        self.send_keys_to_element(self.password_field_xpath, password)
    
    def click_login(self) -> None:
        """Clica no botão de login"""
        self.click_element_by_xpath(self.login_button_xpath)
    
    def login(self, username: str, password: str) -> None:
        """Realiza login completo"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_error_message(self) -> str:
        """Obtém mensagem de erro se houver"""
        try:
            element = self.find_element_by_xpath(self.error_message_xpath)
            return element.text
        except:
            return ""
    
    def is_login_successful(self) -> bool:
        """Verifica se login foi bem-sucedido"""
        return len(self.get_error_message()) == 0
```

---

## Exemplo 3: Serviço para Operações com Dados

**Arquivo: `services/employee_service.py`** (Novo)

```python
from typing import List
from logging import Logger
import pandas as pd

from models.employee import Employee
from config.config import config


class EmployeeService:
    """Serviço para operações com dados de funcionários"""
    
    def __init__(self, logger: Logger = None):
        self.logger = logger
    
    def load_employees_from_excel(self, file_path: str = None) -> List[Employee]:
        """
        Carrega funcionários do arquivo Excel
        
        Args:
            file_path: Caminho do arquivo (usa padrão se None)
            
        Returns:
            Lista de Employee
        """
        if file_path is None:
            file_path = config.EXCEL_FILE_PATH
        
        if self.logger:
            self.logger.info(f"Carregando funcionários de {file_path}")
        
        df = pd.read_excel(file_path)
        employees = [Employee.from_excel_row(row) for _, row in df.iterrows()]
        
        return employees
    
    def validate_employees(self, employees: List[Employee]) -> tuple[List[Employee], List[dict]]:
        """
        Valida lista de funcionários
        
        Args:
            employees: Lista de Employee
            
        Returns:
            (funcionários_válidos, erros_encontrados)
        """
        valid_employees = []
        errors = []
        
        for idx, emp in enumerate(employees, 1):
            is_valid, validation_errors = emp.validate_all()
            
            if is_valid:
                valid_employees.append(emp)
            else:
                errors.append({
                    "linha": idx,
                    "funcionario": str(emp),
                    "erros": validation_errors
                })
                
                if self.logger:
                    self.logger.warning(f"Funcionário {str(emp)} inválido: {validation_errors}")
        
        return valid_employees, errors
    
    def export_results(self, employees: List[Employee], output_file: str) -> None:
        """
        Exporta resultados para arquivo Excel
        
        Args:
            employees: Lista de Employee
            output_file: Caminho do arquivo de saída
        """
        if self.logger:
            self.logger.info(f"Exportando {len(employees)} funcionários para {output_file}")
        
        data = [
            {
                "First Name": emp.first_name,
                "Last Name": emp.last_name,
                "Email": emp.email,
                "Address": emp.address,
                "Phone Number": emp.phone_number,
                "Company Name": emp.company_name,
                "Role in Company": emp.role_in_company
            }
            for emp in employees
        ]
        
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
```

---

## Exemplo 4: Testes Unitários

**Arquivo: `tests/test_employee.py`** (Novo)

```python
import unittest
from models.employee import Employee


class TestEmployee(unittest.TestCase):
    """Testes para o modelo Employee"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.valid_employee = Employee(
            first_name="João",
            last_name="Silva",
            email="joao@example.com",
            address="Rua A, 123",
            phone_number="11 99999999",
            company_name="Tech Corp",
            role_in_company="Developer"
        )
    
    def test_employee_creation(self):
        """Testa criação de Employee"""
        self.assertEqual(self.valid_employee.first_name, "João")
        self.assertEqual(str(self.valid_employee), "João Silva")
    
    def test_employee_is_valid(self):
        """Testa validação de Employee com todos os campos"""
        self.assertTrue(self.valid_employee.is_valid())
    
    def test_employee_is_invalid_missing_field(self):
        """Testa validação com campo faltando"""
        invalid_emp = Employee(
            first_name="Maria",
            last_name="",  # Campo vazio
            email="maria@example.com",
            address="Rua B, 456",
            phone_number="11 99999999",
            company_name="Tech Corp",
            role_in_company="QA"
        )
        self.assertFalse(invalid_emp.is_valid())
    
    def test_email_validation(self):
        """Testa validação de email"""
        # Email válido
        self.assertTrue(self.valid_employee.is_email_valid())
        
        # Email inválido
        invalid_emp = Employee(
            first_name="Test",
            last_name="User",
            email="invalid-email",
            address="Rua C, 789",
            phone_number="11 99999999",
            company_name="Corp",
            role_in_company="Test"
        )
        self.assertFalse(invalid_emp.is_email_valid())
    
    def test_phone_validation(self):
        """Testa validação de telefone"""
        # Telefone válido
        self.assertTrue(self.valid_employee.is_phone_valid())
        
        # Telefone inválido (muito curto)
        invalid_emp = Employee(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            address="Rua D, 999",
            phone_number="123",  # Muito curto
            company_name="Corp",
            role_in_company="Test"
        )
        self.assertFalse(invalid_emp.is_phone_valid())
    
    def test_from_excel_row(self):
        """Testa criação a partir de linha Excel"""
        row = {
            "First Name": "Maria",
            "Last Name ": "Santos",
            "Email": "maria@example.com",
            "Address": "Rua E, 111",
            "Phone Number": "11 99999999",
            "Company Name": "Tech Corp",
            "Role in Company": "QA"
        }
        
        emp = Employee.from_excel_row(row)
        self.assertEqual(emp.first_name, "Maria")
        self.assertEqual(emp.last_name, "Santos")
        self.assertTrue(emp.is_valid())


if __name__ == '__main__':
    unittest.main()
```

---

## Exemplo 5: Controller Estendido com Validação

**Arquivo: `controllers/rpa_challenge_controller.py`** (Versão Estendida)

```python
# ... imports existentes ...
from services.employee_service import EmployeeService
from exceptions import InvalidDataException


class RpaChallengeController(BrowserService):
    """Controller estendido com validação"""
    
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger
        self.driver: WebDriver = None
        self.page_object: RpaChallengePageObject = None
        self.employees: list[Employee] = []
        self.employee_service = EmployeeService(logger)  # Novo serviço
    
    def execute(self) -> None:
        """Executa com validação aprimorada"""
        try:
            self.logger.info("Iniciando execução do RPA Challenge")
            
            self._initialize_browser()
            self._navigate_to_site()
            self._download_and_prepare_excel()
            self._load_and_validate_employees()  # Nova etapa
            self._process_employee_data()
            
            self.logger.info("Execução concluída com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro durante a execução: {str(e)}")
            raise
        finally:
            self._cleanup()
    
    def _load_and_validate_employees(self) -> None:
        """Carrega e valida funcionários"""
        self.logger.info("Carregando funcionários do Excel")
        
        # Carregar
        self.employees = self.employee_service.load_employees_from_excel()
        self.logger.info(f"Total de funcionários carregados: {len(self.employees)}")
        
        # Validar
        valid_employees, errors = self.employee_service.validate_employees(self.employees)
        
        if errors:
            self.logger.warning(f"Encontrados {len(errors)} funcionários inválidos")
            for error in errors:
                self.logger.warning(f"  Linha {error['linha']}: {error['funcionario']} - {error['erros']}")
        
        self.employees = valid_employees
        self.logger.info(f"Total de funcionários válidos: {len(self.employees)}")
        
        if not self.employees:
            raise InvalidDataException("Nenhum funcionário válido para processar")
```

---

## Exemplo 6: Executando Testes

**Executar testes:**

```bash
# Testar um arquivo específico
python -m unittest tests.test_employee

# Testar tudo
python -m unittest discover tests/

# Testar com mais detalhes
python -m unittest discover tests/ -v

# Testar com pytest (se instalado)
pip install pytest
pytest tests/
pytest tests/ -v
```

---

## Conclusão

Estes exemplos mostram como a arquitetura MVC + POM permite:
- ✅ Fácil adicionar novas features
- ✅ Validação de dados robusta
- ✅ Testes simples e diretos
- ✅ Código bem organizado e profissional
- ✅ Fácil manutenção e escalabilidade
