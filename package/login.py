import steam.webauth as wa
import requests
from bs4 import BeautifulSoup

url = '' #Ссылка на инвентарь
username = '' #Логин(не обязательно)
password = '' #Пароль(не обязательно)
two_factor_code = ''
session = None
cookies = {}
game = []
item = []
info = []
bal = []
balance_new = 0
balance_last = 0
count_games = 0
i = True


def login():
    global session
    user = wa.WebAuth(username=username)
    session = user.login(password=password, twofactor_code=two_factor_code)
    return session


def on_login(first_login=False):
    global session
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


def send_cookies(cookies=None, new_session=False):
    if new_session:
        on_login(first_login=True)
        f = open('test.txt', 'w')
        f.writelines('sessionid ' + cookies.get('sessionid') + '\n')
        f.writelines(' steamLoginSecure ' + cookies.get('steamLoginSecure') + '\n')
        f.writelines(' birthtime ' + cookies.get('birthtime') + '\n')
        f.close()
        new_session = False
    else:
        cookies.clear()
        on_login()
        try:
            with open("test.txt") as file:
                for line in file:
                    key, value = line.split()
                    cookies[key] = value
        except TypeError:
            print('Файл пустой')
            send_cookies(cookies=cookies, new_session=True)
    r = requests.get(url=url, cookies=cookies)
    return r


def choice():
    choice_ = input('Использовать куки или войти?\n1.Куки\n2.Войти\n')
    if choice_ == '1':
        send_cookies(cookies=cookies, new_session=False)
    elif choice_ == '2':
        send_cookies(cookies=cookies, new_session=True)
    else:
        print('Unknown choice')

def get_content(html):
    global i, count_games
    soup = BeautifulSoup(html, 'html.parser')
    games = soup.find_all('span', class_="games_list_tab_name")
    items = soup.find_all('span', class_="games_list_tab_number")
    for el in games:
        game.append(el.get_text(strip=True))
    for it in items:
        item.append(it.get_text(strip=True).replace('(','').replace(')',''))

    n = 0
    try:
        for all in game:
            info.append({
                all : item[n]
            })
            n +=1
    except: pass

    if i:
        i = False
        count_games = int(len(game))
    else:
        del info[0:-count_games * 2]
        games.clear()
        items.clear()
        del item[0:-count_games * 2]
        del game[0:-count_games]
    print(info)
    return info

def get_bal(html):
    global balance_last, balance_new
    soup = BeautifulSoup(html, 'html.parser')
    bal_1 = soup.find_all('a', class_="global_action_link", id='header_wallet_balance')
    for b in bal_1:
        bal.append(b.get_text(strip=True).replace(' pуб.', ''))
    del bal[0:-2]
    balance_last = bal[0][:-3]
    try:
        balance_new = bal[1][:-3]
    except:
        pass
    print(balance_last, balance_new)


def main(new = False):
    html = send_cookies(cookies=cookies, new_session=new)
    if html.ok:
        get_content(html.text)
        get_bal(html.text)

