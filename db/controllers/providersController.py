from db.db import db
from ..models.provider import Provider

def get_providers():
    return db.session.query(Provider).all()

def get_provider(rfc):
    return db.session.query(Provider).filter_by(rfc=rfc).first()

def add_provider(rfc, name, rfc_clients):
    provider = Provider(rfc, name, rfc_clients)
    db.session.add(provider)
    db.session.commit()
    return provider
def update_provider(rfc, name, rfc_clients):
    provider = get_provider(rfc)
    provider.name = name
    provider.rfc_clients = rfc_clients
    db.session.commit()
    return provider
def delete_provider(rfc):
    provider = get_provider(rfc)
    db.session.delete(provider)
    db.session.commit()
    return provider