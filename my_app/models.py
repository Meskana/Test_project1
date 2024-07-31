from my_app import db, login_manager, app
from flask_login import UserMixin
import jwt
import datetime 
#from itsdangerous import JSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email =  db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(200),nullable=False, default='defult.png')

    def get_reset_token(self, expires_sec=1800):
        exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_sec)
        token = jwt.encode({'user_id': self.id, 'exp': exp}, app.config['SECRET_KEY'], algorithm='HS256')
        return token

        #s = Serializer(app.config['SECRET_KEY'], expires_sec)
        #return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def get_verify_token(token):
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
        return User.query.get(user_id)



        #s = Serializer(app.config['SECRET_KEY'])
        #try:
            #user_id = s.loads(token)['user_id']
        #except:
            #return None
        #return User.query.get('user_id')


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"
