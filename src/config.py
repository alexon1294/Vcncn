from decouple import config

class Config():
    SECRET_KEY = config('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST='localhost'
    MYSQL_USER='root'
    MYSQL_PASSWORD=config('MYSQL_PASSWORD')
    MYSQL_DB='vacunas'


config = {
    'development': DevelopmentConfig
}
