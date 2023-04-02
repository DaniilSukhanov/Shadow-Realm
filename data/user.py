import datetime
import sqlalchemy as sa
from .database import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "User"

    id = sa.Column(sa.Integer, unique=True, nullable=False, primary_key=True)
    yandex_user_id = sa.Column(sa.String, unique=True, nullable=False)
    username = sa.Column(sa.String, unique=True, nullable=False)
    created_data = sa.Column(sa.DateTime, default=datetime.datetime.now(), nullable=False)
    current_excel_table = sa.Column(sa.String, nullable=False)
    current_row_excel_table = sa.Column(sa.Integer, nullable=False)
    current_excel_sheet = sa.Column(sa.String, nullable=False)
    serialized_stack_positions = sa.Column(sa.String)
    state = sa.Column(sa.Integer, default=0, nullable=False)

    @property
    def position(self):
        return self.current_excel_table, \
            self.current_excel_sheet, self.current_row_excel_table

