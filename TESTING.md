# Guia de Testes - RPA Challenge

## 📊 Resumo de Testes

O projeto possui uma suite completa de testes unitários com **29 testes** cobrindo:

- ✅ Modelo de dados (Employee)
- ✅ Configuração (Config)
- ✅ Page Object Model (Pages)

**Status**: ✅ **Todos os testes passando**

---

## 🚀 Executando Testes

### Método 1: unittest (nativo do Python)

```bash
# Executar todos os testes com verbose
python -m unittest discover tests/ -v

# Executar um arquivo específico
python -m unittest tests.test_employee -v

# Executar uma classe específica
python -m unittest tests.test_employee.TestEmployeeCreation -v

# Executar um teste específico
python -m unittest tests.test_employee.TestEmployeeCreation.test_employee_creation_with_valid_data -v
```

### Método 2: pytest (opcional)

```bash
# Instalar pytest
pip install pytest pytest-cov

# Executar testes
pytest tests/ -v

# Com cobertura de código
pytest tests/ --cov=. --cov-report=html
```

---

## 📋 Estrutura de Testes

```
tests/
├── __init__.py
├── test_employee.py          # 11 testes
├── test_config.py            # 9 testes
├── test_pages.py             # 9 testes
└── README.md                 # Documentação completa
```

---

## 🧪 Cobertura Detalhada

### test_employee.py (11 testes)

Testa o modelo `Employee` com validação de dados:

#### TestEmployeeCreation
- ✅ Criação com dados válidos
- ✅ Representação em string (`__str__`)
- ✅ Criação com campos vazios

#### TestEmployeeFromExcelRow
- ✅ Conversão de linha Excel com dados válidos
- ✅ Tratamento de chaves ausentes (fallback para "")
- ✅ Ignorância de chaves extras
- ✅ Preservação de espaços em branco

#### TestEmployeeEquality
- ✅ Igualdade entre dois Employees com mesmos dados
- ✅ Desigualdade entre Employees diferentes

### test_config.py (9 testes)

Testa a configuração centralizada:

#### TestConfigInitialization
- ✅ Presença de todos os atributos necessários
- ✅ Valores padrão corretos
- ✅ Dicionário XPATHS completo (10 chaves)

#### TestConfigEnvironmentVariables
- ✅ Leitura de variáveis de ambiente
- ✅ Fallback para valores padrão

#### TestConfigFilePathConstruction
- ✅ Construção correta de EXCEL_FILE_PATH
- ✅ Nome padrão do arquivo Excel

#### TestConfigTypeConversion
- ✅ Conversão de timeout (string → int)
- ✅ Validação de valores inválidos (raises ValueError)

### test_pages.py (9 testes)

Testa o Page Object Model:

#### TestBasePageInitialization
- ✅ Inicialização de BasePage
- ✅ Configuração de WebDriverWait

#### TestRpaChallengePageObjectProperties
- ✅ Presença de todas as propriedades de XPath (10)
- ✅ XPaths vêm da configuração

#### TestRpaChallengePageObjectMethods
- ✅ Presença de todos os métodos de ação (12)
- ✅ Métodos chamam Selenium corretamente (mocked)

#### TestRpaChallengePageObjectIntegration
- ✅ `fill_employee_form()` chama todos os métodos de preenchimento

---

## 📈 Resultado de Execução

```
Ran 29 tests in 0.063s
OK

✅ Todos os testes passaram!
```

---

## 🔍 Exemplo de Execução

```bash
$ python -m unittest discover tests/ -v

test_config_reads_environment_variables ... ok
test_config_uses_defaults_when_env_not_set ... ok
test_excel_file_name_default ... ok
test_excel_file_path_construction ... ok
test_config_default_values ... ok
test_config_has_required_attributes ... ok
test_config_xpaths_dictionary ... ok
test_invalid_timeout_raises_error ... ok
test_timeout_values_are_integers ... ok
test_employee_creation_with_valid_data ... ok
test_employee_string_representation ... ok
test_employee_with_empty_fields ... ok
test_employees_with_different_data_are_not_equal ... ok
test_employees_with_same_data_are_equal ... ok
test_from_excel_row_with_extra_keys ... ok
test_from_excel_row_with_missing_keys ... ok
test_from_excel_row_with_valid_data ... ok
test_from_excel_row_with_whitespace ... ok
test_base_page_has_wait_timeout ... ok
test_base_page_initialization ... ok
test_fill_employee_form_calls_all_fill_methods ... ok
test_fill_address_calls_send_keys ... ok
test_fill_email_calls_send_keys ... ok
test_fill_first_name_calls_send_keys ... ok
test_fill_last_name_calls_send_keys ... ok
test_navigate_to_rpa_challenge_calls_driver ... ok
test_page_has_action_methods ... ok
test_page_has_all_xpath_properties ... ok
test_xpaths_are_from_config ... ok

Ran 29 tests in 0.063s

OK
```

---

## 💡 Técnicas Usadas

### 1. Mocking

Simulação de dependências (Selenium WebDriver):

```python
from unittest.mock import Mock
from selenium.webdriver.remote.webdriver import WebDriver

mock_driver = Mock(spec=WebDriver)
page = RpaChallengePageObject(mock_driver)
```

### 2. Patch de Variáveis de Ambiente

Teste com variáveis de ambiente customizadas:

```python
@patch.dict(os.environ, {"VAR": "value"})
def test_com_env(self):
    # Teste com VAR configurada
    pass
```

### 3. Patch de Métodos

Mockar métodos específicos:

```python
with patch.object(self.page, "send_keys_to_element") as mock:
    self.page.fill_first_name("João")
    mock.assert_called_once()
```

---

## ✍️ Escrevendo Novos Testes

### Template Base

```python
import unittest

class TestMeuComponente(unittest.TestCase):
    """Testes para meu componente"""
    
    def setUp(self):
        """Executado antes de cada teste"""
        self.componente = MeuComponente()
    
    def test_comportamento_importante(self):
        """Descrição clara do que está sendo testado"""
        resultado = self.componente.fazer_algo()
        self.assertEqual(resultado, valor_esperado)
    
    def tearDown(self):
        """Limpeza após teste (opcional)"""
        pass

if __name__ == "__main__":
    unittest.main()
```

### Boas Práticas

1. **Nomes descritivos**: `test_employee_creation_with_valid_email`
2. **Uma coisa por teste**: Testa um comportamento específico
3. **Dado-Quando-Então**:
   ```python
   # Dado
   emp = Employee(...)
   
   # Quando
   resultado = str(emp)
   
   # Então
   self.assertEqual(resultado, "João Silva")
   ```
4. **Use setUp/tearDown** para inicialização/limpeza
5. **Mockar coisas externas** (WebDriver, APIs, etc)
6. **Testar casos normais e edge cases**

---

## 🔗 Integração Contínua

### GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python -m unittest discover tests/ -v
```

---

## 📊 Próximos Passos

- [ ] Adicionar testes para `RpaChallengeController`
- [ ] Testes de integração end-to-end
- [ ] Cobertura de código (target: 80%+)
- [ ] Testes de performance
- [ ] Testes com dados reais (fixtures)
- [ ] Testes de tratamento de erros

---

## 📚 Recursos

- [unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Selenium Testing Guide](https://www.selenium.dev/documentation/webdriver/testing/)

---

**Última atualização**: 2026-07-08  
**Total de testes**: 29  
**Status**: ✅ Todos passando
