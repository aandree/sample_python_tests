import pom

from pom import ui
from selenium.webdriver.common.by import By

from .main_page import Page as MainPage

@ui.register_ui(
    input = ui.TextField(By.XPATH, './/input[@name="q"]'))
class Page(MainPage):
    """Full Search page."""
    url = '/search'