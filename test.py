import unittest, time
from HTMLTestRunner import HTMLTestRunner
from webdriverio.app import WebdriverIO

from selenium.webdriver.common.by import By

def add_delay():
    #time.sleep(1)
    pass

class WebdriverIO_BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = WebdriverIO()
        self.app.open("/")

    def tearDown(self):
        print("Page:", self.app.current_page)
        add_delay()
        self.app.quit()
        

    def test_api_link_in_the_header_points_to_API_doc_page(self):
        """Test That the header link for API points to the right page"""
        app = self.app
        self.app.navigate_to('API')
        assert app.current_page == app.api
        app.current_page.side_bar.wait_for_presence()

    def test_searching_for_click_api_fucntionality(self):
        """Validate that when we search for Click, the first result from 'element' section is the click API doc"""
        app = self.app
        self.app.navigate_to('API')
        app.search('Click')
    
        with app.current_page.search_widget.results_block as results:
            time.sleep(1)
            assert results.is_present
            results_for_element = results.all('element')
            assert results_for_element
            results_for_element[0].click()
            
        assert app.current_page == app.api
        app.current_page.side_bar.wait_for_presence()
        self.assertTupleEqual(app.current_page.side_bar.active_menu,('element', 'click'))

    def test_api_protocols_list_is_correct(self):
        """Verify that the API->Protocols list in the menue, matches the expected list of protocols"""
        app = self.app
        self.app.navigate_to('API')
        app.current_page.side_bar.wait_for_presence()
        menues = app.current_page.side_bar.all_menues
        assert "Protocols" in menues
        app.current_page.side_bar.all_menues['Protocols'].click()
        time.sleep(1)
        
        submenues = list(app.current_page.side_bar.active_submenues.keys())
        expected = ["WebDriver Protocol", "Appium", "Mobile JSON Wire Protocol", "Chromium", "Sauce Labs", "Selenium Standalone", "JSON Wire Protocol"]
        
        self.assertListEqual(expected, submenues)

class WebdriverIO_ExtendedTests(unittest.TestCase):

    def setUp(self):
        self.app = WebdriverIO()
        self.app.open("/")

    def tearDown(self):
        print("Page:", self.app.current_page)
        add_delay()
        self.app.quit()
        

    def test_empty_search_cannot_be_cleared(self):
        """Validate that empty serach can not be cleared (button should not be presented)"""
        app = self.app
        app.search('')
    
        assert not app.current_page.search_widget.clear_button.is_present

    def test_search_clear_functionality(self):
        """Validate that when we clear the search, then input is empty and clear button dissaper"""
        app = self.app
        app.search('Test')
        time.sleep(1)

        assert app.current_page.search_widget.clear_button.is_present
        app.current_page.search_widget.clear()
        assert app.current_page.search_widget.input.value == ""
        assert not app.current_page.search_widget.clear_button.is_present

    def test_search_see_more_results(self):
        """Validate that when we clear the search, then input is empty and clear button dissaper"""
        app = self.app
        app.search('Click')
        time.sleep(1)

        assert app.current_page.search_widget.see_all_button.is_present
        app.current_page.search_widget.expand()

        assert app.current_page == app.full_search


    def test_search_see_more_results_in_case_of_single_hit(self):
        """Validate that when we clear the search, then input is empty and clear button dissaper"""
        app = self.app
        app.search('Only one result')
        time.sleep(1)

        assert not app.current_page.search_widget.see_all_button.is_present
        

if __name__ == "__main__":
    unittest.main()
    #unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(stream=open('report.html', 'w')))


    
    

        

    

    
