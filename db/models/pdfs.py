from db.db import db
from sqlalchemy import Column,VARCHAR,Integer

class Pdf(db.Base):
    __tablename__ = 'pdfs'
    id_pdfs = Column(Integer, primary_key=True, autoincrement=True)
    author_pdfs = Column(VARCHAR, nullable=False)
    path_pdfs = Column(VARCHAR, nullable=False)
    status_pdfs = Column(VARCHAR, nullable=False)

    def __init__(self, author_pdfs, path_pdfs, status_pdfs):
        self.author_pdfs = author_pdfs
        self.path_pdfs = path_pdfs
        self.status_pdfs = status_pdfs
    def __repr__(self):
        return self.id_pdfs, self.author_pdfs, self.path_pdfs
    def __str__(self):
        return self.author_pdfs