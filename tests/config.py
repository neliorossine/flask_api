class Config(object):
    """
        General settings about unit tests
    """

    JWT_BLACKLIST_ENABLED = True
    JWT_SECRET_KEY = "DontTellAnyone"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///banco_test.db"
    BUNDLE_ERRORS = True
