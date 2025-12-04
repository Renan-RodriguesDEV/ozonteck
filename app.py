import asyncio
import os

import uvicorn
from fastapi import FastAPI, HTTPException

from main import buy_cart, get_centers, list_products, search_product, select_center
from schemas.schemas import UserCenterSchema, UserSchema, UserSchemaProduct, UserSearchSchema

app = FastAPI(title="Ozoneteck API", version="1.0.0")
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


@app.get("/states")
def states():
    """Lista de estados presentes no site.

    Returns:
        JSON: Lista de estados.
    """
    return {
        "states": [
            "Acre",
            "Alagoas",
            "Amazonas",
            "Amapá",
            "Bahia",
            "Ceará",
            "Distrito Federal",
            "Espírito Santo",
            "Goiás",
            "Maranhão",
            "Minas Gerais",
            "Mato Grosso do Sul",
            "Mato Grosso",
            "Pará",
            "Paraíba",
            "Pernambuco",
            "Piauí",
            "Paraná",
            "Rio de Janeiro",
            "Rio Grande do Norte",
            "Rondônia",
            "Roraima",
            "Rio Grande do Sul",
            "Santa Catarina",
            "Sergipe",
            "São Paulo",
            "Tocantins",
        ]
    }


@app.post("/centers/")
def centers(user: UserCenterSchema):
    """Lista os centros de distribuição disponiveis em determinado estado.

    Args:
        user (UserCenterSchema): Usuario com username, password e state.

    Returns:
        JSON: Lista de centros de distribuição.
    """
    return {"centers": get_centers(user.username, user.password, user.state)}


@app.post("/search/")
def search(user: UserSearchSchema):
    """Busca produtos em um centro de distribuição específico, pode, ou não, adicioná-los ao carrinho.

    Args:
        user (UserSchema): Usuario com username e password.
        state (str): Nome do estado.
        center (str): Nome do centro de distribuição, conforme a rota /centers retorna.
        product (str): Nome do produto a ser buscado.
        quantity (int, optional): Quantidade do produto a ser buscado. Padrão 0 para não adicionar ao carrinho.

    Returns:
        JSON: Lista de produtos, ou produto, encontrados.
    """
    if not select_center(user.username, user.password, user.state, user.center):
        raise HTTPException(404, "Center not found")
    return {
        "products": search_product(
            user.username, user.password, user.product, user.quantity
        )
    }


@app.post("/buy/")
def buy(user: UserSchema):
    """Compra os produtos presente no carrinho e retorna o status da compra.

    Args:
        user (UserSchema): Usuario com username e password.

    Returns:
        JSON: Status da compra, sendo "success" ou "failed".
    """
    is_buy = buy_cart(user.username, user.password)
    return {
        "message": "success" if is_buy else "failed",
        "status": 200 if is_buy else 400,
    }


@app.post("/products/")
def products(user: UserSchemaProduct):
    """Lista os produtos presentes no carrinho.

    Args:
        user (UserSchema): Usuario com username e password.

    Returns:
        JSON: Lista de produtos no carrinho.
    """
    if not select_center(user.username, user.password, user.state, user.center):
        raise HTTPException(404, "Center not found")
    return {"products": list_products(user.username, user.password)}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
