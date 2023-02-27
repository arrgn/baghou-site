from sqlalchemy import create_engine
from os import environ

dao = create_engine(environ['DATABASE_URL'])
dao.connect()
