import requests
from bs4 import BeautifulSoup
import steam.webauth as wa




URL = 'https://steamcommunity.com/profiles/76561198373547526/inventory/#440'
URL_2 = 'https://steamcommunity.com/profiles/76561198373547526/inventory/#440'
Headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.4.3.257 Yowser/2.5 Yptp/1.23 Safari/537.36'
}
listings = []
balance = []
itemPrice = []

def outh():
    user = wa.WebAuth('login')
    twofactor = input('Введите 2FA код: ')
    session = user.login(password='password', twofactor_code=twofactor)
    return session

session = outh()

def get_html(url,params=None):
    r = session.get(url, params=params, headers=Headers)
    print(r)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('span', class_="games_list_tab_number")
    bal = soup.find_all('a', class_='global_action_link', id='header_wallet_balance')
    for b in bal:
        balance.append({

            'balance' : b.get_text(strip=True)

        })

    for i in items:
        listings.append({

            'count' : i.get_text(strip=True).replace('(','').replace(')','')

        })
    del listings[0:-2]
    del balance[0:-2]
    print(balance)
    print(listings)
    return balance, listings

def get_price(url):
    r = session.get(url, headers=Headers)
    html = r
    soup = BeautifulSoup(html.text, 'lxml')
    print(soup)


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

    if listings[-1].get('count') == '8':
        print(listings[-2])
        if listings[-2].get('count') == str(count_items):
            print(count_items)
            print("0")
            return 0

        else:
            count_items = int(listings[-2].get('count'))
            print(count_items)
            print('1')
            return 1

    else:
        print(listings[-1])
        if listings[-1].get('count') == str(count_items):
            print(count_items)
            print("0")
            return 0

        else:
            count_items = int(listings[-1].get('count'))
            balance[-1].get('balance')
            print(count_items)
            print('1')
            return 1
