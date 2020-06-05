from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


def overunder(list):
    return max(set(list), key=list.count)


chrome = webdriver.Chrome('./chromedriver')
chrome.get('https://www.rezultati.com/')
time.sleep(1)  # sega za sega 1
matches = chrome.find_elements_by_css_selector("[id^=g_1_]")
match_ids = []
for e in matches:
    match_ids.append(e.get_attribute("id").strip("g_1_"))
chrome.close()


def get_under_over(match_id, goals):
    chrome = webdriver.Chrome('./chromedriver')
    chrome.get(f'https://www.rezultati.com/utakmica/{match_id}/#tablica;over_under;overall;{goals}')
    ids = chrome.execute_script('return participantEncodedIds')
    t1id, t2id = ids[0], ids[1]
    WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.CLASS_NAME, f'glib-participant-{t1id}')))
    t1 = overunder(
        [el for el in [e.text.split('\n') for e in chrome.find_elements_by_class_name(f'glib-participant-{t1id}')] if
         el != ['']][0][-5:])
    t2 = overunder(
        [el for el in [e.text.split('\n') for e in chrome.find_elements_by_class_name(f'glib-participant-{t2id}')] if
         el != ['']][0][-5:])
    chrome.close()
    if t1 == t2:
        return t1


for match_id in match_ids:
    try:
        chrome = webdriver.Chrome('./chromedriver')
        chrome.get(f'https://www.rezultati.com/utakmica/{match_id}/#omjer;overall')
        omjer = WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "h2h_mutual")))
        strong = [el for el in [e.text for e in omjer.find_elements_by_tag_name('strong')] if el]
        winner = set([e for e in strong if strong.count(e) >= 3])
        ids = chrome.execute_script('return participantEncodedIds')
        t1id, t2id = ids[0], ids[1]
        chrome.close()
        if winner:
            try:
                chrome = webdriver.Chrome('./chromedriver')
                chrome.get(f'https://www.rezultati.com/utakmica/{match_id}/#tablica;ht_ft;overall')
                WebDriverWait(chrome, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, f'glib-participant-{t1id}')))
                stats1 = [e.text.split('\n') for e in chrome.find_elements_by_class_name(f'glib-participant-{t1id}')][0]
                stats2 = [e.text.split('\n') for e in chrome.find_elements_by_class_name(f'glib-participant-{t2id}')][0]
                t1os, t1pp, t1pn, t1pi, t1np, t1nn, t1ni, t1ip, t1in, t1ii = stats1[2], stats1[3], stats1[4], stats1[5], \
                                                                             stats1[6], stats1[7], stats1[8], stats1[9], \
                                                                             stats1[10], stats1[11]
                t2os, t2pp, t2pn, t2pi, t2np, t2nn, t2ni, t2ip, t2in, t2ii = stats2[2], stats2[3], stats2[4], stats2[5], \
                                                                             stats2[6], stats2[7], stats2[8], stats2[9], \
                                                                             stats2[10], stats2[11]
                if (int(t1pp) > int(max(t1pn, t1pi, t1np, t1nn, t1ni, t1ip, t1in, t1ii)) or int(t2ii) > int(
                        max(t2pp, t2pn, t2pi, t2np, t2nn, t2ni, t2ip, t2in))) or (
                        int(t2pp) > int(max(t2pn, t2pi, t2np, t2nn, t2ni, t2ip, t2in, t2ii)) or int(t1ii) > int(
                    max(t1pp, t1pn, t1pi, t1np, t1nn, t1ni, t1ip, t1in))):
                    if get_under_over(match_id, '1.5') == '+' and get_under_over(match_id, '3.5') == '-':
                        print(f'{winner} ht-ft & 2-3')
                chrome.close()
            except:
                continue
    except:
        continue
