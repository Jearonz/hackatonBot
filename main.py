import json

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


def update_keyboard():
    f = open('admissions_information/AIT.txt', 'r')
    while True:
        s = f.readline()
        if not s:
            break
        a = s.split(',')
        new_data = [{"action": {"type": "text", "payload": "{\"button\": \"1\"}", "label": a[1]}, "color": "secondary"}]
        with open('keyboards/keyboard_courses.json', encoding='utf8') as f1:
            data = json.load(f1)
            if new_data not in data["buttons"]:
                data["buttons"].insert(0, new_data)
                with open('keyboards/keyboard_courses.json', 'w', encoding='utf8') as outfile:
                    json.dump(data, outfile, ensure_ascii=False, indent=2)


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


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == 'начать':
                sender(id, 'Главное меню:', get_keyboard('keyboards/keyboard_main.json'))
            if msg == 'информация о приемной комиссии':
                sender(id, 'Выберите действие', get_keyboard('keyboards/keyboard_second.json'))
            if msg == 'в главное меню':
                sender(id, 'Главное меню: ', get_keyboard('keyboards/keyboard_main.json'))
            if msg == 'направления подготовки и специальности':
                update_keyboard()
                sender(id, 'Выберите направление:', get_keyboard('keyboards/keyboard_courses.json'))
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

