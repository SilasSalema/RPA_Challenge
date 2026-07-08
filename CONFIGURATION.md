# 📋 Guia de Configuração do Projeto

## Visão Geral

O projeto utiliza um sistema de configuração centralizado que carrega variáveis do arquivo `.env` (variáveis de ambiente locais) com valores padrão como fallback.

### Ordem de Prioridade

1. **Variáveis de Ambiente do SO** (maior prioridade)
2. **Arquivo `.env`** (local ou na raiz do projeto)
3. **Valores Padrão** em `config/config.py` (menor prioridade)

---

## Como Configurar

### 1️⃣ Usando o Arquivo `.env`

**Método mais recomendado para desenvolvimento local:**

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite as variáveis conforme necessário
```

### 2️⃣ Usando Variáveis de Ambiente do SO

**Para CI/CD ou deployment:**

#### Windows (PowerShell)
```powershell
$env:Environment = "docker"
$env:Browser = "chrome"
$env:Remote_Url = "http://selenium-hub:4444/wd/hub"
```

#### Windows (CMD)
```cmd
set Environment=docker
set Browser=chrome
set Remote_Url=http://selenium-hub:4444/wd/hub
```

#### Linux/Mac (Bash)
```bash
export Environment=docker
export Browser=chrome
export Remote_Url=http://selenium-hub:4444/wd/hub
```

#### Docker (no docker-compose.yml)
```yaml
services:
  app:
    environment:
      - Environment=docker
      - Browser=chrome
      - Remote_Url=http://selenium-hub:4444/wd/hub
```

---

## Variáveis Disponíveis

### URLs
```env
# URL do site RPA Challenge
RPA_CHALLENGE_URL=https://rpachallenge.com/
```

### Paths (Diretórios)
```env
# Diretório para download de arquivos
Caminho_Pasta_Downloads=./downloads/teste

# Diretório para evidências (screenshots)
caminho_evidencias=./logs
```

### Browser
```env
# Ambiente: local, docker ou remote
Environment=docker

# Browser: chrome ou firefox
Browser=chrome

# URL do Selenium Hub
Remote_Url=http://selenium-hub:4444/wd/hub
```

### Files
```env
# Nome do arquivo Excel
Excel_File_Name=challenge.xlsx
```

### Timeouts (em segundos)
```env
# Espera para elementos aparecerem
Default_Wait_Time=60

# Espera para download de arquivos
File_Download_Wait=5
```

### XPaths (Opcionais)
```env
# Se os XPaths mudarem no site, descomente e modifique:
# XPATH_download_button=...
# XPATH_start_button=...
# XPATH_first_name=...
# etc.
```

---

## Exemplos de Configuração

### 🏠 Ambiente Local (Desenvolvimento)

**`.env`:**
```env
Environment=local
Browser=chrome
Remote_Url=http://localhost:4444
Caminho_Pasta_Downloads=./downloads
caminho_evidencias=./logs
Default_Wait_Time=60
File_Download_Wait=5
```

### 🐳 Ambiente Docker

**`.env`:**
```env
Environment=docker
Browser=chrome
Remote_Url=http://selenium-hub:4444/wd/hub
Caminho_Pasta_Downloads=./downloads/teste
caminho_evidencias=./logs
Default_Wait_Time=60
File_Download_Wait=5
```

**`docker-compose.yml`:**
```yaml
services:
  app:
    environment:
      - Environment=docker
      - Browser=chrome
      - Remote_Url=http://selenium-hub:4444/wd/hub
```

### ☁️ Ambiente Remote/Cloud

**`.env`:**
```env
Environment=remote
Browser=chrome
Remote_Url=https://seu-provider-cloud.com/wd/hub
Caminho_Pasta_Downloads=/home/user/downloads
caminho_evidencias=/home/user/logs
Default_Wait_Time=120
File_Download_Wait=10
```

### 🔧 Ambiente CI/CD (GitHub Actions)

**`.github/workflows/main.yml`:**
```yaml
name: RPA Tests
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    env:
      Environment: docker
      Browser: chrome
      Remote_Url: http://localhost:4444/wd/hub
    steps:
      - uses: actions/checkout@v2
      - name: Run RPA
        run: python main.py
```

---

## Como Usar em Código

### Acessar Configurações

```python
from config.config import config

# Acessar variáveis
print(config.RPA_CHALLENGE_URL)
print(config.ENVIRONMENT)
print(config.DEFAULT_WAIT_TIME)
print(config.XPATHS["download_button"])
```

### Exemplo: Controller com Configurações

```python
from config.config import config
from logging import Logger

class RpaChallengeController(BrowserService):
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger
        self.default_timeout = config.DEFAULT_WAIT_TIME
        self.download_timeout = config.FILE_DOWNLOAD_WAIT
        
    def _navigate_to_site(self) -> None:
        self.logger.info(f"Navegando para {config.RPA_CHALLENGE_URL}")
        self.page_object.navigate_to(config.RPA_CHALLENGE_URL)
```

---

## Valores Padrão

Se nenhuma variável for definida, os seguintes padrões são usados:

| Variável | Padrão |
|----------|--------|
| `RPA_CHALLENGE_URL` | `https://rpachallenge.com/` |
| `Caminho_Pasta_Downloads` | `./downloads` |
| `caminho_evidencias` | `./logs` |
| `Remote_Url` | `http://selenium-hub:4444/wd/hub` |
| `Environment` | `local` |
| `Browser` | `chrome` |
| `Excel_File_Name` | `challenge.xlsx` |
| `Default_Wait_Time` | `60` |
| `File_Download_Wait` | `5` |

---

## Verificar Configurações Carregadas

Para verificar quais variáveis foram carregadas:

```python
# No terminal Python
from config.config import config

# Ver todas as configurações
print(f"Environment: {config.ENVIRONMENT}")
print(f"Browser: {config.BROWSER}")
print(f"Remote URL: {config.REMOTE_URL}")
print(f"Download Path: {config.DOWNLOAD_PATH}")
print(f"Default Wait: {config.DEFAULT_WAIT_TIME}")
print(f"XPaths: {list(config.XPATHS.keys())}")
```

Ou execute:
```bash
python -c "from config.config import config; print(f'Environment: {config.ENVIRONMENT}\nBrowser: {config.BROWSER}')"
```

---

## Dicas de Segurança

### ⚠️ Nunca Commitar `.env`

```bash
# Adicione ao .gitignore (já deve estar)
echo ".env" >> .gitignore

# Verifique se .env está ignorado
git check-ignore .env
```

### ✅ Use `.env.example`

O arquivo `.env.example` é usado como referência:
```bash
# Sempre versione o .env.example
git add .env.example
git add .gitignore

# Nunca versione o .env
git add .env  # ❌ ERRADO
```

### 🔐 Dados Sensíveis

Para informações sensíveis (senhas, tokens):
1. Não adicione no `.env`
2. Use variáveis de ambiente do SO
3. Use gerenciador de secrets (Vault, 1Password, etc)

```bash
# ❌ ERRADO - No .env
DATABASE_PASSWORD=minha_senha_123

# ✅ CORRETO - No SO ou Secret Manager
export DATABASE_PASSWORD="minha_senha_123"
```

---

## Troubleshooting

### Variável não está sendo carregada

**Problema:** Configuração não está sendo aplicada

**Solução:**
1. Verifique se o arquivo `.env` está na raiz do projeto
2. Reinicie o aplicativo (Python recarrega variáveis ao iniciar)
3. Verifique a sintaxe do `.env` (sem espaços extras)

```env
# ❌ ERRADO
Environment = docker
Download_Path = ./downloads

# ✅ CORRETO
Environment=docker
Caminho_Pasta_Downloads=./downloads
```

### Valores com Espaços

```env
# Se o valor contém espaços, use aspas
Caminho_Pasta_Downloads="/path/with spaces/downloads"
```

### Variáveis Não Encontradas

Se receber erro de variável não encontrada:

```python
# ✅ Sempre use com fallback
valor = os.getenv("VARIAVEL", "valor_padrao")
```

---

## Próximas Ações

1. ✅ Copie `.env.example` para `.env`
2. ✅ Customize as variáveis para seu ambiente
3. ✅ Adicione `.env` ao `.gitignore`
4. ✅ Teste com: `python main.py`
5. ✅ Verifique logs para confirmar configuração

---

## Referência Completa de Variáveis

Veja [.env.example](.env.example) para lista completa com comentários detalhados.
