import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import env_file

app = FastAPI()

origins = env_file.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


engine = create_engine(f'{env_file.db_type}://'
                       f'{env_file.db_username}:{env_file.db_password}@'
                       f'{env_file.db_host}:{env_file.db_port}/{env_file.db_name}')

Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


if __name__ == '__main__':
    uvicorn.run(app, host=env_file.host, port=env_file.port, debug=True, )
