import sqlalchemy as sa
import sqlalchemy.orm as orm


SqlAlchemyBase = orm.declarative_base()


class DatabaseError(Exception):
    pass


class NotConnect(DatabaseError):
    pass


class MultipleSession(DatabaseError):
    pass


class Database:
    """Класс для подключения к базе данных и создавания сессии с ней.
    Класс реализован на паттерне Singleton. Создание сессии происходит
    с помощью оператора with:
    with Database() as session:
        ...
    """

    __instance = None
    __factory = None
    __current_session = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None or cls.__factory is None:
            raise NotConnect("База данных не подключена.")
        return cls.__instance

    def __enter__(self):
        if self.__current_session is not None:
            msg = "Нельзя начинать сессию, пока не закончилась другая"
            raise MultipleSession(msg)
        session = self.__factory()
        self.__current_session = session
        return session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__current_session.close()
        self.__current_session = None
        return False

    @classmethod
    def connect(cls, filepath: str):
        """Создает подключение к базе данных. База данных должна быть
        Sqlite."""
        conn_str = f'sqlite:///{filepath.strip()}?check_same_thread=False'
        engine = sa.create_engine(conn_str, echo=False)
        factory = orm.sessionmaker(bind=engine)
        from . import _all_models
        SqlAlchemyBase.metadata.create_all(engine)
        cls.__factory = factory
        cls.__instance = super().__new__(cls)


if __name__ == "__main__":
    Database.connect("../db/db.db")
    with Database() as s:
        pass
