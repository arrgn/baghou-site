import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from os import environ
from sqlalchemy.orm import DeclarativeBase
from data_types import str255


class Base(DeclarativeBase):
    type_annotation_map = {
        str255: sa.String(255),
    }


__factory = None


def global_init():
    global __factory

    if __factory:
        return

    conn_str = environ["DATABASE_URL"]
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    from . import __all_models

    Base.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
