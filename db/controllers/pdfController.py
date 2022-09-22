from db.db import db
from ..models.pdfs import Pdf

def get_pdfs():
    return db.session.query(Pdf).all()

def get_pdf(id):
    return db.session.query(Pdf).filter_by(id_pdfs=id).first()

def add_pdf(author_pdfs, path_pdfs):
    pdf = Pdf(author_pdfs=author_pdfs, path_pdfs=path_pdfs, status_pdfs='pending')
    db.session.begin()
    db.session.add(pdf)
    db.session.commit()
    return pdf
def update_pdf(id, author_pdfs, path_pdfs):
    pdf = get_pdf(id)
    pdf.author_pdfs = author_pdfs
    pdf.path_pdfs = path_pdfs
    db.session.commit()
    return pdf
def delete_pdf(id):
    pdf = get_pdf(id)
    db.session.delete(pdf)
    db.session.commit()
    return pdf
def get_pdf_by_author(author_pdfs):
    return db.session.query(Pdf).all()
