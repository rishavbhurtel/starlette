from faker import Faker
from random import randint
from sqlalchemy import create_engine
import json
fake = Faker()
DB_PATH = 'sqlite.db'

def info():
    info = {
        'id': fake.random_int(0,10000),
        'name': fake.name(), 
        'address': fake.address()
    }

    return info

def populate_info(infos):
    #established db connection
    engine = create_engine(f'sqlite:///{DB_PATH}')
    #create connection
    conn = engine.connect()
    #begin transaction
    trans = conn.begin()
    for info in infos:
        conn.execute('INSERT INTO "infos"(id, '
                    'name, '
                    'address)'
                    f'VALUES(?,?,?)', [info[key] for key in info.keys()])
    trans.commit()
    #close connection
    conn.close()

if __name__ == "__main__":
    infos = [info() for _ in range(10)]
    print(f'Adding {len(infos)} info to db.')
    populate_info(infos)