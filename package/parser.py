import requests
from bs4 import BeautifulSoup
import steam.webauth as wa

URL = 'https://steamcommunity.com/profiles/76561198373547526/inventory/#440'
URL_2 = 'https://steamcommunity.com/market/history#'
Headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.4.3.257 Yowser/2.5 Yptp/1.23 Safari/537.36'
}
listings = []
balance = []
itemPrice = []
twofactor= None
session = None
first = True
FILENAME = 'cookies.txt'
username = 'he2hh'
password = 'gfhnbz11'
cookies = {}

def login():
    global session
    twofactor_code = input('-')
    user = wa.WebAuth(username=username)
    session = user.login(password=password,twofactor_code=twofactor_code)
    return session

first_login = True
def on_login():
    global session
    global first_login
    global cookies
    if first_login:
        session = login()
        first_login = False
    for domain in ['store.steampowered.com', 'help.steampowered.com', 'steamcommunity.com']:
        if domain == 'store.steampowered.com':
            cookies.update({'sessionid': session.cookies.get(name='sessionid', domain=domain)})
            cookies.update({'steamLoginSecure': session.cookies.get(name='steamLoginSecure', domain=domain)})
            cookies.update({'birthtime': session.cookies.get(name='birthtime', domain=domain)})
        elif domain == 'help.steampowered.com':
            cookies.update({'sessionid': session.cookies.get(name='sessionid', domain=domain)})
            cookies.update({'steamLoginSecure': session.cookies.get(name='steamLoginSecure', domain=domain)})
            cookies.update({'birthtime': session.cookies.get(name='birthtime', domain=domain)})
        elif domain == 'steamcommunity.com':
            cookies.update({'sessionid': session.cookies.get(name='sessionid', domain=domain)})
            cookies.update({'steamLoginSecure': session.cookies.get(name='steamLoginSecure', domain=domain)})
            cookies.update({'birthtime': session.cookies.get(name='birthtime', domain=domain)})
        else:
            print('Unknown domain')

def send_cookies(cookies=None,new_session=None):
    if new_session:
        on_login()
        f = open('cookies.txt', 'w')
        f.writelines('sessionid ' + cookies.get('sessionid') + '\n')
        f.writelines(' steamLoginSecure ' + cookies.get('steamLoginSecure') + '\n')
        f.writelines(' birthtime ' + cookies.get('birthtime') + '\n')
        f.close()
        new_session = False
    else:
        cookies.clear()
        on_login()
        try:
            with open("cookies.txt") as file:
                for line in file:
                    key, value = line.split()
                    cookies[key] = value
        except TypeError:
            print('Type Error')
    r = requests.get(url=URL,cookies=cookies)
    return r
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
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

def get_bal(url):
    parse()
    return balance


def parse():
    html = send_cookies(cookies=cookies, new_session=True)
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

parse()