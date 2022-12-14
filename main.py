import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# from token import main_token


MAIN_TOKEN = 'vk1.a.KB9CdWn7SuKE2KmFH1uA_p4MOHkhNeg58H7A9n_sLkRzQ5k5nA5Kt4YpXb5zCh0oHmVpMv3-UkJOSqzQ02Lk3ZNjt0DgTG5Imozeyx6uhYamyCAWY4Kt1JUj72eGdtKbc2Dx8SOFRlj7kOH0kiSz2-Ke3xMbLFQ4wmgdIVVBSGpwGRw_gW8nfBQI1L2pHNRsIbFuzbMRyv98O_zRVwj3jQ'
# Press the green button in the gutter to run the script.

vk_session = vk_api.VkApi(token=MAIN_TOKEN)
sessionApi = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

f = open('keyboard.json', 'r')
test = f.read()
def sender(id, text):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'keyboard': test,'random_id': 0})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == 'привет':
                sender(id, 'и тебе привет')
