from data.database import Database
import data._all_models as model


def get_user(yandex_id: str):
    with Database() as session:
        user = session.query(model.User) \
            .filter(model.User.yandex_user_id == yandex_id).first()
    return user
