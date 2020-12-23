from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text

DB_PATH = 'sqlite.db'

def create_info_table():
    engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)
    meta=MetaData()

    infos = Table(
        'infos', meta,
        Column('id', Integer, primary_key=True),
        Column('name', Text),
        Column('address', Text)
    )
    meta.create_all(engine)

def get_db():
    engine = create_engine('sqlite:///sqlite.db')
    metadata = MetaData(bind=engine)
    conn = engine.connect()
    return conn, metadata

if __name__ == '__main__':
    create_info_table()