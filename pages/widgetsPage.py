from argparse import Action
from math import e
from operator import ne
import select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
#import WebElement 
import time
from selenium.webdriver.common.action_chains import ActionChains




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
        self.list_year = (By.XPATH,"//div[contains(@class, 'react-datepicker__year-option')]")
        self.defiles_years = (By.XPATH,"(//div[contains(@class, 'react-datepicker__year-option')])[1]")
        self.click_2035 = (By.XPATH,"(//div[contains(@class, 'react-datepicker__year-option')])[3]")
        self.year_select = (By.CSS_SELECTOR,"react-datepicker__year-read-view--selected-year")

        self.select_hour = (By.CSS_SELECTOR,'.react-datepicker__time-list-item:nth-child(96)')

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


#########################################################################################################
    def select_date_hour(self):
        # 1️⃣ Ouvrir le sélecteur de date
        self.wait.until(EC.element_to_be_clickable(self.date_hour)).click()

        # 2️⃣ Ouvrir la liste des mois
        self.wait.until(EC.element_to_be_clickable(self.click_list_month)).click()

        # 3️⃣ Récupérer la liste des mois disponibles
        list_months = self.wait.until(EC.presence_of_all_elements_located(self.list_month_recup))

        # 4️⃣ Parcourir la liste pour cliquer sur "November"
        for nbmonth in list_months:
            if nbmonth.text.strip() == "November":
                nbmonth.click()
                break
        
        # 5️⃣ Vérifier quel mois a été sélectionné
        month_element = self.wait.until(EC.visibility_of_element_located(self.month_select))
        month_text = month_element.text

        day_element = self.wait.until(EC.element_to_be_clickable(self.nb_days))
        day_element.click()
        
        # 6 Select year
        self.wait.until(EC.element_to_be_clickable(self.click_year)).click()

        # Initialiser `year_text` pour éviter l'erreur UnboundLocalError
        year_text = ""

        try:
            while True:  # Continue jusqu'à ce que 2035 soit visible et sélectionnée
                list_years = self.wait.until(EC.presence_of_all_elements_located(self.list_year))
                year_found = False  # Variable pour savoir si 2035 est trouvée

                for nbyears in list_years:
                    if nbyears.text.strip() == "2035":
                        self.wait.until(EC.element_to_be_clickable(nbyears)).click()  # Clique sur 2035
                        time.sleep(1)  # Laisser le temps à l'interface de prendre en compte le clic
                        year_found = True  # Marquer que l'année a été trouvée
                        break  # Sortir de la boucle FOR
                
                if year_found:
                    break  # Si 2035 a été trouvée et cliquée, on arrête la boucle WHILE
                # Si 2035 n'est pas encore trouvée, on clique sur le bouton pour défiler les années
                self.wait.until(EC.element_to_be_clickable(self.defiles_years)).click()
                time.sleep(1)  # Attendre pour que les années défilent

            # Vérifier l'année sélectionnée après la boucle
            year_element = self.wait.until(EC.visibility_of_element_located(self.year_select))
            year_text = year_element.text.strip()
            
            day_element = self.wait.until(EC.element_to_be_clickable(self.nb_days))
            day_element.click()

        except Exception as e:
            print(f"Erreur lors de la sélection de l'année : {e}")
            print(f"Voici les éléments qu'on a : {month_text}, {year_text}, {list_years}")

        day_element = self.wait.until(EC.element_to_be_clickable(self.nb_days))
        day_element.click()
            
            # 1️⃣ Attendre que la liste des heures soit visible
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__time-list")))

        # 2️⃣ Récupérer tous les éléments de la liste
        time_options = self.driver.find_elements(By.CLASS_NAME, "react-datepicker__time-list-item")
        

        # 3️⃣ Parcourir la liste pour trouver l'heure désirée
        for option in time_options:
            target_time="23:45"
            if option.text.strip() == target_time:
                # 4️⃣ Scroller et cliquer sur l'heure
                actions = ActionChains(self.driver)
                actions.move_to_element(option).click().perform()
                print(f"✅ Heure sélectionnée : {target_time}")
                break
        time.sleep(1)







