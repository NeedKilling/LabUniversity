from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By                         #search
from selenium.webdriver.support import expected_conditions as E     # waits
from selenium.webdriver.support.ui import WebDriverWait             # waits

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import json


from bs4 import BeautifulSoup


def get_schedule(GROUP):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")  
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)



    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver,15)

    all_schedule = []
    scheduleDay = None

    try:  
        driver.get(f"https://mti.moscow/studentu")

        wait.until(E.element_to_be_clickable((By.CLASS_NAME,"header__item")))
        tabStudents = driver.find_elements(By.CLASS_NAME,"header__item")[1]
        tabStudents.click()

        # select = driver.find_element(By.CLASS_NAME,"select__title")
        # select.click()
        wait.until(E.element_to_be_clickable((By.CLASS_NAME,"select__title")))
        driver.find_element(By.CLASS_NAME,"select__title").click()


        wait.until(E.element_to_be_clickable((By.NAME,"group_search")))
        inputGroup = driver.find_element(By.NAME,"group_search")
        inputGroup.send_keys(GROUP)

        # group = driver.find_element(By.CSS_SELECTOR, f"[data-title={GROUP}]")
        # group.click()
        wait.until(E.element_to_be_clickable((By.CSS_SELECTOR, f"[data-title={GROUP}]")))
        driver.find_element(By.CSS_SELECTOR, f"[data-title={GROUP}]").click()
        
        #####
        wait.until(E.text_to_be_present_in_element((By.CSS_SELECTOR, ".table-container"), "10:10" )) #проверка на данные в таблице
        #####
        tab_web = wait.until(E.presence_of_element_located((By.CLASS_NAME,"table-container")))
        tab_html = tab_web.get_attribute("outerHTML")
        pageSoup = BeautifulSoup(tab_html, features="html.parser")
        tbody = list(pageSoup.find("tbody").find_all("tr"))
       

        # params = f"?schedule-title={GROUP}&schedule-type={TYPE}&schedule-id={ID}"
        # driver.get(f"https://mti.moscow/studentu{params}")
        # pageHtml = driver.page_source

        # pageSoup = BeautifulSoup(pageHtml, features="html.parser")
        # tbody =  list(pageSoup.find("tbody").find_all("tr"))
        

        for i,tbodyItems in enumerate(tbody):
            content = tbodyItems.find_all("td")
            # if(i == 20):
            #     break

            lesson = {}
            
            if(content[0]['class'][0] == 'align-top'):  #первая пара вместе с датой
                if scheduleDay is not None:                           
                    all_schedule.append(scheduleDay)

                scheduleDay = {}
                scheduleDay["date"] = content[0].get_text()[0:10]
                scheduleDay["day"] = content[0].get_text()[10:]
                scheduleDay["lessons"] = []
                
                
                lesson["time"] =  content[1].get_text()
                lesson["Discipline"] = content[2].get_text() 
                lesson["typeD"] = content[3].get_text()
                lesson["Building"] = content[4].get_text()
                lesson["numberAud"] = content[5].get_text()
                lesson["Teacher"] = content[6].get_text()

                scheduleDay["lessons"].append(lesson)

            # if(content[0]['class'][0] != 'align-top'):          #####   все остальное что без даты
            else:   #после первой пары цикл отсюда
                if scheduleDay is None:                         ### если нет дня то пропуск                    
                    continue   

                lesson["time"] =  content[0].get_text()
                lesson["Discipline"] = content[1].get_text() 
                lesson["typeD"] = content[2].get_text()
                lesson["Building"] = content[3].get_text()
                lesson["numberAud"] = content[4].get_text()
                lesson["Teacher"] = content[5].get_text()

                scheduleDay["lessons"].append(lesson)


        all_schedule.append(scheduleDay)

        return json.dumps(all_schedule ,indent = 4, ensure_ascii= False)
        
        
    except Exception as error:
        print(f'ERROR: {error}')
        return []
    finally:
        driver.implicitly_wait(3)
        driver.quit()

# print(get_schedule('ОКБП-301итмп'))
