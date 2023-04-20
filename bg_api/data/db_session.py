from os import environ as env

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Session, DeclarativeBase

from bg_api.data.data_types import str255, json, text


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

    conn_str = f"postgresql://{env['DB_USER']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:{env['DB_PORT']}/{env['DATABASE']}"

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    from bg_api.data import __all_models

    Base.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
