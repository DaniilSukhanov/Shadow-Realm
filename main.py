from flask import request, Flask
import json
from data.database import Database
import data._all_models as model
import parser_excel as pe
from data.tools import get_user
import pickle
from parser_excel import const


app = Flask(__name__)
excel = pe.ParserExcel(const.MAIN_EXCEL_FILENAME)


def register(response: dict, __draft_usernames={}):
    """Диалог регистрации. __draft_usernames не трогать!"""
    text_user = request.json["request"]["original_utterance"]
    user_id = request.json["session"]["user"]["user_id"]
    if user_id in __draft_usernames:
        if text_user.lower() == "да":
            with Database() as session:
                user = model.User()
                user.yandex_user_id = user_id
                user.username = __draft_usernames[user_id]
                user.current_excel_sheet = pe.const.ENTRY_POINT_NAME
                user.current_excel_table = pe.const.MAIN_EXCEL_FILENAME
                user.current_row_excel_table = 0
                user.serialized_stack_positions = pickle.dumps([])
                session.add(user)
                session.commit()
            response["response"]["text"] = "Для начало введите любой символ"
        else:
            response["response"]["text"] = "Добро пожаловать в мир нашей RPG игры \"Царство теней\"! Как тебя звать смелый авантюрист, который готов взглянуть в лицо опасности?"
        del __draft_usernames[user_id]
    elif text_user:
        __draft_usernames[user_id] = text_user
        response["response"]["text"] = f"Вы \"{text_user}\", я правильно раслышала?"
        response["response"]["buttons"] = [
            {"title": "Да", "hide": True},
            {"title": "Нет", "hide": True}
        ]
    else:
        response["response"]["text"] = "Добро пожаловать в мир нашей RPG игры \"Царство теней\"! Как тебя звать смелый авантюрист, который готов взглянуть в лицо опасности?"


@app.route("/", methods=["POST"])
def index():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    user = request.json["session"].get("user")
    if user is None:
        response["response"]["text"] = "Вы должны зайти в Яндекс ID"
        return json.dumps(response)
    user_id = user["user_id"]
    user = get_user(user_id)
    if user is None:
        register(response)
        return json.dumps(response)
    user_text = request.json["request"]["original_utterance"]
    if user_text == "Что ты умеешь?":
        response["response"]["text"] = "Я рассказчик. Я могу перемещать твоего героя куда ты скажешь."
        response["response"]["buttons"] = [{"title": "Понятно", "hide": True}]
        return json.dumps(response)
    if user_text == "Помощь":
        response["response"]["text"] = "Путешествуй с помощь подсказок, которые появляються при возникновении нового сообщения."
        response["response"]["buttons"] = [{"title": "Понятно", "hide": True}]
        return json.dumps(response)
    if user.current_row_excel_table == 0:
        excel.send_message(user_id, response)
        excel.next_step(user_id)
    else:
        excel.next_step(user_id)
        excel.send_message(user_id, response)
    return json.dumps(response)


if __name__ == "__main__":
    Database.connect("db/db.db")
    app.run(port=8080)
