# RPA Challenge
 
Projeto para realizar o desafio RPA Challenge com Python.
 
 
![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=status&message=em%20desenvolvimento&color=GREEN&s…)
 
![Badge Python Version](http://img.shields.io/static/v1?label=python&message=3.11.5&color=blue&style=fill)
 
 
 
 
##                   BOAS PRÁTICAS UTILIZADAS DO SELENIUM                        
* [Confira aqui!](https://www.selenium.dev/pt-br/documentation/)
 
 
## Estrutura do projeto (MVC + POM)
```
 
    ├── config/                                        # Configurações centralizadas da aplicação
    │   └── config.py                                  # Variáveis de ambiente, URLs, XPaths e timeouts
    │
    ├── models/                                        # Camada Model - Definição de dados
    │   └── employee.py                                # Modelo de dados para representar um funcionário
    │
    ├── pages/                                         # Page Object Model - Abstração de elementos UI
    │   ├── base_page.py                               # Classe base com métodos comuns para interação
    │   └── rpa_challenge_page.py                      # Page Object para o site RPA Challenge
    │
    ├── controllers/                                   # Camada Controller - Lógica de negócio
    │   └── rpa_challenge_controller.py                # Controller que orquestra o fluxo da aplicação
    │
    ├── services/                                      # Serviços de suporte
    │   ├── browser_service.py                         # Gerenciamento do Selenium WebDriver
    │
    ├── helpers/                                       # Utilitários auxiliares
    │   ├── tratar_erro_helper.py                      # Tratamento de erros e captura de screenshots
    │   ├── criar_arquivo_log_helper.py                # Configuração de logging
    │   ├── excel_helper.py                            # Operações com arquivos Excel
    │
    ├── main.py                                        # Ponto de entrada da aplicação
    ├── requirements.txt                               # Dependências do projeto
    └── README.md                                      # Este arquivo
```

## Padrões de Arquitetura Utilizados

### MVC (Model-View-Controller)
- **Model**: Camada de dados (`models/`) - Define a estrutura de dados (Employee)
- **View**: Camada de apresentação (`pages/`) - Abstrações da interface de usuário (POM)
- **Controller**: Camada de lógica de negócio (`controllers/`) - Orquestra o fluxo da aplicação

### POM (Page Object Model)
- **BasePage**: Classe base com métodos reutilizáveis de interação com elementos
- **RpaChallengePageObject**: Implementação específica para a página do RPA Challenge
- Centraliza todos os XPaths e métodos de interação na página em uma única classe
- Facilita manutenção quando elementos da página mudam

## Como Adicionar Novas Páginas

Para adicionar uma nova página ao projeto:

1. **Criar uma classe que herda de BasePage** em `pages/`:
```python
from pages.base_page import BasePage

class NovaPageObject(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    # Adicionar métodos específicos da página
```

2. **Importar e usar no controller**:
```python
from pages.nova_page import NovaPageObject

page = NovaPageObject(self.driver)
page.seu_metodo()
```

## Como Adicionar Novos Modelos

Para criar um novo modelo de dados:

```python
from dataclasses import dataclass

@dataclass
class NovoModelo:
    campo1: str
    campo2: int
```

## Como Criar um Novo Controller

Para criar um novo fluxo de automação:

1. Herde de `BrowserService`
2. Use injeção de dependência para Logger
3. Implemente os métodos de seu fluxo
4. Chame a partir de `main.py`
## Configuração de Ambiente
- Realize o download e instação do [Python 3.12.3](https://www.python.org/downloads/release/python-3115/)
#### OBS.: Para evitar problemas de compatibilidade, desinstale qualquer versão anterior do python.
 
 
Para realizar a instalação do python na versão do projeto, acesse:
 
- B3Store
 
#
- Após a instalação, verifique se as variáveis de ambiente foram configuradas corretamente. Para isso, basta executar o comando abaixo no terminal para visualizar a versão do python:
```
python --version
```
- O resultado deve ser algo como:
```
Python 3.12.3
```
- Agora verifique se o pip, gerenciador de pacotes do Python, foi instalado corretamente:
```
pip --version
```
- O resultado deve ser algo como:
```
pip 23.2.1 from C:\Program Files\Python311\Lib\site-packages\pip (python 3.12)
```
 
```
pip install -r requirements.txt
```
##
## Editor de texto
Como editor de texto, a sugestão Visual Studio Code, porém você pode utilizar seu favorito.
Caso opte pelo Visual Studio Code, [clique aqui](https://code.visualstudio.com/download) e realize o downlaod e instalação pelo link.
- Para melhor utilização, recomenda-se a instalação das seguintes extensões:
 
| Extensão                   | Função       |
| ---------------            | -------------|
| Path Intellisense          | Auxilia no autocomplete ao inserir caminhos de arquivos e pastas no código.                     |
| Material Icon Theme        | Altera os ícones de arquivos de acordo com a extensão.                                          |
| Black Formatter                 | Auxilia na formatação dos arquivos Python de acordo com o [PEP8](https://peps.python.org/pep-0008/)    |
 
----
## Executando o robô
 Para realizar a execução do robô, utilize o comando:
```
python main.py
```

## Testes Unitários

O projeto possui uma suite completa de **29 testes unitários** cobrindo todos os componentes críticos.

### Executar todos os testes

```bash
python -m unittest discover tests/ -v
```

**Resultado esperado:**
```
Ran 29 tests in 0.063s
OK
```

### Para mais detalhes sobre testes

- Consulte [TESTING.md](TESTING.md) - Guia completo de testes
- Consulte [tests/README.md](tests/README.md) - Documentação dos testes

### Cobertura

- ✅ Modelo Employee: criação, conversão Excel, igualdade
- ✅ Configuração: ambiente, variáveis, caminhos
- ✅ Page Object Model: inicialização, XPaths, métodos
 
## Autores
 
- Silas da Silva Salema