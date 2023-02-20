from datetime import datetime
from db import db


class Microstructure(db.Model):
    __tablename__ = 'microstructures'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    cast_iron_type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    dimensions = db.Column(db.String(20), nullable=False)
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Microstructure %r>' % self.id
