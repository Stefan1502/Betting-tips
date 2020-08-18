import requests
from bs4 import BeautifulSoup

url = 'https://www.forebet.com/en/football-tips-and-predictions-for-today/predictions-1x2'
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

matches = [el.text for el in soup.findAll("span", {"itemprop": "name"})]
matches = matches[::2]
avg = [el.text for el in soup.findAll("td", {"class": "avg_sc"})]
score = [ele.split("-") for ele in [el.text for el in soup.findAll("td", {"class": "ex_sc"})]]

index = 0

for goals in avg:
    if float(goals)>3.0 and int(score[index][0])!=0 and int(score[index][1])!=0 and (int(score[index][0])+int(score[index][1])>3):
        print(f'{matches[index]} gg3+')
    elif float(goals)<2.0 and int(score[index][0])==0 and int(score[index][1])==0:
        print(f'{matches[index]} 0-2')
    index += 1
