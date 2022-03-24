import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class City(SqlAlchemyBase, UserMixin):
    __tablename__ = "cities"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # название города
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # список достопримечательностей
    attractions = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # дата внесения в базу данных
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
