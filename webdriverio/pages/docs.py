import pom

from pom import ui
from selenium.webdriver.common.by import By

from .main_page import Page as MainPage


class Page(MainPage):
    """Main page."""
    url = '/docs/gettingstarted'