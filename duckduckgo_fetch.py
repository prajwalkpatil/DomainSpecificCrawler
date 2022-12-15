import re
import requests
from bs4 import BeautifulSoup

duckDuckUrl = 'https://html.duckduckgo.com/html/'
payload = {'q': ''}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'}

payload['q'] = "Google search"
res = requests.post(duckDuckUrl, data=payload, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
link_elements = soup.findAll('a')

link_set = set()

for i in link_elements:
    link = i.get("href")
    if(re.match(r"http\S*", str(link))):
        link_set.add(link)

for i in link_set:
    print(">> ", i)
