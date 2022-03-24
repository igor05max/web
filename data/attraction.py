import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Attraction(SqlAlchemyBase, UserMixin):
    __tablename__ = "attractions"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    comments = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
