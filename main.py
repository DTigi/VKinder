from random import randrange
import datetime
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import user_token, community_token
from users_db import insert_users

# token = input('Token: ')
user = 777063101

vk = vk_api.VkApi(token=community_token) # авторизация сообщества
longpoll = VkLongPoll(vk) # работа с сообщениями сообщества

def write_msg(user_id, message):
    """Функция для отправки сообщений"""
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#
#         if event.to_me:
#             request = event.text
#
#             if request == "привет":
#                 write_msg(event.user_id, f"Хай, {event.user_id}")
#             elif request == "пока":
#                 write_msg(event.user_id, "Пока((")
#             else:
#                 write_msg(event.user_id, "Не поняла вашего ответа...")


def get_user_info(user_id):
    """Получение информации о пользователе, который написал боту"""
    url = 'https://api.vk.com/method/users.get'
    params = {'access_token': user_token,
              'user_ids': user_id,
              'fields': 'bdate, sex, city',
              'v': '5.131'
    }
    resp = requests.get(url, params=params)
    response = resp.json()
    birthdate = response['response'][0]['bdate']
    birthyear = int(birthdate[-4:])
    year_now = int(datetime.date.today().year)
    target_age = year_now - birthyear

    sex = response['response'][0]['sex']
    if sex == 1:
        target_sex = 2
    else:
        target_sex = 1
    city_id = response['response'][0]['city']['id']
    return target_age, target_sex, city_id


print(get_user_info(user))


def find_user(user_id):
    """Поиск людей, на основании полученных данных о пользователе (поиск пары)"""
    url = f'https://api.vk.com/method/users.search'
    params = {'access_token': user_token,
              'v': '5.131',
              'age_from': get_user_info(user_id)[0],
              'age_to': get_user_info(user_id)[0],
              'sex': get_user_info(user_id)[1],
              'city_id': get_user_info(user_id)[2],
              #'fields': 'is_closed, id, first_name, last_name',
              'status': '1' or '6' or '0',
              'count': 5}
    resp = requests.get(url, params=params)
    response = resp.json()

    dict_1 = response['response']
    list_1 = dict_1['items']
    for person_dict in list_1:
        if person_dict.get('is_closed') == False:
            first_name = person_dict.get('first_name')
            last_name = person_dict.get('last_name')
            vk_id = str(person_dict.get('id'))
            vk_link = 'vk.com/id' + str(person_dict.get('id'))
            insert_users(first_name, last_name, vk_id, vk_link)
        else:
            continue

    print(response)


find_user(user)


def get_photos_id(user_id):
    """получение ID фотографий пользователя с ранжированием по кол-ву лайков в обратном порядке (от большего к меньшему)"""
    url = 'https://api.vk.com/method/photos.getAll'
    params = {'access_token': user_token,
              'owner_id': user_id,
              'extended': 1,
              'count': 25,
              'v': '5.131'}
    resp = requests.get(url, params=params)
    response = resp.json()
    print(response)

    dict_photos = dict()
    dict_1 = response['response']
    list_1 = dict_1['items']
    for i in list_1:
        photo_id = str(i.get('id'))
        i_likes = i.get('likes')
        if i_likes.get('count'):
            likes = i_likes.get('count')
            dict_photos[likes] = photo_id
    list_of_ids = sorted(dict_photos.items(), reverse=True)
    return list_of_ids

get_photos_id(user)


