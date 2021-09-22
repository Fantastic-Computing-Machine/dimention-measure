from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class Projects(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False, unique=True)

    def __repr__(self):
        return '<Name %r>' % self.id


class Dimentions(db.Model):
    __tablename__ = 'dimentions'

    id = db.Column(db.Integer, primary_key=True)
    dim_name = db.Column(db.String(200), nullable=False)
    length = db.Column(db.Numeric(
        precision=2, asdecimal=False, decimal_return_scale=None), nullable=False)
    width = db.Column(db.Numeric(
        precision=2, asdecimal=False, decimal_return_scale=None), nullable=True)
    sqm = db.Column(db.Numeric(
        precision=2, asdecimal=False, decimal_return_scale=None), nullable=True)
    sqft = db.Column(db.Numeric(
        precision=2, asdecimal=False, decimal_return_scale=None), nullable=True)
    rate = db.Column(db.Numeric(
        precision=2, asdecimal=False, decimal_return_scale=None), nullable=True)
    amount = db.Column(db.Numeric(
        precision=2, asdecimal=False, decimal_return_scale=None), nullable=True)
    project_id = db.Column(db.Integer, ForeignKey(
        'projects.id'), nullable=False)
    # project = relationship("Projects", back_populates="dimentions")
