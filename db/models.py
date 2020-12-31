from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()


class Info(Base):
    __tablename__ = "infos"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    date = Column(TIMESTAMP)

    # def to_dict(self):
    #     return vars(self)

    def __repr__(self):
        return "<Info(id='{}', name='{}', address={})>".format(
            self.id, self.name, self.address
        )
