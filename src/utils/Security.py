from decouple import config
from config import Config
import datetime
import jwt
import pytz


class Security():

    secret = config('JWT_SECRET_KEY')
    tz = pytz.timezone("America/Mexico_City")

    @classmethod
    def generate_token(self, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=self.tz),
            'exp': datetime.datetime.now(tz=self.tz) + datetime.timedelta(minutes=0.5),
            'username': authenticated_user.username,
            'fullname': authenticated_user.fullname,
            'roles': ['Administrator', 'Editor']
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    @classmethod
    def verify_token(self, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, self.secret, algorithms=["HS256"])
                    roles = list(payload['roles'])

                    if 'Administrator' in roles:
                        return True
                    return False
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False

        return False
