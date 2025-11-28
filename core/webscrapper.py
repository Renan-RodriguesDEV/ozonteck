from playwright.sync_api import sync_playwright


class WebScraper:
    def __init__(self, url, headless=True):
        self.url = url
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
