import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_db import create_tables, drop_tables, Users, Viewed_Users
from config import DSN

engine = sqlalchemy.create_engine(DSN)

# создание таблиц с найденными пользователями и просмотренными пользователями
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()


# заполнение таблицы Пользователи Users
def insert_users(first_name, last_name, vk_id, vk_link):
    user = Users(first_name=f'{first_name}', last_name=f'{last_name}', vk_id=f'{vk_id}', vk_link=f'{vk_link}')
    session.add(user)
    session.commit()
    return user


# заполнение таблицы Просмотренные_Пользователи Viewed_Users
def insert_viewed_users(vk_id):
    viewed_user = Viewed_Users(viewed_user_id=f'{vk_id}', seen_id='0')
    session.add(viewed_user)
    session.commit()
    return viewed_user


# обновление информации в таблице Просмотренные_Пользователи Viewed_Users
def update_viewed_users(vk_id):
    query = session.query(Viewed_Users).filter(Viewed_Users.viewed_user_id == f'{vk_id}').update({'seen_id': f'{vk_id}'})
    session.commit()
    return query


# выбор пользователей из числа не просмотренных
def user_selection():
    query = session.query(Users).join(Viewed_Users).filter(Viewed_Users.seen_id == '0').all()
    query_list = [q for q in query]
    session.commit()
    return query_list


# удаление всех таблиц
def drop_table():
    drop_tables(engine)


# удаление информации из таблиц
def delete_tables():
    session.query(Viewed_Users).delete()
    session.query(Users).delete()
    session.commit()


session.close()
