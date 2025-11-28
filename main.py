from core.webscraper import WebScraper


def get_webscrapper(username: str) -> WebScraper:
    return WebScraper(
        url="https://office.grupoozonteck.com/", username=username, headless=True
    )


def get_centers(webscraper: WebScraper, username: str, password: str, state):
    with webscraper as scraper:
        if scraper.login(username, password):
            scraper.select_state(state)
            return scraper.list_centers()
    return []


def select_center(
    webscraper: WebScraper, username: str, password: str, state: str, center: str
):
    with webscraper as scraper:
        if scraper.login(username, password):
            scraper.select_state(state)
            return scraper.select_center(center)
    return False


def search_product(
    webscraper: WebScraper,
    username: str,
    password: str,
    product: str,
    quantity: int = 0,
):
    with webscraper as scraper:
        if scraper.login(username, password):
            return scraper.search(product, quantity)
    return None


def buy_cart(
    webscraper: WebScraper,
    username: str,
    password: str,
):
    with webscraper as scraper:
        if scraper.login(username, password):
            return scraper.buy()
    return False
