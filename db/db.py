from faker import Faker
from random import randint
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Info, Base
from config import DB_PATH

fake = Faker()
engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)

engine = create_engine(DB_PATH)
Base.metadata.create_all(engine)


def data():
    data = {
        "id": fake.random_int(0, 10000),
        "name": fake.name(),
        "address": fake.address(),
    }
    return data


# info = Info(
#     id = 1,
#     name = 'Rishav',
#     address = 'Kathmandu'
# )


def populate_info(datas):
    for data in datas:
        info = Info(**data)
        s.add(info)


def recreate_database():
    Base.metadata.drop_all(engine)
    s.commit()
    s.close()
    Base.metadata.create_all(engine)


# def get_db():
#     metadata = Base.metadata.create_all(engine)
#     conn = engine.connect()
#     return conn, metadata

if __name__ == "__main__":
    s = Session()
    s.close_all()
    recreate_database()
    datas = [data() for _ in range(10)]
    print(f"Adding {len(datas)} info to db.")
    populate_info(datas)
    s.commit()
    s.close()
