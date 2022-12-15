import json

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
# Press the green button in the gutter to run the script.

vk_session = vk_api.VkApi(token=MAIN_TOKEN)
vk_session_admin = vk_api.VkApi(token=OWNER_TOKEN)
sessionApi = vk_session.get_api()
sessionApiAdmin = vk_session_admin.get_api()
longpoll = VkLongPoll(vk_session)
longpollAdmin = VkLongPoll(vk_session_admin)

def get_keyboard(file):
    f = open(file, 'r')
    keyboard = f.read()
    f.close()
    return keyboard

def sendNewRequest(msg):
    for adminId in adminsArray:
        sender(adminId, msg)

def getURI(userId):
    list = vk_session.method('groups.getMembers', {'group_id': 217764821, 'fields': 'domain'})
    for item in list['items']:
        if (str(userId) == str(item['id'])):
            return item['domain']
    return False

def sender(id, text, keyboard):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'keyboard': keyboard, 'random_id': 0})


def send_faq(id, text, keyboard):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'keyboard': keyboard, 'random_id': 0})


def read_file(file):
    f = open(file, 'r')
    s = ''
    while True:
        line = f.readline()
        if not line:
            break
        s += line
    f.close()
    return s


f = open('txt_files/FAQ.txt', 'r')
faq = []
faq_part = ''
while True:
    line = f.readline()
    if line == '___\n':
        faq.append(faq_part)
        faq_part = ''
        continue
    if not line:
        break
    faq_part += line
f.close()


def get_faculty_contacts(faculty):
    s = ''
    if faculty == 'аит':
        f = open('txt_contacts/AIT_contacts.txt')
    if faculty == 'тэс':
        f = open('txt_contacts/TES_contacts.txt')
    if faculty == 'фбфо':
        f = open('txt_contacts/FBFO_contacts.txt')
    if faculty == 'пгс':
        f = open('txt_contacts/PGS_contacts.txt')
    if faculty == 'тс':
        f = open('txt_contacts/TS_contacts.txt')
    if faculty == 'эим':
        f = open('txt_contacts/EIM_contacts.txt')
    if faculty == 'упл':
        f = open('txt_contacts/UPL_contacts.txt')
    while True:
        line = f.readline()
        if not line:
            break
        s += line
    f.close()
    return s

def get_list_of_specs(spec):
    f = open('admissions_information/spec.txt', 'r')
    s = ''
    while True:
        line = f.readline()
        a = line.split(';')
        if a[0] == spec:
            s += line + '\n'
        if not line:
            break
    return s

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
        sender(adminId, msg, get_keyboard('keyboards/keyboard_admin.json'))

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            if POST == True and event.text.lower() != 'отмена':
                textOfPost = event.text
                ID_POST = creatPost(OWNER_ID, textOfPost)
                print(ID_POST)
                POST = False
                sender(event.user_id, 'Я сделал пост', get_keyboard('keyboards/keyboard_admin.json'))
                sendNewPost()
            elif POST == True:
                sender(event.user_id, 'Отмена постинга', get_keyboard('keyboards/keyboard_admin.json'))
                POST = False

            if NEW_REQUEST == True and event.text.lower() != 'отмена':
                getLink = getURI(event.user_id)
                trueLink = '"  \nCсылка на пользователя: https://vk.com/' + str(getLink)
                link = trueLink if getURI(event.user_id) else '\n ссылку не удалось найти, проверьте сообщения сообщества'
                sendNewRequest('Пользователь оставил заявку: "' + event.text + link)
                NEW_REQUEST = False
            elif NEW_REQUEST == True:
                sender(event.user_id, 'Заявка отменена', get_keyboard('keyboards/keyboard_main.json'))
                NEW_REQUEST = False

            msg = event.text.lower()
            id = event.user_id
            if msg == 'автоматизация и ит':
                sender(id, get_list_of_specs('Автоматизация и интеллектуальные технологии '), get_keyboard('keyboards/keyboard_branch.json'))
            if msg == 'админ':
                sender(id, 'Главное меню админа', get_keyboard('keyboards/keyboard_admin.json'))
            if msg == 'промышленное и гражданское строительство':
                sender(id, get_list_of_specs('Промышленное и гражданское строительство '), get_keyboard('keyboards/keyboard_branch.json'))
            if msg == 'транспортное строительство':
                sender(id, get_list_of_specs('Транспортное строительство '), get_keyboard('keyboards/keyboard_branch.json'))
            if msg == 'транспортные и энергетические системы':
                sender(id, get_list_of_specs('Транспортные и энергетические системы '), get_keyboard('keyboards/keyboard_branch.json'))
            if msg == 'управление перевозками и логистика':
                sender(id, get_list_of_specs('Управление перевозками и логистика '), get_keyboard('keyboards/keyboard_branch.json'))
            if msg == 'факультет безотрывных форм обучения':
                sender(id, get_list_of_specs('Факультет безотрывных форм обучения '), get_keyboard('keyboards/keyboard_branch.json'))
            if msg == 'экономика и менеджмент':
                sender(id, get_list_of_specs('Экономика и менеджмент '), get_keyboard('keyboards/keyboard_branch.json'))
            if msg == 'начать':
                sender(id, 'Главное меню:', get_keyboard('keyboards/keyboard_main.json'))
            if msg == 'информация о приемной комиссии':
                sender(id, 'Выберите действие', get_keyboard('keyboards/keyboard_second.json'))
            if msg == 'в главное меню':
                sender(id, 'Главное меню: ', get_keyboard('keyboards/keyboard_main.json'))
            if msg == 'направления подготовки и специальности':
                sender(id, 'Выберите направление:', get_keyboard('keyboards/keyboard_branch.json'))
            if msg == 'прочее':
                sender(id, 'Выберите нужную вам информацию: ', get_keyboard('keyboards/keyboard_info.json'))
            if msg == 'вопросы и ответы':
                send_faq(id, faq[0], get_keyboard('keyboards/keyboard_info.json'))
                send_faq(id, faq[1], get_keyboard('keyboards/keyboard_info.json'))
                send_faq(id, faq[2], get_keyboard('keyboards/keyboard_info.json'))
            if msg == 'об университете':
                sender(id, read_file('txt_files/about_university.txt'), get_keyboard('keyboards/keyboard_info.json'))
            if msg == 'контакты':
                sender(id, 'Выберите пункт меню: ', get_keyboard('keyboards/keyboard_contacts.json'))
            if msg == 'контактная информация':
                sender(id, read_file('txt_contacts/contact_info.txt'), get_keyboard('keyboards/keyboard_contacts.json'))
            if msg == 'контакты факультетов':
                sender(id, 'Выберите факультет: ', get_keyboard('keyboards/keyboard_contacts_faculties.json'))
            if msg == 'аит':
                sender(id, get_faculty_contacts(msg), get_keyboard('keyboards/keyboard_contacts_faculties.json'))
            if msg == 'тэс':
                sender(id, get_faculty_contacts(msg), get_keyboard('keyboards/keyboard_contacts_faculties.json'))
            if msg == 'тс':
                sender(id, get_faculty_contacts(msg), get_keyboard('keyboards/keyboard_contacts_faculties.json'))
            if msg == 'пгс':
                sender(id, get_faculty_contacts(msg), get_keyboard('keyboards/keyboard_contacts_faculties.json'))
            if msg == 'фбфо':
                sender(id, get_faculty_contacts(msg), get_keyboard('keyboards/keyboard_contacts_faculties.json'))
            if msg == 'эим':
                sender(id, get_faculty_contacts(msg), get_keyboard('keyboards/keyboard_contacts_faculties.json'))
            if msg == 'упл':
                sender(id, get_faculty_contacts(msg), get_keyboard('keyboards/keyboard_contacts_faculties.json'))
            if msg == 'платные образовательные услуги':
                sender(id, 'https://www.pgups.ru/sveden/paid_edu/', get_keyboard('keyboards/keyboard_main.json'))
            if msg == 'информация о дополнительном образовании':
                sender(id, 'Выберите услугу: ', get_keyboard('keyboards/keyboard_additional_education.json'))
            if msg == 'институт прикладной экономики':
                sender(id, read_file('txt_files/about_university.txt'), get_keyboard('keyboards/keyboard_additional_education.json'))
            if msg == 'центр развития жд перевозок':
                sender(id, read_file('txt_files/education_center.txt'), get_keyboard('keyboards/keyboard_additional_education.json'))
            if msg == 'центр транспортной безопасности':
                sender(id, read_file('txt_files/transport_secure_centre.txt'), get_keyboard('keyboards/keyboard_additional_education.json'))
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

            if msg == 'сделать пост':
                if str(id) in ADMINS_ACTIVE:
                    sender(id, 'Введите текст поста, для отмены введите "отмена"', get_keyboard('keyboards/keyboard_admin_post.json'))
                    POST = True
                elif str(id) in adminsArray:
                    sender(id, 'Вы не вошли в панель администратора', get_keyboard('keyboards/keyboard_admin.json'))
                else:
                    sender(id, 'Вы не админ', get_keyboard('keyboards/keyboard_main.json'))
            if msg == 'даты приемной комиссии':
                sender(id, 'testdate', get_keyboard('keyboards/keyboard_second.json'))

            if msg == 'оставить заявку':
                sender(id, 'Введите текст заявки, для отмены введите "отмена"',get_keyboard('keyboards/keyboard_main.json'))
                NEW_REQUEST = True

            if msg == 'админ' and str(id) in adminsArray:
                sender(id, 'Вы вошли в панель админа',get_keyboard('keyboards/keyboard_admin.json'))
                ADMINS_ACTIVE.append(str(id))

            if msg == 'выход' and str(id) in ADMINS_ACTIVE:
                sender(id, 'Вы вышли из панели администратора', get_keyboard('keyboards/keyboard_main.json'))
                ADMINS_ACTIVE.remove(str(id))