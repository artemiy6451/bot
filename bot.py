import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from package import login
from pyowm.owm import OWM
import time

session = requests.Session()

vk_session = vk_api.VkApi(token='6f88ad51080d9915b1b744718780f612b2b3f5e4d9cc72cf0acc9df06bd43a440b623d23b00d8ad7f93da')
token = 'e0e9c0ccd1fa05300b95620e16ea503f'
new = 1
flag = False

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
keyboard.add_button('Старт', color=VkKeyboardColor.DEFAULT)
vk.messages.send(user_id="254928937", random_id='0', message='Нажми старт', keyboard=keyboard.get_keyboard())

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.message == 'Старт':
                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                keyboard.add_button('Стим', color=VkKeyboardColor.DEFAULT)
                keyboard.add_button('Погода', color=VkKeyboardColor.PRIMARY)
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
                            print(login.balance[-1])
                            if int(login.balance[0]) > int(login.balance[-1]):
                                _balance = str(int(login.balance[0]) - int(login.balance[-1]))
                            elif int(login.balance[0]) < int(login.balance[-1]):
                                _balance = str(int(login.balance[0]) + int(login.balance[-1]))
                            elif int(login.balance[0]) == int(login.balance[-1]):
                                _balance = str(int(login.balance[0]) - int(login.balance[-1]))
                            keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
                            vk.messages.send(user_id=event.user_id, random_id='0',
                                             message=f'Баланс сейчас {login.balance[-1]} руб, прошлый баланс {login.balance[0]} руб, разница {_balance} руб.',
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
                            for event_4 in longpoll.listen():
                                if event_4.type == VkEventType.MESSAGE_NEW:
                                    if event_4.message == login.game[0]:
                                        if int(login.item[0]) <= 4:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[0]} предмета.')
                                        else:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[0]} предметов.')

                                    if event_4.message == login.game[1]:
                                        if int(login.item[1]) <= 4:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[1]} предмета.')
                                        else:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[1]} предметов.')

                                    if event_4.message == login.game[2]:
                                        if int(login.item[2]) <= 4:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[2]} предмета.')
                                        else:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[2]} предметов.')

                                    if event_4.message == login.game[3]:
                                        if int(login.item[3]) <= 4:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[3]} предмета.')
                                        else:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[3]} предметов.')

                                    if event_4.message == login.game[4]:
                                        if int(login.item[4]) <= 4:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[4]} предмета.')
                                        else:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[4]} предметов.')

                                    if event_4.message == login.game[5]:
                                        if int(login.item[5]) <= 4:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[5]} предмета.')
                                        else:
                                            vk.messages.send(user_id=event_2.user_id, random_id='0',
                                                             keyboard=keyboard.get_keyboard(),
                                                             message=f'Сейчас в инвентаре {login.item[5]} предметов.')

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
                                                    login.twofactor_code = event_8.message
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
                                                new += 1
                                            else:
                                                vk.messages.send(user_id=event.user_id,
                                                                 keyboard=keyboard.get_keyboard(),
                                                                 random_id='0',
                                                                 message='Вы уже вошли в свой аккаунт')
                                            flag = False
                                    if event_5.message ==  'Куки':
                                        login.main()
                                        print(len(login.balance))
                                        if len(login.balance) == 0:
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
                                        elif len(login.balance) > 0:
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
                    vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), random_id='0',
                                     message='Главное меню')
                    flag = False

