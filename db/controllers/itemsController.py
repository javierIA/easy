from db.db import db
from ..models.item import Item

def get_items():
    if not db.session.query(Item).count():
        return None
    return db.session.query(Item).all()
def  get_item(id):
    if not db.session.query(Item).filter_by(Id_items=id).count():
        return None
    return db.session.query(Item).filter_by(Id_items=id).first()
def add_item(desc, quant, mes, cost, nom):
    item = Item(Id_items=0,Description_items=desc, Quantity_items=quant, Mesure_items=mes,Cost_items=cost,Num_invoice= nom)
    db.session.add(item)
    db.session.commit()
    return item
def update_item(Id_items, Description_items, Quantity_items, Mesure_items, Cost_items, Num_invoice):
    item = get_item(Id_items)
    if not item:
        return None
    item.Description_items = Description_items
    item.Quantity_items = Quantity_items
    item.Mesure_items = Mesure_items
    item.Cost_items = Cost_items
    item.Num_invoice = Num_invoice
      
    db.session.commit()

    return item
def delete_item(id):
    item = get_item(id)
    db.session.delete(item)
    db.session.commit()
    return item
    