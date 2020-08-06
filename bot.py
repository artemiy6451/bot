import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from package import login
from pyowm.owm import OWM
import time
import sqlite3

session = requests.Session()

vk_session = vk_api.VkApi(token='207b5701fac3bf264fc8bdf0f2416dd4fbad3f54e07d3ca91f77db5414527f04178d5538a639dbad930fc') #Токен вк
token = 'e0e9c0ccd1fa05300b95620e16ea503f' #Токен openWeather
new = 1
flag = False
new_1 = 1
is_on = True


longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

db = sqlite3.connect('server.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
user INTEGER
)""")
db.commit()

keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
keyboard.add_button('Старт', color=VkKeyboardColor.DEFAULT)
vk.messages.send(user_id="254928937", random_id='0', message='Нажми старт', keyboard=keyboard.get_keyboard())


def comparation():
    n = 0
    for i in login.item:
        try:
            if i == login.item[n + int(len(login.item)/2)]:
                print('+')
                n += 1
            else:
                vk.messages.send(user_id=event.user_id, random_id='0', message=f'В игре {login.game[n+int(len(login.item)/2)]} новый пердмет, теперь их {login.item[n+int(len(login.item)/2)]}')
                n += 1
        except IndexError:
            break

while True:
    try:
        for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.message == 'Старт':
                        keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                        keyboard.add_button('Стим', color=VkKeyboardColor.DEFAULT)
                        keyboard.add_button('Погода', color=VkKeyboardColor.PRIMARY)
                        keyboard.add_button('Подписка', color=VkKeyboardColor.POSITIVE)
                        keyboard.add_button('Оповещения', color=VkKeyboardColor.NEGATIVE)
                        keyboard.add_line()
                        keyboard.add_button('Данные', color=VkKeyboardColor.NEGATIVE)
                        vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                         message='Главное меню')
                    if event.message == 'Стим':
                        keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                        keyboard.add_button('Баланс', color=VkKeyboardColor.DEFAULT)
                        keyboard.add_button('Инвентарь', color=VkKeyboardColor.PRIMARY)
                        keyboard.add_button('Вход', color=VkKeyboardColor.POSITIVE)
                        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                        vk.messages.send(user_id=event.user_id,
                                         keyboard=keyboard.get_keyboard(),
                                         random_id='0',
                                         message='''Стим меню''')
                        for event_2 in longpoll.listen():
                            if event_2.type == VkEventType.MESSAGE_NEW:
                                if event_2.message == 'Баланс':
                                    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                    login.main()
                                    if int(login.balance_last) < int(login.balance_new):
                                        _balance = '+' + str(int(login.balance_new) - int(login.balance_last))
                                    elif int(login.balance_last) > int(login.balance_new):
                                        _balance = '-' + str(int(login.balance_last) - int(login.balance_new))
                                    elif int(login.balance_last) == int(login.balance_new):
                                        _balance = str(int(login.balance_new) - int(login.balance_last))
                                    keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
                                    vk.messages.send(user_id=event.user_id, random_id='0',
                                                     message=f'Баланс сейчас {login.balance_new} руб, прошлый баланс {login.balance_last} руб, разница {_balance} руб.',
                                                     keyboard=keyboard.get_keyboard())
                                    for event_3 in longpoll.listen():
                                        if event_3.type == VkEventType.MESSAGE_NEW:
                                            if event_3.message == 'Назад':
                                                flag = True
                                                break
                                            if flag:
                                                break
                                        if flag:
                                            break
                                    if flag:
                                        keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                        keyboard.add_button('Баланс', color=VkKeyboardColor.DEFAULT)
                                        keyboard.add_button('Инвентарь', color=VkKeyboardColor.PRIMARY)
                                        keyboard.add_button('Вход', color=VkKeyboardColor.POSITIVE)
                                        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                                        vk.messages.send(user_id=event.user_id,
                                                         keyboard=keyboard.get_keyboard(),
                                                         random_id='0',
                                                         message='''Стим меню''')
                                        flag = False
                                if event_2.message == 'Инвентарь':
                                    try:
                                        keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                        login.main()
                                        n = 0
                                        for game in login.game:
                                            if n == 4 or n == 8 or n == 12 or n == 16 or n == 20:
                                                keyboard.add_line()
                                                keyboard.add_button(login.game[n], color=VkKeyboardColor.DEFAULT)
                                                n += 1
                                            else:
                                                keyboard.add_button(login.game[n], color=VkKeyboardColor.DEFAULT)
                                                n += 1
                                        keyboard.add_line()
                                        keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
                                        vk.messages.send(user_id=event.user_id,
                                                         keyboard=keyboard.get_keyboard(),
                                                         random_id='0',
                                                         message='Выберите игру')
                                    except:
                                        keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                        keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
                                        vk.messages.send(user_id=event.user_id,
                                                         keyboard=keyboard.get_keyboard(),
                                                         random_id='0',
                                                         message='Инвентарь пуст')
                                    for event_4 in longpoll.listen():
                                        if event_4.type == VkEventType.MESSAGE_NEW:
                                            x = 0
                                            for elements in login.game:
                                                if event_4.message == login.game[x]:
                                                    if int(login.item[x]) <= 4:
                                                        vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                                         keyboard=keyboard.get_keyboard(),
                                                                         message=f'Сейчас в инвентаре {login.item[x]} предмета.')
                                                    else:
                                                        vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                                         keyboard=keyboard.get_keyboard(),
                                                                         message=f'Сейчас в инвентаре {login.item[x]} предметов.')
                                                x += 1

                                            if event_4.message == 'Назад':
                                                flag = True
                                                break
                                            if flag:
                                                break
                                        if flag:
                                            break
                                    if flag:
                                        keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                        keyboard.add_button('Баланс', color=VkKeyboardColor.DEFAULT)
                                        keyboard.add_button('Инвентарь', color=VkKeyboardColor.PRIMARY)
                                        keyboard.add_button('Вход', color=VkKeyboardColor.POSITIVE)
                                        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                                        vk.messages.send(user_id=event.user_id,
                                                         keyboard=keyboard.get_keyboard(),
                                                         random_id='0',
                                                         message='''Стим меню''')
                                        flag = False
                                if event_2.message == 'Вход':
                                    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                    keyboard.add_button('Логин', color=VkKeyboardColor.DEFAULT)
                                    keyboard.add_button('Пароль', color=VkKeyboardColor.PRIMARY)
                                    keyboard.add_button('2FA код', color=VkKeyboardColor.POSITIVE)
                                    keyboard.add_button('Куки', color=VkKeyboardColor.POSITIVE)
                                    keyboard.add_line()
                                    keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
                                    vk.messages.send(user_id=event.user_id,
                                                     keyboard=keyboard.get_keyboard(),
                                                     random_id='0',
                                                     message='Сначала логин, затем пароль, и потом 2FA код')
                                    for event_5 in longpoll.listen():
                                        if event_5.type == VkEventType.MESSAGE_NEW:
                                            if event_5.message == 'Логин':
                                                vk.messages.send(user_id=event.user_id,
                                                                 random_id='0',
                                                                 message='Введите свой логин')
                                                time.sleep(1)
                                                for event_6 in longpoll.listen():
                                                    if event_6.type == VkEventType.MESSAGE_NEW:
                                                        if event_6.message == 'Введите свой логин':
                                                            print('1')
                                                        else:
                                                            login.username = event_6.message
                                                            flag = True
                                                            if flag:
                                                                break
                                                        if flag:
                                                            break
                                                    if flag:
                                                        break
                                                if flag:
                                                    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                                    keyboard.add_button('Логин', color=VkKeyboardColor.DEFAULT)
                                                    keyboard.add_button('Пароль', color=VkKeyboardColor.PRIMARY)
                                                    keyboard.add_button('2FA код', color=VkKeyboardColor.POSITIVE)
                                                    keyboard.add_button('Куки', color=VkKeyboardColor.POSITIVE)
                                                    keyboard.add_line()
                                                    keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
                                                    vk.messages.send(user_id=event.user_id,
                                                                     keyboard=keyboard.get_keyboard(),
                                                                     random_id='0',
                                                                     message='Теперь пароль')
                                                    flag = False
                                            if event_5.message == 'Пароль':
                                                vk.messages.send(user_id=event.user_id,
                                                                 random_id='0',
                                                                 message='Введите свой пароль')
                                                time.sleep(1)
                                                for event_7 in longpoll.listen():
                                                    if event_7.type == VkEventType.MESSAGE_NEW:
                                                        if event_7.message == 'Введите свой пароль':
                                                            print('1')
                                                        else:
                                                            login.password = event_7.message
                                                            flag = True
                                                            if flag:
                                                                break
                                                        if flag:
                                                            break
                                                    if flag:
                                                        break
                                                if flag:
                                                    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                                    keyboard.add_button('Логин', color=VkKeyboardColor.DEFAULT)
                                                    keyboard.add_button('Пароль', color=VkKeyboardColor.PRIMARY)
                                                    keyboard.add_button('2FA код', color=VkKeyboardColor.POSITIVE)
                                                    keyboard.add_button('Куки', color=VkKeyboardColor.POSITIVE)
                                                    keyboard.add_line()
                                                    keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
                                                    vk.messages.send(user_id=event.user_id,
                                                                     keyboard=keyboard.get_keyboard(),
                                                                     random_id='0',
                                                                     message='Ну и напоследок 2FA')
                                                    flag = False
                                            if event_5.message == '2FA код':
                                                vk.messages.send(user_id=event.user_id,
                                                                 random_id='0',
                                                                 message='Жду твой 2FA код')
                                                time.sleep(1)
                                                for event_8 in longpoll.listen():
                                                    if event_8.type == VkEventType.MESSAGE_NEW:
                                                        if event_8.message == 'Жду твой 2FA код':
                                                            print('1')
                                                        else:
                                                            login.two_factor_code = event_8.message
                                                            flag = True
                                                            if flag:
                                                                break
                                                        if flag:
                                                            break
                                                    if flag:
                                                        break
                                                if flag:
                                                    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                                    keyboard.add_button('Логин', color=VkKeyboardColor.DEFAULT)
                                                    keyboard.add_button('Пароль', color=VkKeyboardColor.PRIMARY)
                                                    keyboard.add_button('2FA код', color=VkKeyboardColor.POSITIVE)
                                                    keyboard.add_button('Куки', color=VkKeyboardColor.POSITIVE)
                                                    keyboard.add_line()
                                                    keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
                                                    vk.messages.send(user_id=event.user_id,
                                                                     keyboard=keyboard.get_keyboard(),
                                                                     random_id='0',
                                                                     message='Вхожу')
                                                    if new == 1:
                                                        login.main(new=True)
                                                        login.main()
                                                        new += 1
                                                    else:
                                                        vk.messages.send(user_id=event.user_id,
                                                                         keyboard=keyboard.get_keyboard(),
                                                                         random_id='0',
                                                                         message='Вы уже вошли в свой аккаунт')
                                                    flag = False
                                            if event_5.message == 'Куки':
                                                login.main()
                                                login.main()
                                                print(len(login.balance_last))
                                                if int(login.balance_last) == 0:
                                                    flag = True
                                                if flag:
                                                    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                                    keyboard.add_button('Логин', color=VkKeyboardColor.DEFAULT)
                                                    keyboard.add_button('Пароль', color=VkKeyboardColor.PRIMARY)
                                                    keyboard.add_button('2FA код', color=VkKeyboardColor.POSITIVE)
                                                    keyboard.add_button('Куки', color=VkKeyboardColor.POSITIVE)
                                                    keyboard.add_line()
                                                    keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
                                                    vk.messages.send(user_id=event.user_id,
                                                                     keyboard=keyboard.get_keyboard(),
                                                                     random_id='0',
                                                                     message='Кукки не действительны\nПожалуйста войдите в аккаунт')
                                                    flag = False
                                                elif int(login.balance_last) > 0:
                                                    flag = True
                                                if flag:
                                                    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                                    keyboard.add_button('Логин', color=VkKeyboardColor.DEFAULT)
                                                    keyboard.add_button('Пароль', color=VkKeyboardColor.PRIMARY)
                                                    keyboard.add_button('2FA код', color=VkKeyboardColor.POSITIVE)
                                                    keyboard.add_button('Куки', color=VkKeyboardColor.POSITIVE)
                                                    keyboard.add_line()
                                                    keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
                                                    vk.messages.send(user_id=event.user_id,
                                                                     keyboard=keyboard.get_keyboard(),
                                                                     random_id='0',
                                                                     message='Вы успешно вошли')
                                                    flag = False
                                            if event_5.message == 'Назад':
                                                flag = True
                                                if flag:
                                                    break
                                            if flag:
                                                break
                                        if flag:
                                            break
                                    if flag:
                                        keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                        keyboard.add_button('Баланс', color=VkKeyboardColor.DEFAULT)
                                        keyboard.add_button('Инвентарь', color=VkKeyboardColor.PRIMARY)
                                        keyboard.add_button('Вход', color=VkKeyboardColor.POSITIVE)
                                        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                                        vk.messages.send(user_id=event.user_id,
                                                         keyboard=keyboard.get_keyboard(),
                                                         random_id='0',
                                                         message='''Стим меню''')
                                        flag = False
                                if event_2.message == 'Назад':
                                    flag = True
                                    if flag:
                                        break
                                if flag:
                                    break
                            if flag:
                                break
                        if flag:
                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                            keyboard.add_button('Стим', color=VkKeyboardColor.DEFAULT)
                            keyboard.add_button('Погода', color=VkKeyboardColor.PRIMARY)
                            keyboard.add_button('Подписка', color=VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Оповещения', color=VkKeyboardColor.NEGATIVE)
                            keyboard.add_line()
                            keyboard.add_button('Данные', color=VkKeyboardColor.NEGATIVE)
                            vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                             message='Главное меню')
                            flag = False
                    if event.message == 'Погода':
                        vk.messages.send(user_id=event.user_id, random_id='0', message='В каком городе?')
                        for event_4 in longpoll.listen():
                            if event_4.type == VkEventType.MESSAGE_NEW:
                                if event_4.message == 'В каком городе?':
                                    pass
                                else:
                                    city = event_4.message
                                    owm = OWM(api_key=token)
                                    mgr = owm.weather_manager()
                                    observation = mgr.weather_at_place(city)
                                    w = observation.weather
                                    vk.messages.send(user_id=event.user_id, random_id='0',
                                                     message=f'''
        Сейчас температура {str(w.temperature('celsius')['temp'])} градусов.
        Ощущается как {str(w.temperature('celsius')['feels_like'])} градусов.
        Влажность {str(w.humidity)}%.
        Ветер {str(w.wind()['speed'])} м/c.
        ''')
                                    flag = True
                                    if flag:
                                        break
                                if flag:
                                    break
                            if flag:
                                break
                        if flag:
                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                            keyboard.add_button('Стим', color=VkKeyboardColor.DEFAULT)
                            keyboard.add_button('Погода', color=VkKeyboardColor.PRIMARY)
                            keyboard.add_button('Подписка', color=VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Оповещения', color=VkKeyboardColor.NEGATIVE)
                            keyboard.add_line()
                            keyboard.add_button('Данные', color=VkKeyboardColor.NEGATIVE)
                            vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                             message='Главное меню')
                            flag = False
                    if event.message == 'Подписка':
                        sql.execute('SELECT user FROM users')
                        if sql.fetchone() is None:
                            sql.execute(f'INSERT INTO users VALUES("{event.user_id}")')
                            db.commit()
                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                            keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                            vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                             message='Вы успешно подписались на рассылку')
                            for event1 in longpoll.listen():
                                if event1.type == VkEventType.MESSAGE_NEW:
                                    if event1.message == 'Назад':
                                        flag = True
                                        if flag:
                                            break
                                    if flag:
                                        break
                                if flag:
                                    break
                            if flag:
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button('Стим', color=VkKeyboardColor.DEFAULT)
                                keyboard.add_button('Погода', color=VkKeyboardColor.PRIMARY)
                                keyboard.add_button('Подписка', color=VkKeyboardColor.POSITIVE)
                                keyboard.add_button('Оповещения', color=VkKeyboardColor.NEGATIVE)
                                keyboard.add_line()
                                keyboard.add_button('Данные', color=VkKeyboardColor.NEGATIVE)
                                vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                                 message='Главное меню')
                                flag = False
                        else:
                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                            keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
                            keyboard.add_button('Отписаться', color=VkKeyboardColor.NEGATIVE)
                            vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                             message='Вы уже подписаны на рассылку')
                            for event_10 in longpoll.listen():
                                if event_10.type == VkEventType.MESSAGE_NEW:
                                    if event_10.message == 'Отписаться':
                                        sql.execute(f'DELETE FROM users WHERE {event.user_id}')
                                        db.commit()
                                        keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                                        vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(),
                                                         random_id='0',
                                                         message='Вы успешно отписались')
                                        for event_11 in longpoll.listen():
                                            if event_11.type == VkEventType.MESSAGE_NEW:
                                                if event_11.message == 'Назад':
                                                    flag = True
                                                    if flag:
                                                        break
                                                if flag:
                                                    break
                                            if flag:
                                                break
                                        if flag:
                                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                            keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                                            vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(),
                                                             random_id='0',
                                                             message='А зачем тебе это надо, может подпишишься?(')
                                            flag = False


                                    if event_10.message == 'Назад':
                                        flag = True
                                        if flag:
                                            break
                                    if flag:
                                        break
                                if flag:
                                    break
                            if flag:
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button('Стим', color=VkKeyboardColor.DEFAULT)
                                keyboard.add_button('Погода', color=VkKeyboardColor.PRIMARY)
                                keyboard.add_button('Подписка', color=VkKeyboardColor.POSITIVE)
                                keyboard.add_button('Оповещения', color=VkKeyboardColor.NEGATIVE)
                                keyboard.add_line()
                                keyboard.add_button('Данные', color=VkKeyboardColor.NEGATIVE)
                                vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                                 message='Главное меню')
                                flag = False
                    if event.message == 'Оповещения':
                        msg = 'Напишите сколько сделать проверок\nУчтите, что пока все проверки не выполняться вы не сможете пользоваться ботом\nПроверка делаеться раз в 6 минут\nРекомендуемое число от 5-10'

                        vk.messages.send(user_id=event.user_id, random_id='0',
                                         message=msg)
                        time.sleep(1)
                        for event_13 in longpoll.listen():
                            if event_13.type == VkEventType.MESSAGE_NEW:
                                if event_13.message == msg:
                                    print('1')
                                else:
                                    for i in range(int(event_13.message)):
                                        if new_1 == 1:
                                            login.main()
                                            login.main()
                                            new_1 += 1
                                        else:
                                            login.main()
                                        comparation()
                                        time.sleep(360)
                                    flag = True
                                    if flag:
                                        break
                                if flag:
                                    break
                            if flag:
                                break
                        if flag:
                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                            keyboard.add_button('Стим', color=VkKeyboardColor.DEFAULT)
                            keyboard.add_button('Погода', color=VkKeyboardColor.PRIMARY)
                            keyboard.add_button('Подписка', color=VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Оповещения', color=VkKeyboardColor.NEGATIVE)
                            keyboard.add_line()
                            keyboard.add_button('Данные', color=VkKeyboardColor.NEGATIVE)
                            vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                             message='Провекра закончилась')
                            login.main()
                            new_1 = 1
                    if event.message == 'Данные':
                        for i in range(2):
                            if i == 0:
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                                vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                                 message=f'Логин: {login.username}')
                            elif i == 1:
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                                vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                                 message=f'Пароль: {login.password}')
                        for eventm in longpoll.listen():
                            if eventm.type == VkEventType.MESSAGE_NEW:
                                if eventm.message == 'Назад':
                                    flag = True
                                    break
                                if flag:
                                    break
                            if flag:
                                break
                        if flag:
                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                            keyboard.add_button('Стим', color=VkKeyboardColor.DEFAULT)
                            keyboard.add_button('Погода', color=VkKeyboardColor.PRIMARY)
                            keyboard.add_button('Подписка', color=VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Оповещения', color=VkKeyboardColor.NEGATIVE)
                            keyboard.add_line()
                            keyboard.add_button('Данные', color=VkKeyboardColor.NEGATIVE)
                            vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                             message='Главное меню')
                            flag = False

    except:
        print(Exception)
        try:
            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
            keyboard.add_button('Стим', color=VkKeyboardColor.DEFAULT)
            keyboard.add_button('Погода', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('Подписка', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('Оповещения', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button('Данные', color=VkKeyboardColor.NEGATIVE)
            vk.messages.send(user_id="254928937", random_id='0',
                             message=f'Случилась ошибка', keyboard=keyboard.get_keyboard())
        except:
            pass
