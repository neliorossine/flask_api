from tests.config import Config
from random import randint
from api_rest.app import app
from flask_api import status
import unittest


class TestCashback(unittest.TestCase):
    """
        The test aims to ensure that the cashback requirements are correct
    """

    EMAIL = "newemail{}@nelio.com".format(randint(12121, 8484848))
    PASSWORD = "whatever"
    FULL_NAME = "Fullname"
    CPF_VALIDO = "15350946056"
    TOKEN = ""  # declared in 'test_post_login_user_success()'

    def setUp(self):
        """
        set app
        """
        app.config.from_object(Config)
        self.app = app.test_client()
        self.response_get = self.app.get("/cashback")

    def test_get_cashback(self):
        """
        valid return cashback data from an API.
        """

        cashback_request = self.app.get("/cashback/" + str(self.CPF_VALIDO))
        self.assertEqual(cashback_request.status_code, status.HTTP_200_OK)
