from tests.config import Config
from random import randint
from api_rest.app import app
from flask_api import status
import unittest


class TestCadastroView(unittest.TestCase):
    """
      The test aims to ensure that the create dealer requirements are correct
    """

    EMAIL = "newemail{}@nelio.com".format(randint(12121, 8484848))
    PASSWORD = "whatever"
    NOME = "Fullname"
    CPF_INVALIDO = "12345678989"
    CPF_VALIDO = " 15350946056"

    def setUp(self):
        """
        set app
        """
        app.config.from_object(Config)
        self.app = app.test_client()
        self.response_get = self.app.get("/cadastro")

    def test_get_cadastro_not_allowed(self):
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

    def test_get_cadastro_response(self):
        """
        valid GET method
        """
        response_expected = {"message": "Cannot login with GET method"}
        self.assertEqual(
            response_expected,
            self.response_get.json,
            msg="The response data is not equal",
        )

    def test_create_user_failed_missing_payload(self):
        """
        valid missing payload
        """
        response_post = self.app.post("/cadastro")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_post.status_code)

    def test_invalid_cpf(self):
        """
        valid Invalid CPF
        """
        payload = {
            "email": self.EMAIL,
            "senha": self.PASSWORD,
            "nome_completo": self.NOME,
            "cpf": self.CPF_INVALIDO,
        }
        response_post = self.app.post("/cadastro", data=payload)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response_post.status_code)
        response_expected = {"message": "Invalid CPF field"}
        self.assertEqual(response_expected, response_post.json)

    def test_create_user_is_blank(self):
        """
        valid Invalid CPF
        """
        payload = {
            "email": None,
            "senha": self.PASSWORD,
            "nome_completo": self.NOME,
            "cpf": self.CPF_VALIDO,
        }
        response_post = self.app.post("/cadastro", data=payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_post.status_code)
        response_expected = {
            "message": {
                "email": "The field 'email' cannot be left blank or is not a format valid"
            }
        }
        self.assertEqual(response_expected, response_post.json)

    def test_create_user_success(self):
        """
        valid Dealer registration with correct information
        """
        payload = {
            "email": self.EMAIL,
            "senha": self.PASSWORD,
            "nome_completo": self.NOME,
            "cpf": self.CPF_VALIDO,
        }
        response_post = self.app.post("/cadastro", data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response_post.status_code)
