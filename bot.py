from vk_api.longpoll import VkLongPoll, VkEventType

from main import user, insert_found_user_info, insert_viewed_user_info, write_msg, send_user_info, longpoll
from users_db import delete_tables


def event_handler(user_id):
    '''Функция обработки входящих сообщений в сообществе'''
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "старт":
                    delete_tables()
                    insert_found_user_info(user)
                    insert_viewed_user_info(user)
                    write_msg(event.user_id, f"Бот запущен. Хочешь найти себе пару, {event.user_id}? да/нет")

                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.to_me:
                                request = event.text
                                if request == 'да':
                                    send_user_info(user_id)
                                    write_msg(event.user_id, "Выполнить поиск еще раз? да/нет")
                                else:
                                    write_msg(event.user_id, "Пока((")
                                    break
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")


event_handler(user)
