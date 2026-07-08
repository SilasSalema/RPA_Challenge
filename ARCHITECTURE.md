# Diagrama de Arquitetura MVC + POM

## Fluxo da Aplicação

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                 │
│          (Ponto de entrada da aplicação)                        │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              RpaChallengeController                             │
│              (Camada Controller - Lógica)                       │
│                                                                 │
│  • execute()                                                    │
│  • _initialize_browser()                                        │
│  • _navigate_to_site()                                          │
│  • _download_and_prepare_excel()                                │
│  • _process_employee_data()                                     │
│  • _cleanup()                                                   │
└────────────┬──────────────────────────┬──────────────────────────┘
             │                          │
             ▼                          ▼
    ┌──────────────────┐      ┌─────────────────────┐
    │ BrowserService   │      │ RpaChallengePageObj │
    │  (Service)       │      │     (View - POM)    │
    │                  │      │                     │
    │ • abrir_navegador│      │ • fill_first_name   │
    │ • fechar_navegador│     │ • fill_last_name    │
    │ • maximizar_janela│     │ • fill_employee_    │
    │                  │      │   form()            │
    └──────────────────┘      │ • click_download_   │
                              │   button()          │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   BasePage           │
                              │  (Base para POM)     │
                              │                      │
                              │ • find_element()     │
                              │ • click_element()    │
                              │ • send_keys()        │
                              └──────────────────────┘

             ▼                          ▼
    ┌──────────────────┐      ┌──────────────────────┐
    │   Config         │      │    Employee (Model)  │
    │  (Configurações) │      │  (Camada Model)      │
    │                  │      │                      │
    │ • XPATHS         │      │ • first_name         │
    │ • URLs           │      │ • last_name          │
    │ • TIMEOUTS       │      │ • email              │
    │ • PATHS          │      │ • from_excel_row()   │
    └──────────────────┘      └──────────────────────┘

             ▼                          ▼
    ┌──────────────────┐      ┌──────────────────────┐
    │   Helpers        │      │   Services (Data)    │
    │ (Utilidades)     │      │  (Lógica de dados)   │
    │                  │      │                      │
    │ • excel_helper   │      │ • load_employees()   │
    │ • error_helper   │      │ • validate()         │
    │ • log_helper     │      │ • export_results()   │
    └──────────────────┘      └──────────────────────┘
```

## Separação de Responsabilidades

```
┌────────────────────────────────────────────────────────────────┐
│                    ARQUITETURA MVC + POM                       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  MODEL (Camada de Dados)                                 │ │
│  │  └─> models/employee.py                                  │ │
│  │      • Define estrutura de dados                         │ │
│  │      • Validação de dados                                │ │
│  │      • Transformação de dados                            │ │
│  └─────────────────────────────────────────────────────────┘ │
│                            △                                  │
│                            │                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  VIEW (Camada de Apresentação - POM)                     │ │
│  │  └─> pages/                                              │ │
│  │      ├─ base_page.py (Métodos comuns)                    │ │
│  │      └─ rpa_challenge_page.py (Específico)               │ │
│  │      • Abstrai elementos HTML                            │ │
│  │      • Centraliza XPaths                                 │ │
│  │      • Métodos de interação                              │ │
│  │      • Sem lógica de negócio                             │ │
│  └─────────────────────────────────────────────────────────┘ │
│                            △                                  │
│                            │                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  CONTROLLER (Camada de Lógica de Negócio)               │ │
│  │  └─> controllers/rpa_challenge_controller.py            │ │
│  │      • Orquestra o fluxo                                 │ │
│  │      • Coordena Model e View                             │ │
│  │      • Implementa regras de negócio                      │ │
│  │      • Tratamento de erros                               │ │
│  │      • Logging                                           │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                │
│  SUPORTE:                                                      │
│  ├─> config/config.py (Configurações centralizadas)           │
│  ├─> services/ (Serviços auxiliares)                          │
│  ├─> helpers/ (Funções utilitárias)                           │
│  └─> factories/ (Padrão Factory - Opcional)                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUXO DE EXECUÇÃO COMPLETO                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. main.py                                                     │
│     └─> Inicia Logger                                           │
│     └─> Cria RpaChallengeController                             │
│                                                                 │
│  2. RpaChallengeController.execute()                            │
│     ├─> _initialize_browser()                                   │
│     │   └─> Cria WebDriver (BrowserService)                     │
│     │   └─> Cria RpaChallengePageObject                         │
│     │                                                           │
│     ├─> _navigate_to_site()                                     │
│     │   └─> PageObject.navigate_to_rpa_challenge()              │
│     │       └─> driver.get(config.RPA_CHALLENGE_URL)            │
│     │                                                           │
│     ├─> _download_and_prepare_excel()                           │
│     │   ├─> excluir_arquivo_excel() [Helper]                    │
│     │   ├─> PageObject.click_download_button()                  │
│     │   └─> verificar_se_arquivo_excel_existe() [Helper]        │
│     │                                                           │
│     ├─> _load_employees_from_excel()                            │
│     │   ├─> obter_data_frame_do_arquivo_excel() [Helper]        │
│     │   └─> Employee.from_excel_row() [Model]                   │
│     │       └─> Cria lista de Employee                          │
│     │                                                           │
│     ├─> _process_employee_data()                                │
│     │   ├─> PageObject.click_start_button()                     │
│     │   └─> Para cada Employee:                                 │
│     │       ├─> PageObject.fill_employee_form(employee)         │
│     │       │   ├─> fill_first_name()                           │
│     │       │   ├─> fill_last_name()                            │
│     │       │   ├─> fill_email()                                │
│     │       │   └─> ... (outros campos)                         │
│     │       └─> PageObject.click_submit_button()                │
│     │                                                           │
│     └─> _cleanup()                                              │
│         └─> BrowserService.fechar_navegador()                   │
│             └─> driver.quit()                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Interação entre Componentes

```
┌──────────┐
│ main.py  │
└────┬─────┘
     │ cria
     ▼
┌─────────────────────────┐
│ RpaChallengeController  │ extends BrowserService
└──────────┬──────────────┘
     │
     ├─ usa ────────────────► RpaChallengePageObject
     │                        extends BasePage
     │
     ├─ carrega ────────────► Employee (Model)
     │                        from_excel_row()
     │
     ├─ lê config ──────────► config.py
     │                        XPATHS, URLs, TIMEOUTS
     │
     └─ usa helpers ────────► excel_helper.py
                             error_helper.py
                             log_helper.py
```

## Estrutura de Page Objects Atual

```
pages/
├─ base_page.py (métodos genéricos)
│  ├─ click_element_by_xpath()
│  ├─ send_keys_to_element()
│  └─ find_element_by_xpath()
│
├─ rpa_challenge_page.py (específico do site RPA Challenge)
│  ├─ fill_employee_form()
│  ├─ click_download_button()
│  └─ ... (métodos de negócio)
│
└─ (Adicionar nova_pagina_page.py conforme necessário)
```

## Stack Tecnológico

```
┌─────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Linguagem:      Python 3.11+                           │
│  Framework Web:  Selenium 4.35.0                        │
│  Processamento:  Pandas 2.3.2                           │
│  Dados:          openpyxl 3.1.5 (Excel)                 │
│  Banco (opcional): pyodbc 5.2.0                         │
│  Padrões:        MVC + POM                              │
│  Logging:        logging (Python built-in)              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```
