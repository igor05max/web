import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


def my_date():
    dt = datetime.datetime.now()
    dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return dt


class Chat(SqlAlchemyBase, UserMixin):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # дата внесения в базу данных

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=my_date)

    participants = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    list_messages = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    new_message = sqlalchemy.Column(sqlalchemy.String, nullable=True)
