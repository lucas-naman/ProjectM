from google.cloud import firestore
import jwt
import datetime

class User(object):
    def __init__(self, username, email, password, registration_date = firestore.SERVER_TIMESTAMP):
        self.username = username
        self.email = email
        self.password = password # hash the password here
        self.registration_date = registration_date

    def to_dict(self):
        ans = {
            u'username': self.username,
            u'email': self.email,
            u'password': self.password,
            u'registration_date': self.registration_date,
        }
        return ans

    @staticmethod
    def from_dict(source):
        if u'registration_date' in source:
            user = User(source[u'username'], source['email'], source[u'password'], source[u'registration_date'])
        else:
            user = User(source[u'username'], source['email'], source[u'password'])
        return user

    def generate_token(self, id, db):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': id
            }
            return jwt.encode(
                payload,
                db.collection(u'secrets').document(u'token_key').get().to_dict()['value'],
                algorithm='HS256'
            )
        except Exception as e:
            return e