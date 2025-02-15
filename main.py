from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

MOST_PLAYED_XPATH = "//*[@id='main']/div[2]/div[1]/div[1]/table"
TRENDING_XPATH = "//*[@id='main']/div[2]/div[1]/div[2]/table"
RELEASE_XPATH = '//*[@id="main"]/div[2]/div[2]/div[1]/table'
HOT_XPATH = '//*[@id="main"]/div[2]/div[2]/div[2]/table'

# Configurer Chrome option
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Exécuter en mode headless

# Init Selenium Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open browser
driver.get("https://steamdb.info/")

time.sleep(7)

XPATH_LIST = [MOST_PLAYED_XPATH, TRENDING_XPATH, RELEASE_XPATH, HOT_XPATH]

email_content = []

for xpath in XPATH_LIST:
    try:
        parent_table = driver.find_element(By.XPATH, xpath)
        rows = parent_table.find_elements(By.TAG_NAME, 'tr')

        # Extracts column title
        headers = rows[0].find_elements(By.TAG_NAME, 'th')
        header_names = [header.text.strip() for header in headers[1:4]]  # Colonnes d'index 2, 3 et 4
        title = header_names[0]
        email_content.append(" ")
        email_content.append(title)

        # Get data from tables rows
        for index, row in enumerate(rows[1:11], start=1):  # Les 10 premiers jeux, en ignorant l'en-tête
            columns = row.find_elements(By.TAG_NAME, 'td')
            game_name_element = columns[2].find_element(By.TAG_NAME, 'a')
            game_name = game_name_element.text.strip()
            game_href = game_name_element.get_attribute('href')
            current_players = columns[3].text.strip()
            peak_today = columns[4].text.strip()

            # Format data
            line = f"{index}: Game: {game_name} (<a href='{game_href}'>Link</a>), {header_names[1]}: {current_players}, {header_names[2]}: {peak_today}"
            email_content.append(line)

    except NoSuchElementException:
        print("The searched element was not found.")
    except TimeoutException:
        print("Webpage took too long to load.")
    except Exception as e:
        print(f"Error happened : {e}")

# Quit driver Selenium
driver.quit()

# Print future email
for line in email_content:
    print(line)
