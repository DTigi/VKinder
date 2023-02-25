import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_db import create_tables, Viewed_Users
from config import DSN

engine = sqlalchemy.create_engine(DSN)

# создание таблиц с просмотренными пользователями
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()


# заполнение таблицы Просмотренные_Пользователи Viewed_Users
def insert_viewed_users(vk_id):
    viewed_user = Viewed_Users(viewed_user_id=f'{vk_id}')
    session.add(viewed_user)
    session.commit()


def count_of_viewed_users():
    count = session.query(Viewed_Users).count()
    return count


session.close()
