from db.db import db
from ..models.client import Client 

def get_clients():
    return db.session.query(Client).all()

def get_client(rfc):
    return db.session.query(Client).filter_by(rfc=rfc).first()

def add_client(rfc, name):
    client = Client(rfc, name)
    db.session.add(client)
    db.session.commit()
    return client

def update_client(rfc, name):
    client = get_client(rfc)
    client.name = name
    db.session.commit()
    return client

def delete_client(rfc):
    client = get_client(rfc)
    db.session.delete(client)
    db.session.commit()
    return client
