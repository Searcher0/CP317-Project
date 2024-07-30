from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Walmart(db.Model):
    __tablename__ = 'walmart'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    generalized_name = db.Column(db.String(255), nullable=False)

class Loblaws(db.Model):
    __tablename__ = 'loblaws'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    generalized_name = db.Column(db.String(255), nullable=False)

class Superstore(db.Model):
    __tablename__ = 'superstore'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    generalized_name = db.Column(db.String(255), nullable=False)

class Metro(db.Model):
    __tablename__ = 'metro'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    generalized_name = db.Column(db.String(255), nullable=False)