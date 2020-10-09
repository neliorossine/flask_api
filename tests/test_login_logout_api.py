from tests.config import Config
from random import randint
from api_rest.app import app
from flask_api import status
import unittest


class TestLoginLogout(unittest.TestCase):
    """
        The test aims to ensure that the login and logout requirements are correct
    """

    EMAIL = "newemail{}@nelio.com".format(randint(12121, 8484848))
    PASSWORD = "whatever"
    FULL_NAME = "Fullname"
    CPF_VALIDO = " 15350946056"
    TOKEN = ""  # declared in 'test_post_login_user_success()'
    DEALER_ID = ""  # declared in 'test_post_login_user_success()'

    def setUp(self):
        """
        set app
        """
        app.config.from_object(Config)
        self.app = app.test_client()
        self.response_get = self.app.get("/login")

    def test_get_login_not_allowed(self):
        """
        valid request allowed
        """
        self.assertEqual(
            status.HTTP_405_METHOD_NOT_ALLOWED, self.response_get.status_code
        )

    def test_content_type(self):
        """
        valid Content-Type
        """
        content_type = "application/json"
        self.assertIn(content_type, self.response_get.content_type)

    def test_get_login_response(self):
        """
        valid GET method
        """
        response_expected = {"message": "Cannot login with GET method"}
        self.assertEqual(
            response_expected,
            self.response_get.json,
            msg="The response data is not equal",
        )

    def test_post_login_missing_payload(self):
        """
        valid missing payload
        """
        response_post = self.app.post("/login")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_post.status_code)

    def test_post_login_user_failed(self):
        """
        valid login with wrong information
        """
        payload = {"email": self.EMAIL, "senha": self.PASSWORD}
        response_post = self.app.post("/login", data=payload)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response_post.status_code)

    def test_post_login_user_success(self):
        """
        valid login with correct information.
        """
        self.app = app.test_client()
        payload_cadastro = {
            "email": self.EMAIL,
            "senha": self.PASSWORD,
            "nome_completo": self.FULL_NAME,
            "cpf": self.CPF_VALIDO,
        }
        new_user_request = self.app.post("/cadastro", data=payload_cadastro)
        self.__class__.DEALER_ID = new_user_request.json.get("dealer_id")

        if new_user_request.status_code == status.HTTP_201_CREATED:
            payload_login = {"email": self.EMAIL, "senha": self.PASSWORD}
            login_request = self.app.post("/login", data=payload_login)
            self.assertEqual(status.HTTP_200_OK, login_request.status_code)
            self.__class__.TOKEN = login_request.json.get("access_token")

    def test_post_logout_user_success(self):
        """
        valid logout with correct information.
        """

        headers = {"authorization": "Bearer {}".format(self.__class__.TOKEN)}

        logout_request = self.app.delete(
            "/dealers/" + str(self.__class__.DEALER_ID), headers=headers
        )
        self.assertEqual(logout_request.status_code, status.HTTP_200_OK)
