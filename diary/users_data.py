from flask_sqlalchemy import SQLAlchemy
from app import db
from app import app


class User(db.Model):
    __name__  = "users_table"
    email = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    active = db.Column(db.Boolean)
    id = db.Column(db.Integer)
    password = db.Column(db.Integer)

    def __repr__(self):
        return "<User(name={},active={})>" \
            .format(self.name, self.active)



