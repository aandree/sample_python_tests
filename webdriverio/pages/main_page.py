import pom

from pom import ui
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from waiting import wait


@ui.register_ui(
    docs    = ui.Link(By.XPATH, './/a[text()="Docs"]'),
    api     = ui.Link(By.XPATH, './/a[text()="API"]'),
    search  = ui.Link(By.XPATH, './/button[contains(@class, "DocSearch")]'))
class Navigation(ui.Block):
    """App navigation"""

    def select(self, text):
        try:
            self.find_element((By.XPATH, f'.//a[text()="{text}"]')).click()
        except Exception as e:
            print("Invalid option")
            raise e

class ResultsBlock(ui.Block):
    """Search widget results container"""

    def all(self, section=None):
        pattern = f".//section[descendant::div[text()='{section}']]//li" if section else ".//li"
        wait(lambda: self.find_elements((By.XPATH, pattern)), timeout_seconds=10, sleep_seconds=0.1)
        return self.find_elements((By.XPATH, pattern))

@ui.register_ui(
    input         = ui.TextField(By.ID, 'docsearch-input'),
    clear_button  = ui.Button(By.XPATH, './/button[@type="reset"]'),
    see_all_button= ui.Link(By.XPATH, './/section[@class="DocSearch-HitsFooter"]/a[contains(text(), "See all")]'),
    results_block = ResultsBlock(By.CLASS_NAME, "DocSearch-Dropdown")
    )
class SearchWidget(ui.Block):
    """App search widget"""

    def clear(self):
        self.clear_button.wait_for_presence(timeout=2)
        if self.clear_button.is_present: self.clear_button.click()
        else: print("Nothing to clear")

    def expand(self):
        self.see_all_button.wait_for_presence(timeout=2)
        if self.see_all_button.is_present: self.see_all_button.click()
        else: print("Nothing to expand")

    

@ui.register_ui(list = ui.List(By.TAG_NAME, 'ul'))
class SideBar(ui.Block):
    "App sidebar"

    @property
    def active_menu(self):
        try:
            category = self.find_element((By.XPATH, ".//ul/li/a[contains(@class, 'menu__link--active')]"))
            subcategory = category.find_elements(By.XPATH, "..//ul/li/a[contains(@class, 'active')]")    
            return (category.text, subcategory[0].text if subcategory else None)
        except NoSuchElementException:
            return (None, None)
    @property
    def active_submenues(self):
        try:
            category = self.find_element((By.XPATH, ".//ul/li/a[contains(@class, 'menu__link--sublist')]"))
            submenues = category.find_elements(By.XPATH, "..//ul/li/a")    
            return {x.text: x for x in submenues}
        except NoSuchElementException:
            return {}

    @property
    def all_menues(self):
        links = [row.webelement.find_element(By.TAG_NAME, 'a') for row in self.list.rows]
        return {link.text: link for link in links}        

@ui.register_ui(
    navigation      = Navigation(By.XPATH, '//nav[contains(@class, "navbar")]'),
    search_widget   = SearchWidget(By.CLASS_NAME, "DocSearch-Modal"),
    side_bar        = SideBar(By.CSS_SELECTOR, '.main-wrapper .menu')
    )
class Page(pom.Page):
    """Main page."""
    url = '/'
