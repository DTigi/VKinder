import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_db import create_tables, Users, Viewed_Users
from config import DSN

engine = sqlalchemy.create_engine(DSN)

# создание таблиц с найденными пользователями и просмотренными пользователями
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()


# создание объектов
def insert_users(first_name, last_name, vk_id, vk_link):
    user = Users(first_name=f'{first_name}', last_name=f'{last_name}', vk_id=f'{vk_id}', vk_link=f'{vk_link}')
    viewed_user = Viewed_Users(vk_id=f'{vk_id}')
    session.add_all([user, viewed_user])
    session.commit()


# выбор пользователей из числа не просмотренных
q = session.query(Users).join(Viewed_Users.vk_id).filter(Viewed_Users.vk_id is None)
# print(q)

session.close()
