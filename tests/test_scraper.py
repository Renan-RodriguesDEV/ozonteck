import os

import pytest

from main import get_centers, search_product, select_center

USUARIO = os.getenv("LOGIN")
SENHA = os.getenv("SENHA")


@pytest.mark.search
def test_search():
    search_product(USUARIO, SENHA, "soberano")


@pytest.mark.centers
def test_list_centers():
    centers = get_centers(USUARIO, SENHA, "São Paulo")
    [print(center) for center in centers]
    assert len(centers) > 0


@pytest.mark.select_center
def test_select_center():
    is_select = select_center(USUARIO, SENHA, "São Paulo", "Ozonteck Praia Grande - SP")
    assert is_select
