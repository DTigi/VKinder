import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

"""Найденные пользователи"""
class Users(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    vk_id = sq.Column(sq.String(length=40), primary_key=True, nullable=False)
    vk_link = sq.Column(sq.String(length=100), nullable=False)


"""Просмотренные пользователи"""
class Viewed_Users(Base):
    __tablename__ = 'viewed_users'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.String, sq.ForeignKey("users.vk_id"), nullable=False)

    users = relationship(Users, backref='viewed_users')


def create_tables(engine):
    Base.metadata.drop_all(engine) # не нужно удалять таблицы
    Base.metadata.create_all(engine)