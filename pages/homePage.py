from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class HomePage :
    def __init__(self,driver,wait):
        self.driver = driver
        self.wait = wait

        self.title_img = (By.XPATH,'//*[@id="app"]/header/a')
        self.menu_items = (By.CSS_SELECTOR,'.card:nth-child(4) .card-up')
        self.url_attendu = 'https://demoqa.com/widgets'


    def verif_page_homepage(self) :
        assert self.wait.until(EC.visibility_of_element_located(self.title_img))
        assert self.wait.until(EC.visibility_of_element_located(self.menu_items))
    
    def click_menu_item_widget(self):
        self.wait.until(EC.visibility_of_element_located(self.menu_items)).click()
        self.wait.until(EC.url_to_be(self.url_attendu))  # Attend que l'URL soit mise à jour
        assert self.driver.current_url == self.url_attendu, f"L'URL attendue est {self.url_attendu}, mais l'URL actuelle est {self.driver.current_url}"
        

