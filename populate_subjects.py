from bs4 import BeautifulSoup
import requests

page = requests.get('http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html')

soup = BeautifulSoup(page.text, 'lxml')
print page.text
print soup.find_all('SELECT')