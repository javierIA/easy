from db.db import db
from sqlalchemy import Column,VARCHAR,BOOLEAN

class User(db.Base):
    __tablename__ = 'users'
    email_users = Column(VARCHAR, nullable=False, primary_key=True)
    password_users= Column(VARCHAR, nullable=False)
    isadmin_users= Column(BOOLEAN, nullable=False)
    username_users= Column(VARCHAR, nullable=False)
    def __init__(self, email, password, isadmin, username):
        self.email_users = email
        self.password_users = password
        self.isadmin_users = isadmin
        self.username_users = username

        
    def __repr__(self):
        return f'user({self.email_users}, {self.password_users}, {self.isadmin_users}, {self.username_users})'
    def __str__(self):
        return self.username_users
