import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.dialects.postgresql import BYTEA
from os import environ
from server.data.data_types import str255, json, text


class Base(DeclarativeBase):
    __allow_unmapped__ = True
    type_annotation_map = {
        str255: sa.String(255),
        bytes: BYTEA,
        json: sa.JSON,
        text: sa.TEXT
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
