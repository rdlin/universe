from bs4 import BeautifulSoup
import requests
import re

page = requests.get('https://uwaterloo.ca/find-out-more/programs/results')

soup = BeautifulSoup(page.text, 'lxml')
print page.text
programs = []
for li in soup.find_all('li'):
    print li
    result = re.search('">(.*)</a>', str(li))
    programs.append(result.group(1))
print programs