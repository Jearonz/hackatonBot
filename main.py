import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import threading


MAIN_TOKEN = 'vk1.a.KB9CdWn7SuKE2KmFH1uA_p4MOHkhNeg58H7A9n_sLkRzQ5k5nA5Kt4YpXb5zCh0oHmVpMv3-UkJOSqzQ02Lk3ZNjt0DgTG5Imozeyx6uhYamyCAWY4Kt1JUj72eGdtKbc2Dx8SOFRlj7kOH0kiSz2-Ke3xMbLFQ4wmgdIVVBSGpwGRw_gW8nfBQI1L2pHNRsIbFuzbMRyv98O_zRVwj3jQ'
OWNER_TOKEN = 'vk1.a.XVjgiLNTQtrLs00Raha2V1vWIT4GTGA5nt-EHME3aejya4rpDyL8iA3zYH-BYZeD7GBs86qqylJLFCnog9DE14FZ_mi8OMsqqkqviMLDUWqLQ7-PSEoT5aFo5pJOVT4JCcDqUwpgJ_7WFlPJVfyMkxbreed4m3uAToC2gBLaqIe-nIksW-3LWdQ7zlXuZ-u5J8eygrtkp8dc_dDdu3x-bQ'
textOfPost = ''
OWNER_ID = -217764821
POST = False
ID_POST = None
NEW_REQUEST = False
ADMINS_ACTIVE = []
# ID_OF_USER_REQUEST = 0

# Press the green button in the gutter to run the script.

vk_session = vk_api.VkApi(token=MAIN_TOKEN)
vk_session_admin = vk_api.VkApi(token=OWNER_TOKEN)
sessionApi = vk_session.get_api()
sessionApiAdmin = vk_session_admin.get_api()
longpoll = VkLongPoll(vk_session)
longpollAdmin = VkLongPoll(vk_session_admin)



# f = open('keyboard.json', 'r')
# test = f.read()

try:
    f = open('users.txt', 'r')
    f.close()
except IOError as e:
    f = open('users.txt', 'wr')
    f.close()
finally:
    f = open('users.txt', 'r')
    users = f.read()
    print(users)
    usersArray = users.split(',')
    print(usersArray)
    f.close()

    f = open('admins.txt', 'r')
    admins = f.read()
    adminsArray = admins.split(',')
    f.close()

def sender(id, text):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})

def sendPost(id, attachment):
    vk_session.method('messages.send', {'user_id': id, 'attachment': attachment, 'random_id': 0})

def creatPost(id, text):
    idPost = vk_session_admin.method('wall.post',{'owner_id': id, 'message': text, "random_id": 0})
    return idPost
def sendNewPost():
    for userId in usersArray:
        sendPost(int(userId), 'wall' + str(OWNER_ID) +'_' + str(ID_POST['post_id']))

def sendNewRequest(msg):
    for adminId in adminsArray:
        sender(adminId, msg)

#def getURI(chat_id):


for event in longpoll.listen():
    # print(event.attachments)
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if POST == True and event.text.lower() != 'отмена':
                textOfPost = event.text
                # if event.attachments: attachments = event.attachments['attach1_type'] + event.attachments['attach1']
                ID_POST = creatPost(OWNER_ID, textOfPost)
                print(ID_POST)
                POST = False
                sender(event.user_id, 'Я сделал пост')
                sendNewPost()
            elif POST == True:
                sender(event.user_id, 'Отмена постинга')
                POST = False

            if NEW_REQUEST == True and event.text.lower() != 'отмена':
                sendNewRequest('Пользователь оставил заявку: "' + event.text + '"  \nCсылка на пользователя: https://vk.com/' + str(event.user_id))
                NEW_REQUEST = False


            msg = event.text.lower()
            id = event.user_id
            idString = str(id)
            if idString not in users:
                usersArray.append(idString)
                f = open('users.txt', 'w')
                f.write('')
                f.close()
                f = open('users.txt', 'a')
                for userId in usersArray:
                    f.write(str(userId))
                    if userId != usersArray[-1] and userId != '':
                        f.write(',')
                f.close()
                print(usersArray)
            if msg == 'привет':
                sender(id, 'и тебе привет')
            if msg == 'пост':
                print(adminsArray)
                if str(id) in ADMINS_ACTIVE:
                    sender(id, 'Введите текст поста, для отмены введите "отмена"')
                    POST = True
                elif str(id) in adminsArray:
                    sender(id, 'Вы не вошли в панель администратора')
                else:
                    sender(id, 'Вы не админ')

            if msg == 'оставить заявку':
                sender(id, 'Введите текст заявки, для отмены введите "отмена"')
                NEW_REQUEST = True


            if msg == 'админ' and str(id) in adminsArray:
                sender(id, 'Вы вошли в панель админа')
                ADMINS_ACTIVE.append(str(id))

            if msg == 'выход' and str(id) in ADMINS_ACTIVE:
                sender(id, 'Вы вышли из панели администратора')
                ADMINS_ACTIVE.remove(str(id))