from .entities.User import User
from flask_jwt_extended import (JWTManager, jwt_required, 
                                get_jwt_identity,create_access_token, verify_jwt_in_request)

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname, JWT FROM user 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, fullname FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], None)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_token_by_username(self, db, username):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT JWT FROM user WHERE username = {}".format(username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return row[0]
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def create_token_and_update_db(cls, db, user_identity):
        try:
            JWT = create_access_token(identity=user_identity)
            cursor = db.connection.cursor()
            update_token_sql = "UPDATE user SET JWT = '{}' WHERE id = {}".format(JWT, user_identity['id'])
            cursor.execute(update_token_sql)
            db.connection.commit()
            print('Token actualizado.')
        except Exception as ex:
            raise Exception(ex)