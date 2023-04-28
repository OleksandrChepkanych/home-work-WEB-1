from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser
import pathlib

file_config = pathlib.Path(__file__).parent.parent.joinpath('config_db.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'USERNAME')
password = config.get('DB', 'PASSWORD')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')

url = f'postgresql://{username}:{password}@{domain}:5432/{db_name}'
Base = declarative_base()
engine = create_engine(url, echo=False, pool_size=5)

DBSession = sessionmaker(bind=engine)
session = DBSession()
