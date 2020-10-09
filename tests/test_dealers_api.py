from tests.config import Config
from random import randint
from api_rest.app import app
from flask_api import status
import unittest


class TestDealersView(unittest.TestCase):
    """
      The test aims to ensure that the dealers requirements are correct
    """

    EMAIL = "newemail{}@nelio.com".format(randint(12121, 8484848))
    PASSWORD = "whatever"
    NOME = "Fullname"
    CPF_INVALIDO = "12345678989"
    CPF_VALIDO = " 15350946056"
    CODIGO = randint(1, 9999999)
    VALOR = 150.00
    DATA = "2020-02-12"

    def setUp(self):
        """
        set app and get created token.
        """
        app.config.from_object(Config)
        self.app = app.test_client()
        payload = {
            "email": self.EMAIL,
            "senha": self.PASSWORD,
            "nome_completo": self.NOME,
            "cpf": self.CPF_VALIDO,
        }
        new_user_request = self.app.post("/cadastro", data=payload)
        self.dealer_id = new_user_request.json.get("dealer_id")

        if new_user_request.status_code == status.HTTP_201_CREATED:
            payload_login = {"email": self.EMAIL, "senha": self.PASSWORD}
            login_request = self.app.post("/login", data=payload_login)
            self.access_token = login_request.json.get("access_token")

    def test_get_dealer(self):
        """
        valid get dealer by ID.
        """
        headers = {"authorization": "Bearer {}".format(self.access_token)}
        dealer_request = self.app.get(
            "/dealers/" + str(self.dealer_id), headers=headers
        )
        self.assertEqual(dealer_request.status_code, status.HTTP_200_OK)

    def test_delete_dealer(self):
        """
        valid delete dealer by ID.
        """
        headers = {"authorization": "Bearer {}".format(self.access_token)}

        dealer_request = self.app.delete(
            "/dealers/" + str(self.dealer_id), headers=headers
        )
        self.assertEqual(dealer_request.status_code, status.HTTP_200_OK)
