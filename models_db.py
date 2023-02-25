import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Viewed_Users(Base):
    """Просмотренные пользователи"""
    __tablename__ = 'viewed_users'

    viewed_user_id = sq.Column(sq.String(length=40), primary_key=True)

    def __str__(self):
        return f'{self.viewed_user_id}'


def create_tables(engine):
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
