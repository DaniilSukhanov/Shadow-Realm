from pprint import pprint

from flask import request, Flask
import json
from data.database import Database
import data._all_models as model
import parser_excel as pe


app = Flask(__name__)


def register(response: dict):
    username = request.json["request"]["original_utterance"]
    print(username)
    if username:
        with Database() as session:
            user = model.User()
            user.yandex_user_id = request.json["session"]["user"]["user_id"]
            user.username = username
            user.current_excel_sheet = pe.const.ENTRY_POINT_NAME
            user.current_excel_table = pe.const.MAIN_EXCEL_FILENAME
            user.current_row_excel_table = 0
            session.add(user)
            session.commit()
        response["response"]["text"] = f"Вы {username}"
    else:
        response["response"]["text"] = "Зарегистрируйтесь"

@app.route("/", methods=["POST"])
def index():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    user_id = request.json["session"]["user"]["user_id"]
    with Database() as session:
        user = session.query(model.User).filter(model.User.yandex_user_id == user_id).first()
    if user is None:
        register(response)
    else:
        response["response"]["text"] = "+"
    return json.dumps(response)


if __name__ == "__main__":
    Database.connect("db/db.db")
    app.run(port=8080)
