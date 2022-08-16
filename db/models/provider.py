from db.db import db
from sqlalchemy import Column,VARCHAR

class Provider(db.Base):
    __tablename__ = 'providers'
    RFC_providers = Column(VARCHAR, nullable=False, primary_key=True)
    Name_providers= Column(VARCHAR, nullable=False)
    RFC_clients= Column(VARCHAR, nullable=False)
   
    def __init__(self, rfc, name, rfc_clients):
        self.RFC_providers = rfc
        self.Name_providers = name
        self.RFC_clients = rfc_clients
        
    def __repr__(self):
        return f'provider({self.RFC_providers}, {self.Name_providers}, {self.RFC_clients})'
    def __str__(self):
        return self.name