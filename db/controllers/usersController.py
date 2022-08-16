from db.db import db
from db.models.user import User
from sqlalchemy.orm import Session

def get_users():
    return db.session.query(User).all()
def get_user(email):
    return db.session.query(User).filter_by(email_users=email).first()
def get_user_by_username(username):
    db.session.begin()

    return db.session.query(User).filter_by(username_users=username).first()

def add_user(email, password, isadmin, username):
    user = User(email, password, isadmin, username)
    db.session.begin()
    db.session.add(user)
    db.session.commit()
def update_user(email, password, isadmin, username):
    db.session.begin()
    user = get_user(email)
    user.password = password
    user.isadmin = isadmin
    user.username = username
    db.session.commit()
    return user
def delete_user(email):
    user = get_user(email)
    db.session.delete(user)
    db.session.commit()
    return user
def update_user_password(email, password):
    db.session.begin()
    user = get_user(email)
    user.password_users = password
    db.session.commit()
    return user
