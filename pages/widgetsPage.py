from math import e
import select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
#import WebElement 
import time




class WidgetPage :
    def __init__(self,driver,wait):
        self.driver = driver
        self.wait = wait

        #Premier conteneur 
        self.date_picker = (By.CSS_SELECTOR,'.show #item-2 > .text')
        self.container_picker = (By.ID,'datePickerContainer')
        self.select_date_input = (By.ID,'datePickerMonthYearInput')
        self.mouth = (By.CLASS_NAME,'react-datepicker__month-select')
        self.year = (By.CLASS_NAME,'react-datepicker__year-select')
        self.nb_days = (By.CSS_SELECTOR,'.react-datepicker__day--005')
#########################################################################################################

        #Deuxième conteneur
        self.date_hour = (By.ID,'dateAndTimePickerInput')
        #Cliquer et voir la liste des mois
        self.click_list_month = (By.CSS_SELECTOR,'.react-datepicker__month-read-view--selected-month')
        #Le mois de selectionner final
        self.month_select = (By.CSS_SELECTOR,'.react-datepicker__month-read-view--selected-month')
        #Liste des mois que je stocker dans une liste pour les parcourir
        self.list_month_recup = (By.XPATH,"//div[contains(@class, 'react-datepicker__month-option')]")

        self.click_year = (By.CSS_SELECTOR,'.react-datepicker__year-read-view--selected-year') 
        self.goto2035 = (By.CSS_SELECTOR,'.react-datepicker__navigation react-datepicker__navigation--years react-datepicker__navigation--years-upcoming')
        self.click_2035 = (By.CSS_SELECTOR,'.react-datepicker__year-option')

    def click_date_picker(self):
        self.wait.until(EC.visibility_of_element_located(self.date_picker)).click()#
    
    def select_date(self):
        try:
            # Ouvrir le sélecteur de date
            self.wait.until(EC.element_to_be_clickable(self.select_date_input)).click()

            # Sélectionner le mois
            Select(self.driver.find_element(*self.mouth)).select_by_visible_text('November')

            # Sélectionner l'année
            Select(self.driver.find_element(*self.year)).select_by_visible_text('2035')

            # Sélectionner le jour
            day_element = self.wait.until(EC.element_to_be_clickable(self.nb_days))
            day_element.click()

            print("Sélection de la date réussie.")
        
        except TimeoutException:
            print("Erreur : Un ou plusieurs éléments ne se sont pas chargés à temps.")#



    def select_date_hour(self):
        # 1️⃣ Ouvrir le sélecteur de date
        self.wait.until(EC.element_to_be_clickable(self.date_hour)).click()

        # 2️⃣ Ouvrir la liste des mois
        self.wait.until(EC.element_to_be_clickable(self.click_list_month)).click()

        # 3️⃣ Récupérer la liste des mois disponibles
        months = self.wait.until(EC.presence_of_all_elements_located(self.list_month_recup))

        # 4️⃣ Parcourir la liste pour cliquer sur "November"
        for month in months:
            if month.text.strip() == "November":
                month.click()
                time.sleep(5)
                break  # Stopper la boucle une fois que Novembre est sélectionné

        # 5️⃣ Vérifier quel mois a été sélectionné
        month_element = self.wait.until(EC.visibility_of_element_located(self.month_select))
        month_text = month_element.text

        day_element = self.wait.until(EC.element_to_be_clickable(self.nb_days))
        day_element.click()

        print("Sélection de la date réussie.")

        print("✅ Mois sélectionné :", month_text)  # Affiche le mois sélectionné








