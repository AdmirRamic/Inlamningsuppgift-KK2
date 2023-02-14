from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest

class WebTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.serv_obj = Service("C:\Drivers\chromedriver_win32\chromedriver.exe")
        self.driver = webdriver.Chrome(options=options,service=self.serv_obj)
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.axesslogistics.se/")
        self.driver.maximize_window()
    
    # Test som verifierar om länken "VÅRA TJÄNSTER" leder till förväntad rubrik
    def test_link_path(self):
        link_vara_tjanster = self.driver.find_element(By.XPATH,"//a[@role='button'][normalize-space()='Våra tjänster']")
        expected = link_vara_tjanster.text.upper()
        link_vara_tjanster.click()
        actual = self.driver.find_element(By.XPATH,"//*[@id='section_196']/p").text.upper()
        self.assertEqual(expected,actual)

    # Test som verifierar om att byta land till norges hemsida fungerar
    def test_open_linked_homepage(self):
        self.driver.find_element(By.XPATH,"//section[@class='section section_Content section_1457 js-country-icon hidden-xs']//p[@class='flag-blue-text'][normalize-space()='BYT LAND']").click()
        self.driver.find_element(By.LINK_TEXT,"AXESS.NO").click()
        windowsIDs = self.driver.window_handles
        self.driver.switch_to.window(windowsIDs[1])
        expected = "https://www.axesslogistics.no/"
        actual = self.driver.current_url
        self.assertEqual(expected,actual)

    def test_change_language(self):
        self.driver.find_element(By.XPATH,"/html/body/div[3]/div[4]/div/div[5]/section/p[2]").click()
        self.driver.find_element(By.XPATH,"//a[normalize-space()='English']").click()
        actual = self.driver.find_element(By.XPATH,"//p[@class='language-text'][normalize-space()='LANGUAGE']").text
        expected = "LANGUAGE"
        self.assertEqual(expected,actual)


    

    
    

        

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()