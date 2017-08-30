from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from unittest import skip

class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.item_input_box().send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item."
        ))

        # She tries again with some text for the item, which now works
        inputbox = self.item_input_box()
        inputbox.send_keys('Trying again')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Trying again')

        # Perversely, she now decides to submit a second blank list item
        self.item_input_box().send_keys(Keys.ENTER)
        
        # She receives a similar warning on the list page
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item."
        ))
        
        # And she can correct it by filling some text in
        inputbox = self.item_input_box()
        inputbox.send_keys('How about now?')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Trying again')
        self.wait_for_row_in_list_table('2: How about now?')
