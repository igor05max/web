import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


def my_date():
    dt = datetime.datetime.now()
    dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return dt


class Message(SqlAlchemyBase, UserMixin):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    # дата внесения в базу данных
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=my_date)
    # сообщение
    message = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # удалено ли сообщение
    remote = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    # создатель сообщения (user)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # получатель сообщения
    recipient = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # прочитано ли сообщение
    had_seen = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
