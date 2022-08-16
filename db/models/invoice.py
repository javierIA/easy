from db.db import db
from sqlalchemy import Column, Float,VARCHAR,Date
class Invoice(db.Base):
    __tablename__ = 'invoices'
    Num_invoices = Column(VARCHAR, nullable=False, primary_key=True)
    Date_invoices = Column(Date, nullable=False)
    Origin_invoices = Column(VARCHAR, nullable=False)
    Total_invoices = Column(Float, nullable=False)
    RFC_clients = Column(VARCHAR, nullable=False)


    def __init__(self, num,date, origin,total,rfc):
        self.Num_invoices = num
        self.RFC_clients = rfc
        self.Date_invoices = date
        self.Total_invoices = total
        self.Origin_invoices = origin
    def __repr__(self):
        return f'({self.Num_invoices}, {self.RFC_clients}, {self.Date_invoices}, {self.Total_invoices}, {self.Origin_invoices})'
    def __str__(self):
        return self.name
