import db.db.db as db
from sqlalchemy import Column,VARCHAR,Integer,Float
class Item(db.Base):
    __tablename__ = 'items'
    Id_items = Column(Integer, nullable=False, primary_key=True, autoincrement=True, unique=True)
    Description_items = Column(VARCHAR, nullable=False)
    Quantity_items = Column(Integer, nullable=False)
    Mesure_items = Column(VARCHAR, nullable=False)
    Cost_items = Column(Float, nullable=False)
    Num_invoice = Column(VARCHAR, nullable=False)
    def __init__(self, Id_items, Description_items, Quantity_items, Mesure_items, Cost_items, Num_invoice):
        self.Id_items = Id_items
        self.Description_items = Description_items
        self.Quantity_items =  Quantity_items
        self.Mesure_items =     Mesure_items
        self.Cost_items =     Cost_items
        self.Num_invoice =    Num_invoice
    def __repr__(self):
        return self.Id_items, self.Description_items, self.Quantity_items, self.Mesure_items, self.Cost_items, self.Num_invoice  
    def __str__(self):
        return self.Description_items