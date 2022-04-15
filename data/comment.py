import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
import datetime


def my_date():
    dt = datetime.datetime.now()
    dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return dt


class Comment(SqlAlchemyBase, UserMixin):
    __tablename__ = "comments"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # комментарий
    comment = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # дата внесения в базу данных
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=my_date)
    # создатель комментария (user)
    creator = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    location_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("locations.id"))
    location = orm.relation('Location')
