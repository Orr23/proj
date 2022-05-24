from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:potterdursley@172.31.224.1/URL_DATABASE'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)


class Urls(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    status_code = db.Column(db.Integer(), nullable=True)
    last_update = db.Column(db.DateTime(), nullable=True)

    def __int__(self, id, url, status_code, last_update):
        self.id = id
        self.url = url
        self.status_code = status_code
        self.last_update = last_update

    def __repr__(self):
        return self.id

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_if_test(cls):
        return cls.query.filter(cls.url.like("%test%")).all()

    @classmethod
    def get_if_no_status(cls):
        return cls.query.filter(cls.status_code == None)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()