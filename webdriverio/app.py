import pom

from webdriverio.pages import main_page, api, docs, full_search

from pom import ui

class MainPage(main_page.Page):
    """app main page"""

class Docs(docs.Page):
    """app main page"""

class Api(api.Page):
    """app main page"""

class FullSearch(full_search.Page):
    """app main page"""

@pom.register_pages([MainPage, Docs, Api, FullSearch])
class WebdriverIO(pom.App):
    """WebdriverIO web application."""
    def __init__(self):
        super(WebdriverIO, self).__init__('https://webdriver.io/', 'Chrome')
        self.webdriver.maximize_window()
        self.webdriver.set_page_load_timeout(30)

    def navigate_to(self, text):
        self.current_page.navigation.select(text)

    def search(self, text):
        self.current_page.navigation.search.click()
        with self.current_page.search_widget as search:
            search.input.value = text
            #print(search.results_options)
            search.results_block.wait_for_presence()

        

        
if __name__ == "__main__":
    
    app = WebdriverIO()
    app.open("/")
    
    app.navigate_to('API')
    #app.api_documentation.is_loaded()
    app.search('Click')
    
    with app.current_page.search_widget.results_block as results:
        results.wait_for_presence()
        results.all('element')[0].click()

    app.current_page.side_bar.wait_for_presence()
    print(app.current_page.side_bar.active_menu)
    app.current_page.side_bar.all_menues['element'].click()
    app.current_page.side_bar.all_menues['Protocols'].click()

    app.search('Click')
    app.current_page.search_widget.expand()

    print(app.current_page)