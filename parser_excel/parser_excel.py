import pandas as pd
from . import const
import data.database as db
import data._all_models as model
import pickle
from data.tools import get_user
from flask import request
import math


class ExcelError(Exception):
    pass


class NotFoundMainSheet(ExcelError):
    pass


class ParserExcel:
    def __init__(self, filename: str):
        self.excel_table = pd.read_excel(filename, sheet_name=None)
        main_sheet = self.excel_table.get(const.ENTRY_POINT_NAME)
        if main_sheet is None:
            raise NotFoundMainSheet("В excel-файле нет точки вхождения.")
        self.main_sheet = main_sheet

    def send_message(self, user_id: str, response: dict):
        user = get_user(user_id)
        sheet = self.excel_table[user.current_excel_sheet]
        text, choice, *_ = sheet.values[user.current_row_excel_table]
        response["response"]["text"] = text
        if isinstance(choice, str):
            buttons = [
                {
                    "title": string.split(":")[0],
                    "hide": True,
                } for string in choice.split(";")
            ]
            buttons.append({"title": "Что ты умеешь?", "hide": True})
            buttons.append({"title": "Помощь", "hide": True})
            response["response"]["buttons"] = buttons

    def next_step(self, user_id: str):
        user = get_user(user_id)
        stack: list = pickle.loads(user.serialized_stack_positions)
        sheet = self.excel_table[user.current_excel_sheet]
        current_row = sheet.values[user.current_row_excel_table]
        next_sheet = user.current_excel_sheet
        next_row = user.current_row_excel_table + 1
        if next_row >= len(sheet):
            if user.current_excel_sheet == const.ENTRY_POINT_NAME:
                next_row = 0
            elif stack:
                next_sheet, next_row = stack.pop(-1)
            else:
                return
        else:
            _, choice, *_ = current_row
            choice: str
            if type(choice) is str and ":" in choice:
                transitions = dict(
                    map(lambda x: x.split(":"), choice.split(";"))
                )
                text_user = request.json["request"]["original_utterance"]
                user_choice = transitions.get(text_user)
                if user_choice is not None:
                    result: str = user_choice
                    if result.isdigit():
                        next_row = int(result)
                        next_sheet = user.current_excel_sheet
                    else:
                        print(0)
                        next_row = 0
                        next_sheet = result
                        stack.append((user.current_excel_sheet, user.current_row_excel_table + 1))
                else:
                    return
        with db.Database() as session:
            user = session.query(model.User) \
                .filter(model.User.yandex_user_id == user.yandex_user_id) \
                .first()
            user.current_excel_sheet = next_sheet
            user.current_row_excel_table = next_row
            user.serialized_stack_positions = pickle.dumps(stack)
            session.commit()


if __name__ == "__main__":
    parser = ParserExcel("/Users/daniilsuhanov/Desktop/ExcelTest.xlsx")

