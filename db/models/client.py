from db.db import db
from sqlalchemy import Column, Integer, String, Float,VARCHAR
class Client(db.Base):
    __tablename__ = 'clients'
    RFC_clients = Column(VARCHAR, nullable=False, primary_key=True)
    Name_clients= Column(VARCHAR, nullable=False)


    def __init__(self, rfc, name):
        self.RFC_clients = rfc
        self.Name_clients = name
    def __repr__(self):
        return f'cliente({self.RFC_clients}, {self.Name_clients})'
    def __str__(self):
        return self.name