from pathlib import Path

from playwright.sync_api import ElementHandle, TimeoutError, sync_playwright


class WebScraper:
    def __init__(self, url: str, username: str, headless: bool = True):
        self.url = url
        self.username = username
        self.data_dir = Path(f"./data/{self.username}")
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(
            self.data_dir,
            headless=self.headless,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
        )
        self.page = (
            self.browser.pages[0] if self.browser.pages else self.browser.new_page()
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def login(self, username, password):
        self.page.goto(self.url + "login")
        self.page.wait_for_load_state("load")
        if self.page.url != f"{self.url}login":
            return True
        self.page.fill('input[type="email"]', username)
        self.page.fill('input[type="password"]', password)
        self.page.click('button[type="submit"]')
        if self.page.wait_for_selector(
            ".modal-content", state="visible", timeout=10_000
        ):
            try:
                self.page.evaluate('closeModal("modal-updateAddress")')
                self.page.evaluate('$("#modal-message").remove()')
            except Exception as e:
                print("No modal to close:", str(e))
        try:
            self.page.wait_for_url(self.url, timeout=60_000)
        except TimeoutError as e:
            print("O login falhou:", str(e))
            return False
        return True

    def select_state(self, state: str):
        # https://office.grupoozonteck.com/universal/store-internal
        self.page.goto(self.url + "universal/store-internal")
        try:
            self.page.select_option('select[id="state_id_store"]', state)
            print(f"Estado {state} selecionado com sucesso.")
            return True
        except TimeoutError as e:
            print("Falha ao selecionar o estado:", str(e))
        return False

    def list_centers(self):
        centers = [
            e.inner_text() for e in self.page.query_selector_all('strong[class="mb-1"]')
        ]
        print(f"Centros encontrados: {centers}")
        return centers

    def select_center(self, center: str):
        card = self.page.query_selector(
            f'//div[@class="card-body"]//strong[text()="{center}"]/../..'
        )
        if not card:
            return False
        try:
            card.query_selector('//button[text()="Selecionar"]').click()
            self.page.wait_for_url(
                "https://office.grupoozonteck.com/universal/store-show"
            )
            print("Centro selecionado com sucesso.")
        except TimeoutError as e:
            print("Falha ao selecionar o centro:", str(e))
            return False
        return True

    def search(
        self,
        product: str,
        quantity: int = 0,
    ):
        # https://office.grupoozonteck.com/universal/store-show?search=Omega&category=
        self.page.goto(self.url + f"universal/store-show?search={product}&category=")
        self.page.wait_for_load_state("load")
        products = self.page.query_selector_all('//div[@class="card-body"]')
        if not products:
            print("Nenhum produto encontrado.")
            return []
        if len(products) > 1:
            print(f"Produtos encontrados: {[e.inner_text() for e in products]}")
            return [self.product_details(e) for e in products]
        if quantity > 0:
            self.page.fill('input[type="text"]', str(quantity))
            self.page.click('//button[contains(@class,"button-cart")]')
        self.page.wait_for_load_state("load")
        print(f"Produto {products[0].inner_text()} adicionado ao carrinho.")
        return self.product_details(products[0])

    def buy(self):
        # https://office.grupoozonteck.com/universal/store-cart
        self.page.goto(self.url + "universal/store-cart")
        try:
            self.page.click('//span[contains(text(),"endereço")]')
            self.page.click('//button[@type="submit" and contains(text(),"pagamento")]')
            self.page.click('//button[@id="pay-with-balance"]')
            self.page.click('//button[@id="confirm-payment"]')
            print("Compra finalizada com sucesso.")
            return True
        except TimeoutError as e:
            print("Falha ao finalizar a compra:", str(e))
        return False

    def product_details(self, card: ElementHandle):
        name = card.query_selector('//span[@class="fw-bold mb-sm-2"]')
        description = card.query_selector('//p[@class="card-text"]')
        priece = card.query_selector('//strong[contains(text(),"R$")]')
        print(f"Detalhes do produto extraídos com sucesso. {name, description, priece}")
        return {
            "name": name.inner_text() if name else "",
            "description": description.inner_text() if description else "",
            "priece": priece.inner_text() if priece else "",
        }

    def products(self):
        self.page.goto(self.url + "universal/store-show")
        self.page.wait_for_url(self.url + "universal/store-show")
        self.page.evaluate(
            "window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })"
        )
        products = self.page.query_selector_all('//div[@class="card-body"]')
        print(f"Produtos encontrados: {len(products)}")
        return [self.product_details(e) for e in products]
