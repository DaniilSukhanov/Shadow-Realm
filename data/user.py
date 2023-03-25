import datetime
import sqlalchemy as sa
from .database import SqlAlchemyBase


class User(SqlAlchemyBase):
    id = sa.Column(sa.String, unique=True, nullable=False)
    username = sa.Column(sa.String, unique=True, nullable=False)
    created_data = sa.Column(sa.DateTime, nullable=datetime.datetime.now())


