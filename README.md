# Ozoneteck API

Automação de compras e consultas dentro do portal Ozonteck utilizando FastAPI e Playwright. A API encapsula as ações executadas via navegador (login, seleção de estado/centro, busca de produtos e finalização de pedidos) e expõe rotas REST simples para integrações externas.

## Tecnologias principais

- **FastAPI / Uvicorn**: servidor HTTP assíncrono que expõe as rotas em `app.py`.
- **Playwright (Chromium)**: controle do navegador persistente configurado em `core/webscraper.py`.
- **Pydantic**: validação dos payloads recebidos nas rotas.
- **python-dotenv**: leitura de credenciais e URL base em `.env`.
- **Pytest**: suíte de testes em `tests/test_scraper.py`.

## Requisitos

- Python 3.10+
- Google Chrome/Chromium disponível (Playwright instala um runtime dedicado)
- Conta válida no portal Ozonteck

## Configuração do ambiente

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Renan-RodriguesDEV/ozonteck.git
   cd ozonteck
   ```
2. **Crie e ative um ambiente virtual (opcional, porém recomendado)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
   ```
3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
4. **Configure variáveis de ambiente** (`.env` na raiz):
   ```ini
   URL_BASE="https://office.grupoozonteck.com/"
   LOGIN="seu_usuario"
   SENHA="sua_senha"
   ```
   > Os dados de sessão do Playwright são salvos automaticamente em `data/<LOGIN>/`, permitindo reaproveitar cookies entre execuções.

## Execução da API

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Em Windows o arquivo `app.py` já força `asyncio.WindowsProactorEventLoopPolicy` para permitir que o Playwright crie subprocessos nas threads utilizadas pelo FastAPI.

## Endpoints

| Método | Rota         | Corpo esperado                                                          | Descrição                                      |
| ------ | ------------ | ----------------------------------------------------------------------- | ---------------------------------------------- |
| GET    | `/states`    | —                                                                       | Lista fixa dos estados aceitos pela plataforma |
| POST   | `/centers/`  | `{ "username", "password", "state" }`                                   | Retorna os centros disponíveis para o estado   |
| POST   | `/search/`   | `{ "username", "password", "state", "center", "product", "quantity"? }` | Seleciona um centro e busca/adiciona produtos  |
| POST   | `/products/` | `{ "username", "password", "state", "center" }`                         | Lista os produtos presentes no carrinho        |
| POST   | `/buy/`      | `{ "username", "password" }`                                            | Finaliza a compra com o carrinho atual         |

### `/states`

Resposta:

```json
{
  "states": ["Acre", "Alagoas", "Amazonas", "...", "Tocantins"]
}
```

### `/centers/`

```bash
curl -X POST http://localhost:8000/centers/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "renanrodrigues7110",
           "password": "#Admin2025",
           "state": "São Paulo"
         }'
```

Resposta: lista de centros retornados por `WebScraper.list_centers()`.

### `/search/`

```bash
curl -X POST http://localhost:8000/search/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "renanrodrigues7110",
           "password": "#Admin2025",
           "state": "São Paulo",
           "center": "Ozonteck Praia Grande - SP",
           "product": "Omega",
           "quantity": 2
         }'
```

- Quando `quantity > 0` o produto é adicionado ao carrinho através da automação Playwright.
- Se o centro não for encontrado, a rota dispara `HTTPException(404)`.

### `/products/`

```bash
curl -X POST http://localhost:8000/products/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "renanrodrigues7110",
           "password": "#Admin2025",
           "state": "São Paulo",
           "center": "Ozonteck Praia Grande - SP"
         }'
```

Resposta: lista de produtos presentes no carrinho retornados por `WebScraper.products()`.

### `/buy/`

```bash
curl -X POST http://localhost:8000/buy/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "renanrodrigues7110",
           "password": "#Admin2025"
         }'
```

Resposta:

```json
{
  "message": "success",
  "status": 200
}
```

Caso algo falhe durante o checkout, `message` vira `failed` e `status` retorna `400`.

## Testes automatizados

Execute a suíte completa:

```bash
pytest
```

Marcadores disponíveis em `tests/test_scraper.py`:

- `pytest -m search`
- `pytest -m centers`
- `pytest -m select_center`

## Dicas e solução de problemas

- Garanta que o usuário fornecido tenha permissão para acessar o portal; caso contrário o login travará antes das rotas serem concluídas.
- Se precisar resetar a sessão do navegador, remova a pasta `data/<LOGIN>/` antes de rodar novamente.
- Em ambientes Windows, mantenha o servidor iniciado via `python app.py` ou `uvicorn app:app ...` para que a política de loop configurada no início do arquivo seja aplicada.
