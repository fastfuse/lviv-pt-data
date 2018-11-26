import os


class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '\xde\x9d\xb8\xb6\x1b|\xf0\x88LD\xddRqy\x8e\xc1\xaa\xe8\x80d(\x17}\xa8')

    DATA_DIR = os.path.join(BASE_DIR, 'app', 'data')

    VEHICLE_POSITION_URL = "http://track.ua-gis.com/gtfs/lviv/vehicle_position"
    STATIC_DATA_URL = "http://track.ua-gis.com/gtfs/lviv/static.zip"

    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL',
                                           'redis://localhost:6379')

    CELERY_IMPORTS = ("app.tasks",)


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    pass


class StagingConfig(Config):
    pass


class ProductionConfig(Config):
    pass
