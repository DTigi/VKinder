from random import randrange
import datetime
import requests
import vk_api
from vk_api.longpoll import VkLongPoll
from config import user_token, community_token
from users_db import insert_users, insert_viewed_users, user_selection, update_viewed_users, drop_table



# token = input('Token: ')
user = 777063101

vk = vk_api.VkApi(token=community_token)  # авторизация сообщества
longpoll = VkLongPoll(vk)  # работа с сообщениями сообщества


def write_msg(user_id, message):
    """Функция для отправки сообщений"""
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})




def get_profile_info(user_id):
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


def find_user(user_id):
    """Поиск людей, на основании полученных данных о пользователе (поиск пары)"""
    url = f'https://api.vk.com/method/users.search'
    params = {'access_token': user_token,
              'v': '5.131',
              'age_from': get_profile_info(user_id)[0],
              'age_to': get_profile_info(user_id)[0],
              'sex': get_profile_info(user_id)[1],
              'city_id': get_profile_info(user_id)[2],
              'status': '1' or '6' or '0',
              'count': 50}
    resp = requests.get(url, params=params)
    response = resp.json()

    return response


def insert_found_user_info(user_id):
    '''Заполнение таблицы найденных пользователей'''
    dict_1 = find_user(user_id)['response']
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


def insert_viewed_user_info(user_id):
    '''Заполнение таблицы просмотренных пользователей'''
    dict_1 = find_user(user_id)['response']
    list_1 = dict_1['items']
    for person_dict in list_1:
        if person_dict.get('is_closed') == False:
            # first_name = person_dict.get('first_name')
            # last_name = person_dict.get('last_name')
            vk_id = str(person_dict.get('id'))
            # vk_link = 'vk.com/id' + str(person_dict.get('id'))
            insert_viewed_users(vk_id)
        else:
            continue


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


def get_photo(user_id):
    """Получение остортированного списка ID фотографий"""
    list1 = get_photos_id(user_id)
    list_of_ids = []
    for i in list1:
        list_of_ids.append(i[1])
    return list_of_ids


def find_user_info():
    """Вывод информации о найденном пользователе"""
    list_user = user_selection()
    list_users = []
    for item in list_user:
        list_users.append(item)
    return str(list_users[0]).split(', ')


def send_photo(user_id, message):
    """Отправка трех самых популярных фотографий"""
    vk.method('messages.send', {'user_id': user_id,
                                'access_token': user_token,
                                'message': message,
                                'attachment': f'photo{find_user_info()[2]}_{get_photo(find_user_info()[2])[0]},photo{find_user_info()[2]}_{get_photo(find_user_info()[2])[1]},photo{find_user_info()[2]}_{get_photo(find_user_info()[2])[2]}',
                                'random_id': randrange(10 ** 7)})


def send_user_info(user_id):
    """Отправка информации о найденном пользователе"""
    write_msg(user_id, " ".join(find_user_info()))
    send_photo(user_id, 'photo:')
    update_viewed_users(find_user_info()[2])



