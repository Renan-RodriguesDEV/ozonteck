import os

from dotenv import load_dotenv

from core.webscraper import WebScraper

load_dotenv()

URL_BASE = os.getenv("URL_BASE")


def get_centers(username: str, password: str, state):
    with WebScraper(url=URL_BASE, username=username, headless=False) as scraper:
        if scraper.login(username, password):
            scraper.select_state(state)
            return scraper.list_centers()
    return []


def select_center(username: str, password: str, state: str, center: str):
    with WebScraper(url=URL_BASE, username=username, headless=False) as scraper:
        if scraper.login(username, password):
            scraper.select_state(state)
            return scraper.select_center(center)
    return False


def search_product(
    username: str,
    password: str,
    product: str,
    quantity: int = 0,
):
    with WebScraper(url=URL_BASE, username=username, headless=False) as scraper:
        if scraper.login(username, password):
            return scraper.search(product, quantity)
    return None


def buy_cart(
    username: str,
    password: str,
):
    with WebScraper(url=URL_BASE, username=username, headless=False) as scraper:
        if scraper.login(username, password):
            return scraper.buy()
    return False
