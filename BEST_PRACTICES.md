# Guia de Boas Práticas - MVC + POM

## Estrutura de Projeto MVC + POM

Este guia fornece exemplos práticos de como trabalhar com a arquitetura MVC + POM implementada no projeto.

---

## 1. Adicionando uma Nova Página

### Exemplo: Adicionar suporte para página de login

**Passo 1:** Criar a classe PageObject em `pages/login_page.py`

```python
from pages.base_page import BasePage

class LoginPageObject(BasePage):
    """Page Object para a página de login"""
    
    @property
    def username_field_xpath(self) -> str:
        return "//input[@id='username']"
    
    @property
    def password_field_xpath(self) -> str:
        return "//input[@id='password']"
    
    @property
    def login_button_xpath(self) -> str:
        return "//button[@id='login-btn']"
    
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
```

---

## 2. Adicionando um Novo Modelo

### Exemplo: Modelo de Usuário para login

**Criar em `models/user.py`:**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """Modelo de dados para usuário"""
    username: str
    password: str
    email: Optional[str] = None
    role: Optional[str] = None
    
    def is_valid(self) -> bool:
        """Valida se o usuário tem dados obrigatórios"""
        return bool(self.username and self.password)
    
    def __str__(self) -> str:
        return f"User({self.username})"
```

---

## 3. Estendendo o Controller

### Exemplo: Adicionar autenticação

**Modificar `controllers/rpa_challenge_controller.py`:**

```python
from pages.login_page import LoginPageObject
from models.user import User

class RpaChallengeController(BrowserService):
    
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger
        self.driver: WebDriver = None
        self.page_object: RpaChallengePageObject = None
        self.login_page: LoginPageObject = None
        self.employees: list[Employee] = []
    
    def execute(self) -> None:
        """Executa com autenticação"""
        try:
            self._initialize_browser()
            
            # Nova etapa: autenticar
            self._authenticate()
            
            self._navigate_to_site()
            self._download_and_prepare_excel()
            self._process_employee_data()
            
        except Exception as e:
            self.logger.error(f"Erro: {str(e)}")
            raise
        finally:
            self._cleanup()
    
    def _authenticate(self) -> None:
        """Autentica o usuário"""
        self.logger.info("Iniciando autenticação")
        self.login_page = LoginPageObject(self.driver)
        
        user = User(username="admin", password="senha123")
        
        if not user.is_valid():
            raise Exception("Credenciais inválidas")
        
        self.login_page.login(user.username, user.password)
        self.logger.info(f"Autenticado como {user}")
```

---

## 4. Padrão de Serviço para Lógica Reutilizável

### Exemplo: Criar serviço para operações comuns

**Criar em `services/data_service.py`:**

```python
from typing import List
import pandas as pd
from models.employee import Employee
from config.config import config

class DataService:
    """Serviço para operações com dados"""
    
    @staticmethod
    def load_employees_from_excel(file_path: str = None) -> List[Employee]:
        """Carrega funcionários do Excel"""
        if file_path is None:
            file_path = config.EXCEL_FILE_PATH
        
        df = pd.read_excel(file_path)
        employees = [Employee.from_excel_row(row) for _, row in df.iterrows()]
        return employees
    
    @staticmethod
    def validate_employees(employees: List[Employee]) -> bool:
        """Valida lista de funcionários"""
        if not employees:
            return False
        
        for emp in employees:
            if not all([emp.first_name, emp.last_name, emp.email]):
                return False
        
        return True
    
    @staticmethod
    def export_results(employees: List[Employee], output_file: str) -> None:
        """Exporta resultados para arquivo"""
        data = [
            {
                "First Name": emp.first_name,
                "Last Name": emp.last_name,
                "Email": emp.email,
                "Company": emp.company_name
            }
            for emp in employees
        ]
        
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
```

**Usar no Controller:**

```python
from services.data_service import DataService

class RpaChallengeController(BrowserService):
    def _load_employees_from_excel(self) -> None:
        """Carrega funcionários usando serviço"""
        self.employees = DataService.load_employees_from_excel()
        
        if not DataService.validate_employees(self.employees):
            raise Exception("Dados de funcionários inválidos")
        
        self.logger.info(f"{len(self.employees)} funcionários carregados")
```

---

## 5. Tratamento de Erros Melhorado

### Criar `exceptions.py` para exceções customizadas:

```python
class RpaException(Exception):
    """Exceção base do projeto"""
    pass

class FileNotDownloadedException(RpaException):
    """Exceção quando arquivo não é baixado"""
    pass

class InvalidDataException(RpaException):
    """Exceção para dados inválidos"""
    pass

class BrowserException(RpaException):
    """Exceção relacionada ao navegador"""
    pass
```

**Usar no Controller:**

```python
from exceptions import FileNotDownloadedException

def _download_and_prepare_excel(self) -> None:
    """Baixa arquivo com tratamento customizado"""
    excluir_arquivo_excel()
    self.page_object.click_download_button()
    time.sleep(config.FILE_DOWNLOAD_WAIT)
    
    if not verificar_se_arquivo_excel_existe():
        raise FileNotDownloadedException(
            f"Arquivo não foi baixado em {config.EXCEL_FILE_PATH}"
        )
    
    self.logger.info("Arquivo Excel baixado com sucesso")
```

---

## 6. Padrão Factory para Criar Controllers

**Criar em `factories/controller_factory.py`:**

```python
from controllers.rpa_challenge_controller import RpaChallengeController
from typing import Type
from logging import Logger

class ControllerFactory:
    """Factory para criar controllers"""
    
    _controllers = {
        'rpa_challenge': RpaChallengeController,
        # Adicionar novos controllers aqui
    }
    
    @staticmethod
    def create(controller_type: str, logger: Logger):
        """Cria uma instância do controller requisitado"""
        controller_class = ControllerFactory._controllers.get(controller_type)
        
        if not controller_class:
            raise ValueError(f"Controller '{controller_type}' não encontrado")
        
        return controller_class(logger)
```

**Usar em `main.py`:**

```python
from factories.controller_factory import ControllerFactory

def main():
    logging = configurar_arquivo_log()
    
    try:
        logging.info("Iniciou Execução")
        
        # Usar factory para criar controller
        controller = ControllerFactory.create('rpa_challenge', logging)
        controller.execute()
        
        logging.info("Terminou Execução")
    except Exception as e:
        logging.error(f"Erro: {str(e)}")
        raise
```

---

## 7. Testes Unitários

### Exemplo: Testar modelo Employee

**Criar em `tests/test_employee.py`:**

```python
import unittest
from models.employee import Employee

class TestEmployee(unittest.TestCase):
    
    def test_employee_creation(self):
        """Testa criação de Employee"""
        emp = Employee(
            first_name="João",
            last_name="Silva",
            email="joao@email.com",
            address="Rua A, 123",
            phone_number="11999999999",
            company_name="Tech Corp",
            role_in_company="Dev"
        )
        
        self.assertEqual(emp.first_name, "João")
        self.assertEqual(str(emp), "João Silva")
    
    def test_employee_from_excel_row(self):
        """Testa criação a partir de linha Excel"""
        row = {
            "First Name": "Maria",
            "Last Name ": "Santos",
            "Email": "maria@email.com",
            "Address": "Rua B, 456",
            "Phone Number": "11988888888",
            "Company Name": "Tech Corp",
            "Role in Company": "QA"
        }
        
        emp = Employee.from_excel_row(row)
        self.assertEqual(emp.first_name, "Maria")

if __name__ == '__main__':
    unittest.main()
```

**Executar testes:**
```bash
python -m unittest discover tests/
```

---

## Checklist de Boas Práticas

- [ ] Cada classe tem uma responsabilidade clara
- [ ] Métodos são pequenos e focados
- [ ] Nomes são descritivos (classes, métodos, variáveis)
- [ ] Código DRY (não repetir lógica)
- [ ] Type hints em todos os métodos
- [ ] Docstrings em classes e métodos públicos
- [ ] Logging em etapas importantes
- [ ] Tratamento de exceções apropriado
- [ ] Testes unitários para lógica crítica
- [ ] Configurações centralizadas em `config.py`

---

## Recursos Úteis

- [Design Patterns em Python](https://refactoring.guru/design-patterns/python)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Type Hints em Python](https://docs.python.org/3/library/typing.html)
- [Unittest Documentation](https://docs.python.org/3/library/unittest.html)
