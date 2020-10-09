class Config(object):
    """
        General project settings
    """

    JWT_BLACKLIST_ENABLED = True
    JWT_SECRET_KEY = "DontTellAnyone"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///banco.db"
    SQLALCHEMY_DATABASE_URI_TEST = "sqlite:///banco_test.db"
    BUNDLE_ERRORS = True
