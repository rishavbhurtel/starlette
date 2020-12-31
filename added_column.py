from datetime import datetime
from sqlalchemy.orm import sessionmaker
from db.models import Info, Base
from db.config import DB_PATH
from sqlalchemy import create_engine, MetaData

engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
s = Session()

infos = s.query(Info).all()

for info in infos:
    date = (datetime.now()).strftime("%Y-%b-%d, %H:%M:%S")
    info.date = date
    s.add(info)

s.commit()
s.close()
