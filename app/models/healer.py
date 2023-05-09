from app import db

class Healer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    # back_populates will ref attribute that we set on crystals
    crystals = db.relationship("Crystal", back_populates="healer")