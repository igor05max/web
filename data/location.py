import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm


class Location(SqlAlchemyBase, UserMixin):
    __tablename__ = "locations"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # название достопримечательности
    # список картинок достопримечательности
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # категория (памятник, музей, парк и т.д)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # дата внесения в базу данных
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("cities.id"))
    city = orm.relation('City')
