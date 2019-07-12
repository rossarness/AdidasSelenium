import unittest

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

TEST_SETINGS = [
    [
        "apple",
        "A common, round fruit produced by the tree Malus domestica,"
        " cultivated in temperate climates.",
    ],
    [
        "pear",
        "An edible fruit produced by the pear tree, similar to an apple but"
        " elongated towards the stem.",
    ],
]
HTTP_URL = "https://en.wiktionary.org/"
HTTP_TITLE = "Wiktionary, the free dictionary"
SEARCH_BOX_ID = "searchInput"
SEARCH_RESULT_PATH = "#mw-content-text > div "
PAGE_ELEMENTS_PATH = (
    "#mw-content-text > div > ol:nth-child(n) > li:nth-child(n)")


class Adidas_test(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_the_website(self):
        self.browser.get(HTTP_URL)
        try:
            assert HTTP_TITLE in self.browser.title
        except AssertionError:
            self.fail("Incorrect website loaded")
        for test in TEST_SETINGS:
            search_box = self.browser.find_element_by_id(SEARCH_BOX_ID)
            search_box.click()
            search_box.send_keys(test[0])
            search_box.send_keys(Keys.RETURN)
            try:
                WebDriverWait(self.browser, 10).until(
                    ec.presence_of_element_located(
                        (By.CSS_SELECTOR, SEARCH_RESULT_PATH)
                    )
                )
            except TimeoutException:
                self.fail("Search results failed to load in 10 seconds")
            page_elements = self.browser.find_elements_by_css_selector(
                PAGE_ELEMENTS_PATH
            )
            text_found = False
            for element in page_elements:
                if test[1] in element.text:
                    text_found = True
            if not text_found:
                self.fail(f"Did not found proper result for {test[0]}")
