from pprint import pprint

from flask import request, Flask
import json
from data.database import Database
import data._all_models as model
import parser_excel as pe


app = Flask(__name__)


def register(response: dict, __draft_usernames={}):
    """Диалог регистрации. __draft_usernames не трогать!"""
    text_user = request.json["request"]["original_utterance"]
    user_id = request.json["session"]["user"]["user_id"]
    if user_id in __draft_usernames:
        if text_user.lower() == "да":
            with Database() as session:
                user = model.User()
                user.yandex_user_id = user_id
                user.username = text_user
                user.current_excel_sheet = pe.const.ENTRY_POINT_NAME
                user.current_excel_table = pe.const.MAIN_EXCEL_FILENAME
                user.current_row_excel_table = 0
                session.add(user)
                session.commit()
            response["response"]["text"] = "Вы зарегистрированы!"
        else:
            response["response"]["text"] = "Зарегистрируйтесь. Введите имя."
        del __draft_usernames[user_id]
    elif text_user:
        __draft_usernames[user_id] = text_user
        response["response"]["text"] = f"Вы уверены в выборе \"{text_user}\""
    else:
        response["response"]["text"] = "Зарегистрируйтесь. Введите имя."


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
    with Database() as session:
        user = session.query(model.User) \
            .filter(model.User.yandex_user_id == user_id).first()
    if user is None:
        register(response)
        return json.dumps(response)
    response["response"]["text"] = "+"
    return json.dumps(response)


if __name__ == "__main__":
    Database.connect("db/db.db")
    app.run(port=8080)
