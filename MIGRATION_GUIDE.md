# Guia de Estrutura - MVC + POM

A documentação a seguir descreve a estrutura atual do projeto que implementa os padrões MVC (Model-View-Controller) e POM (Page Object Model).

## Estrutura Atual

```
main.py
├── RpaChallengeController (Controller)
    ├── RpaChallengePageObject (View - POM)
    │   └── BasePage
    ├── Employee (Model)
    ├── BrowserService (Service)
    └── Excel/Log Helpers (Utilities)

config/
└── config.py (Configurações centralizadas)

models/
└── employee.py (Estrutura de dados)

pages/ (Page Object Model)
├── base_page.py
└── rpa_challenge_page.py

controllers/
└── rpa_challenge_controller.py
```

---

## Como Usar a Nova Estrutura

### Executar o projeto:
```bash
python main.py
```

O fluxo agora é:
1. `main.py` chama `RpaChallengeController`
2. Controller cria instância de `RpaChallengePageObject`
3. PageObject abstrai os elementos e ações da página
4. Model (`Employee`) estrutura os dados
5. `config.py` centraliza configurações

---

## Próximos Passos Recomendados

1. **Adicionar testes unitários** para Models e Controllers
2. **Criar mais PageObjects** se houver outras páginas
3. **Implementar padrão Strategy** se houver múltiplos tipos de processamento
4. **Adicionar validações** no Model
5. **Documentar métodos** com docstrings detalhadas

---

## Referências

- [POM - Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [MVC Architecture](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
- [Python Design Patterns](https://refactoring.guru/design-patterns/python)
