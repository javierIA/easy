from db.db import db
from ..models.invoice import Invoice

def get_invoices():
    return db.session.query(Invoice).all()

def get_invoice(num):
    return db.session.query(Invoice).filter_by(Num_invoices=num).first()


def add_invoice(Num_invoices, RFC_clients, Origin_invoices, Total_invoices, Date_invoices):
    invoice = Invoice(Num_invoices, RFC_clients, Origin_invoices, Total_invoices, Date_invoices)
    db.session.add(invoice)
    db.session.commit()
    return invoice

def update_invoice(Num_invoices, RFC_clients, Origin_invoices, Total_invoices, Date_invoices):
    invoice = get_invoice(Num_invoices)
    invoice.RFC_clients = RFC_clients
    invoice.Date_invoices = Date_invoices
    invoice.Origin_invoices = Origin_invoices
    invoice.Total_invoices = Total_invoices
    try:
        
        db.session.commit()
    except:
        db.session.rollback()

    return invoice

def delete_invoice(num):
    invoice = get_invoice(num)
    db.session.delete(invoice)
    db.session.commit()
    return invoice
def getmaxInvoices():
    return db.session.query(Invoice).count()