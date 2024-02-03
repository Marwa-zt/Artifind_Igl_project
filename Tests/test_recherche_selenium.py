from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service as ChromeService



# Chemin du driver de navigateur 
driver_path = "chromedriver.exe"
#driver_path = "C:\\Users\\Dell\\Desktop\\app_essai\\Fastapi_mysql\\chromedriver.exe"
# L'URL de notre site web 
url = "https://www.google.com"

# Le terme à rechercher
search_term = "Matlab"

chrome_options = Options()
chrome_options.add_argument("--headless")  # Exemple : exécuter en mode sans tête
chrome_options.add_argument("--disable-extensions")
# Utilisez ChromeService au lieu de webdriver.Chrome
chrome_service = ChromeService(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Accéder à l'URL du site web 
driver.get(url)
time.sleep(5)
# Trouver l'élément de recherche
search_box = driver.find_element("name", "q")

# Entrer le terme de recherche
search_box.send_keys(search_term)

# Appuyer sur la touche Entrée pour effectuer la recherche
search_box.send_keys(Keys.RETURN)

# Attendre quelques secondes pour que les résultats de la recherche soient chargés 
time.sleep(5)

# Vérifier si le terme de recherche est présent dans le titre de la page résultante
assert search_term.lower() in driver.title.lower()

# Fermer le navigateur
driver.quit()
