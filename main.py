import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

MAIN_TOKEN = 'vk1.a.KB9CdWn7SuKE2KmFH1uA_p4MOHkhNeg58H7A9n_sLkRzQ5k5nA5Kt4YpXb5zCh0oHmVpMv3-UkJOSqzQ02Lk3ZNjt0DgTG5Imozeyx6uhYamyCAWY4Kt1JUj72eGdtKbc2Dx8SOFRlj7kOH0kiSz2-Ke3xMbLFQ4wmgdIVVBSGpwGRw_gW8nfBQI1L2pHNRsIbFuzbMRyv98O_zRVwj3jQ'
# Press the green button in the gutter to run the script.

vk_session = vk_api.VkApi(token=MAIN_TOKEN)
sessionApi = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def get_keyboard(file):
    f = open(file, 'r')
    keyboard = f.read()
    f.close()
    return keyboard


def sender(id, text, keyboard):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'keyboard': keyboard, 'random_id': 0})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == 'привет':
                sender(id, 'и тебе привет', get_keyboard('keyboard_main.json'))
            if msg == 'информация о приемной комиссии':
                sender(id, 'test', get_keyboard('keyboard_second.json'))
            if msg == '':
                sender(id, 'test', get_keyboard('keyboard_third.json'))
            if msg == 'в главное меню':
                sender(id, 'test2', get_keyboard('keyboard_main.json'))
