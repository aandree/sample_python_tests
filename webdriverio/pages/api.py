import pom

from pom import ui
from selenium.webdriver.common.by import By

from .main_page import Page as MainPage


@ui.register_ui(
    title               = ui.UI(By.CSS_SELECTOR, 'header h1'),
    full_description    = ui.Block(By.CSS_SELECTOR, 'div.markdown'))
class Article(ui.Block):
    "API doc article"

    @property
    def text(self):
        return f"{self.title.get_attribute('innerText')}\n\n{self.get_attribute('innerText')}" 

@ui.register_ui(article = Article(By.TAG_NAME, 'article'))
class Page(MainPage):
    """Main page."""
    url = '/docs/api'