from bs4 import BeautifulSoup
import requests
import json
import lxml

headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

params = {
    'q': 'Google doodle',  # query
    'gl': 'us',    # country to search from
    'hl': 'en',     # language
}

page_range = []
no_of_pages = 5
for i in range(0, no_of_pages):
    page_range.append(i*10)

data = []
for i in page_range:
    params['start'] = i
    html = requests.get("https://www.google.com/search",
                        headers=headers, params=params, timeout=20)
    soup = BeautifulSoup(html.text, 'lxml')
    for result in soup.select('.tF2Cxc'):
        link = result.select_one('.yuRUbf a')['href']
        data.append(link)

print(json.dumps(data, indent=2, ensure_ascii=False))
