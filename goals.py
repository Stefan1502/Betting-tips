from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

chrome = webdriver.Chrome('./chromedriver')
chrome.get('https://www.rezultati.com/')
time.sleep(10)
matches = chrome.find_elements_by_css_selector("[id^=g_1_]")
match_ids = []
for e in matches:
    match_ids.append(e.get_attribute("id").strip("g_1_"))
chrome.close()

for match_id in match_ids:
    try:
        chrome = webdriver.Chrome('./chromedriver')
        chrome.get(f'https://www.rezultati.com/utakmica/{match_id}/#tablica;over_under;overall;2.5')
        ids = chrome.execute_script('return participantEncodedIds')
        t1id, t2id = ids[0], ids[1]
        stats = WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.ID, 'table-type-6-2.5')))
        statst1 = \
        [el for el in [e.text.split('\n') for e in stats.find_elements_by_class_name(f'glib-participant-{t1id}')] if
         el != ['']][0]
        statst2 = \
            [el for el in [e.text.split('\n') for e in stats.find_elements_by_class_name(f'glib-participant-{t2id}')] if
             el != ['']][0]
        chrome.close()
        if statst1[-5:].count('+') >= 4 and float(statst1[-7]) > 2.5 and statst2[-5:].count('+') >= 4 and float(
                statst2[-7]) > 2.5:
            print(statst1[1] + ' 3+')
        elif statst1[-5:].count('-') >= 4 and float(statst1[-7]) < 2.5 and statst2[-5:].count('-') >= 4 and float(
                statst2[-7]) < 2.5:
            print(statst1[1] + ' 0-2')
    except:
        try:
            chrome.close()
        except:
            continue
