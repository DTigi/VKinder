import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

"""Найденные пользователи"""
class Users(Base):
    __tablename__ = 'users'

    first_name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    vk_id = sq.Column(sq.String(length=40), primary_key=True)
    vk_link = sq.Column(sq.String(length=100), nullable=False)


    def __str__(self):
        return f'{self.first_name}, {self.last_name}, {self.vk_id}, {self.vk_link}'


"""Просмотренные пользователи"""
class Viewed_Users(Base):
    __tablename__ = 'viewed_users'

    id = sq.Column(sq.Integer, primary_key=True)
    viewed_user_id = sq.Column(sq.String, sq.ForeignKey("users.vk_id"))
    seen_id = sq.Column(sq.String(length=40))

    users = relationship(Users, backref='viewed_users')


    def __str__(self):
        return f'{self.viewed_user_id}'


def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop_all(engine)
