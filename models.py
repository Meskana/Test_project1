from coin_reserch import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email =  db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(20),nullable=False, default='img.png')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"
