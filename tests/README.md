# Testes Unitários

Este diretório contém todos os testes unitários do projeto RPA Challenge.

## Estrutura

```
tests/
├── __init__.py                  # Package initialization
├── test_employee.py             # Testes do modelo Employee
├── test_config.py               # Testes da configuração
├── test_pages.py                # Testes das páginas (POM)
└── README.md                    # Este arquivo
```

## Executando Testes

### Executar todos os testes

```bash
python -m unittest discover tests/ -v
```

### Executar um arquivo de testes específico

```bash
python -m unittest tests.test_employee -v
```

### Executar uma classe de testes específica

```bash
python -m unittest tests.test_employee.TestEmployeeCreation -v
```

### Executar um teste específico

```bash
python -m unittest tests.test_employee.TestEmployeeCreation.test_employee_creation_with_valid_data -v
```

### Com pytest (opcional)

```bash
pip install pytest pytest-cov
pytest tests/ -v
pytest tests/ --cov=.  # Com cobertura de código
```

## Cobertura de Testes

### test_employee.py

Testa o modelo `Employee`:

- ✅ Criação com dados válidos
- ✅ Representação em string
- ✅ Criação com campos vazios
- ✅ Conversão de linha Excel
- ✅ Tratamento de chaves ausentes
- ✅ Ignorância de chaves extras
- ✅ Tratamento de espaços em branco
- ✅ Igualdade entre objetos

**Classe de testes:**
- `TestEmployeeCreation` - Testes básicos de criação
- `TestEmployeeFromExcelRow` - Testes de conversão de Excel
- `TestEmployeeEquality` - Testes de igualdade

### test_config.py

Testa a configuração `Config`:

- ✅ Inicialização com atributos necessários
- ✅ Valores padrão corretos
- ✅ Dicionário XPATHS completo
- ✅ Leitura de variáveis de ambiente
- ✅ Fallback para valores padrão
- ✅ Construção de caminhos de arquivo
- ✅ Conversão de tipos (string → int)
- ✅ Validação de valores inválidos

**Classe de testes:**
- `TestConfigInitialization` - Testes de inicialização
- `TestConfigEnvironmentVariables` - Testes de variáveis de ambiente
- `TestConfigFilePathConstruction` - Testes de construção de caminhos
- `TestConfigTypeConversion` - Testes de conversão de tipos

### test_pages.py

Testa o Page Object Model (POM):

- ✅ Inicialização de BasePage
- ✅ Configuração de WebDriverWait
- ✅ Propriedades de XPath
- ✅ Métodos de ação
- ✅ Integração de fill_employee_form
- ✅ Mocking de Selenium

**Classe de testes:**
- `TestBasePageInitialization` - Testes de BasePage
- `TestRpaChallengePageObjectProperties` - Testes de propriedades
- `TestRpaChallengePageObjectMethods` - Testes de métodos
- `TestRpaChallengePageObjectIntegration` - Testes de integração

## Exemplo de Execução

```bash
# Executar todos os testes com verbose
python -m unittest discover tests/ -v

# Saída esperada:
# test_employee_creation_with_valid_data (tests.test_employee.TestEmployeeCreation) ... ok
# test_employee_string_representation (tests.test_employee.TestEmployeeCreation) ... ok
# test_from_excel_row_with_valid_data (tests.test_employee.TestEmployeeFromExcelRow) ... ok
# ...
# Ran 30 tests in 0.234s
# OK
```

## Escrevendo Novos Testes

### Template básico

```python
import unittest
from seu_modulo import SuaClasse

class TestSuaClasse(unittest.TestCase):
    """Descrição dos testes"""
    
    def setUp(self):
        """Executado antes de cada teste"""
        self.objeto = SuaClasse()
    
    def tearDown(self):
        """Executado após cada teste"""
        pass
    
    def test_algo_importante(self):
        """Testa se algo funciona"""
        resultado = self.objeto.fazer_algo()
        self.assertEqual(resultado, valor_esperado)

if __name__ == "__main__":
    unittest.main()
```

### Boas práticas

1. **Nomes descritivos**: `test_user_creation_with_valid_email`
2. **Uma assertion por teste** (geralmente)
3. **Usar setUp/tearDown** para inicialização/limpeza
4. **Mockar dependências externas** (Selenium, banco de dados, APIs)
5. **Testar casos normais e edge cases**
6. **Documentar com docstrings**

## Mocking

### Mock de WebDriver

```python
from unittest.mock import Mock
from selenium.webdriver.remote.webdriver import WebDriver

mock_driver = Mock(spec=WebDriver)
mock_driver.get.assert_called_once_with("url")
```

### Patch de variáveis de ambiente

```python
from unittest.mock import patch
import os

@patch.dict(os.environ, {"VAR": "value"})
def test_com_env_var(self):
    # Testa com VAR = "value"
    pass
```

### Patch de métodos

```python
with patch.object(self.page, "send_keys_to_element") as mock_method:
    self.page.fill_first_name("João")
    mock_method.assert_called_once()
```

## Cobertura de Código

### Gerar relatório de cobertura

```bash
pip install coverage
coverage run -m unittest discover tests/
coverage report
coverage html  # Gera relatório HTML
```

## Continuous Integration

Para integrar os testes com CI/CD (GitHub Actions, GitLab CI, etc):

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
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: python -m unittest discover tests/ -v
```

## Troubleshooting

### ImportError ao executar testes

```bash
# Adicione o diretório raiz ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m unittest discover tests/ -v
```

### Testes encontram variáveis .env diferentes

```python
# Use patch para garantir ambiente consistente
@patch.dict(os.environ, {}, clear=True)
def test_com_env_limpo(self):
    pass
```

## Próximos Passos

- [ ] Adicionar testes para `RpaChallengeController`
- [ ] Adicionar testes de integração end-to-end
- [ ] Configurar CI/CD pipeline
- [ ] Atingir 80%+ cobertura de código
- [ ] Testes de performance
- [ ] Testes com banco de dados (se aplicável)

---

**Última atualização**: 2026-07-08  
**Status**: ✅ Testes implementados
