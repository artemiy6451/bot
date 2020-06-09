import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from package import parser
import requests
import time

session = requests.Session()

vk_session = vk_api.VkApi(token='6f88ad51080d9915b1b744718780f612b2b3f5e4d9cc72cf0acc9df06bd43a440b623d23b00d8ad7f93da')

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
while True:
    for event in longpoll.listen():
        while True:
            if parser.comparison() == 1:
                vk.messages.send(user_id=event.user_id, message='У вас новый предмет в инвентаре: ' + 'https://steamcommunity.com/profiles/76561198373547526/inventory/#440', random_id='0')
                time.sleep(1800)
            else:
                time.sleep(1800)