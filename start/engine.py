from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from env_file import db_type, db_username, db_host, db_password, db_name, db_port

engine = create_engine(f'{db_type}://'
                       f'{db_username}:{db_password}@'
                       f'{db_host}:{db_port}/{db_name}', )

Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
