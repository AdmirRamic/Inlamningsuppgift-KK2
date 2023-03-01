from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class WebTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        serv_obj = Service("C:\Drivers\chromedriver_win32\chromedriver.exe")
        cls.driver = webdriver.Chrome(service=serv_obj)
        cls.mywait = WebDriverWait(cls.driver,10)
        cls.driver.maximize_window()

    def setUp(self):
        self.driver.get("https://www.axesslogistics.se/")
        self.mywait.until(EC.element_to_be_clickable((By.XPATH,"(//a[normalize-space()='Acceptera'])[1]"))).click()
        
    # Test som verifierar att länken "VÅRA TJÄNSTER" leder till förväntad rubrik
    def test_link_path(self):
        link_vara_tjanster = self.driver.find_element(By.XPATH,"//a[@role='button'][normalize-space()='Våra tjänster']")
        expected = (link_vara_tjanster.text).upper()
        link_vara_tjanster.click()
        actual = (self.mywait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='section_196']/p"))).text).upper()
        self.assertEqual(expected,actual)

    # Test som verifierar att byta språk verkligen byter språk till engelska
    def test_change_language(self):
        self.driver.find_element(By.XPATH,"/html/body/div[3]/div[4]/div/div[5]/section/p[2]").click()
        self.mywait.until(EC.element_to_be_clickable((By.XPATH,"(//a[normalize-space()='English'])[1]"))).click()
        actual = self.driver.find_element(By.XPATH,"//p[@class='language-text'][normalize-space()='LANGUAGE']").text
        expected = "LANGUAGE"
        self.assertEqual(expected,actual)

    #  Test som verifierar att Malmö anläggningen finns med och att adressuppgifterna stämmer
    def test_address(self):
        self.driver.find_element(By.XPATH,"(//a)[24]").click()
        address = self.driver.find_element(By.XPATH,"//section[@id='section_494']").text
        expected = "MALMÖ\nBox 50331, 202 12 Malmö\nBESÖKSADRESS:\nFrihamnsallén 20, 211 20 Malmö"
        self.assertEqual(expected,address)

    # Test som verifierar att man får felmeddelande "Felaktigt användarenamn eller lösenord" 
    # när man försöker logga in med ogiltiga uppgifter
    def test_invalid_login(self):
        self.driver.find_element(By.XPATH,"(//img[contains(@class,'login-icon')])[1]").click()
        self.mywait.until(EC.element_to_be_clickable((By.XPATH,"//a[@href='/User/Login']"))).click()
        self.driver.find_element(By.ID,"User_UserName").send_keys("peter.petersson@hotmail.com")
        self.driver.find_element(By.ID,"User_Password").send_keys("Selenium")
        self.driver.find_element(By.XPATH,"//button[normalize-space()='Logga in']").click()
        pop_up = self.mywait.until(EC.presence_of_element_located((By.XPATH,"//article[@class='alertify-log alertify-log-error alertify-log-show']")))
        expected ="Felaktigt användarnamn eller lösenor"
        self.assertEqual(expected,pop_up.text)

    # Testar om man kommer tillbaka till startsidan när man klickar på AxessLogistics loggo
    def test_back_to_main_page(self):
        main_title = self.driver.title
        self.driver.find_element(By.XPATH,"(//a[normalize-space()='Nyheter'])[1]").click()
        under_page_title = self.driver.title
        self.assertEqual(under_page_title,"One Master - News Archive")
        self.driver.find_element(By.XPATH,"//a[@href='/sv']//img").click()
        self.assertEqual(main_title,self.driver.title)

    # Testar om man får rätt nyhetsartikel som länker hänvisar till
    def test_right_news_article(self):
        self.driver.find_element(By.XPATH,"(//a[normalize-space()='Nyheter'])[1]").click()
        news_link = self.mywait.until(EC.presence_of_element_located((By.XPATH,"//article[1]/div/div/h3/a")))
        news_link_text = (news_link.text).upper()
        news_link.click()
        news_header_text = (self.driver.find_element(By.CSS_SELECTOR,".article-title").text).upper()
        header_content = news_link_text in news_header_text
        self.assertTrue(header_content)

    # Test som verifierar att byta land till norges hemsida fungerar
    def test_open_linked_homepage(self):
        self.driver.find_element(By.XPATH,"//section[@class='section section_Content section_1457 js-country-icon hidden-xs']//p[@class='flag-blue-text'][normalize-space()='BYT LAND']").click()
        self.mywait.until(EC.element_to_be_clickable((By.LINK_TEXT,"AXESS.NO"))).click()
        windowsIDs = self.driver.window_handles
        self.driver.switch_to.window(windowsIDs[1])
        expected = "https://www.axesslogistics.no/"
        actual = self.driver.current_url
        self.assertEqual(expected,actual)
        self.driver.close()
        self.driver.switch_to.window(windowsIDs[0])

    def tearDown(self):
        self.driver.delete_all_cookies()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
