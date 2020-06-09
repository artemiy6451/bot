import requests
from bs4 import BeautifulSoup


baseId = 440_2_8815869294

URL = 'https://steamcommunity.com/profiles/76561198373547526/inventory/#440'
Headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.4.3.257 Yowser/2.5 Yptp/1.23 Safari/537.36'
}
listings = []

def get_html(url,params=None):
    r = requests.get(url, params=params, headers=Headers)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('span', class_="games_list_tab_number")

    print(items)
    for i in items:
        listings.append({

            'count' : i.get_text(strip=True).replace('(','').replace(')','')
        })
    print(listings)
    return listings

def parse():
    html = get_html(URL)
    print(html.status_code)
    if html.status_code == 200:
        get_content(html.text)
    else: print('Error')
count_items = 1
def comparison():
    parse()
    global count_items
    if listings[-1].get('count') == str(count_items):
        print(count_items)
        print("0")
        return 0
    else:
        count_items = int(listings[-1].get('count'))
        print(count_items)
        print('1')
        return 1