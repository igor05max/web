import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Attraction(SqlAlchemyBase, UserMixin):
    __tablename__ = "attractions"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # название достопримечательности
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  
    # список картинок достопримечательности
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # категория (памятник, музей, парк и т.д)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # список комментариев
    comments = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # дата внесения в базу данных
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
