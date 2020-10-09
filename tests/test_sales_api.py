from tests.config import Config
from random import randint
from api_rest.app import app
from flask_api import status
import unittest


class TestSalesView(unittest.TestCase):
    """
      The test aims to ensure that the sales requirements are correct
    """

    EMAIL = "newemail{}@nelio.com".format(randint(12121, 8484848))
    PASSWORD = "password"
    NOME = "Fullname"
    CPF_VALIDO = " 15350946056"
    CODIGO = randint(1, 9999999)
    VALOR = 150.00
    DATA = "2020-02-12"
    TOKEN = ""  # declared in 'setUp()'
    SALE_STATUS = ""  # declared in 'test_create_sales_success()'
    SALE_ID = ""  # declared in 'test_create_sales_success()'

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

        if new_user_request.status_code == status.HTTP_201_CREATED:
            payload_login = {"email": self.EMAIL, "senha": self.PASSWORD}
            login_request = self.app.post("/login", data=payload_login)
            self.__class__.TOKEN = login_request.json.get("access_token")

    def test_create_sales_success(self):
        """
        valid new registered sale.
        """
        payload = {
            "codigo": self.CODIGO,
            "valor": self.VALOR,
            "data": self.DATA,
            "cpf": self.CPF_VALIDO,
        }

        headers = {"authorization": "Bearer {}".format(self.__class__.TOKEN)}
        sales_request = self.app.post("/sales", headers=headers, data=payload)
        self.assertEqual(sales_request.status_code, status.HTTP_201_CREATED)
        self.__class__.SALE_ID = sales_request.json.get("sale_id")
        self.__class__.SALE_STATUS = sales_request.json.get("status")

    def test_get_all_sales(self):
        """
        valid get all sales.
        """
        sales_request = self.app.get("/sales")
        self.assertEqual(sales_request.status_code, status.HTTP_200_OK)

    def test_get_sale_by_id(self):
        """
        valid get sale by ID.
        """
        sales_request = self.app.get("/sales/" + str(self.__class__.SALE_ID))
        self.assertEqual(sales_request.status_code, status.HTTP_200_OK)

    def test_update_delete_sale_by_id(self):
        """
        valid update sale by ID.
        """
        payload = {
            "codigo": randint(232323, 989898),
            "valor": self.VALOR,
            "data": self.DATA,
            "cpf": self.CPF_VALIDO,
        }

        headers = {"authorization": "Bearer {}".format(self.__class__.TOKEN)}
        sales_request = self.app.put(
            "/sales/" + str(self.__class__.SALE_ID), headers=headers, data=payload
        )

        # If status 'Aprovado', cannot change.
        if self.__class__.SALE_STATUS == "Aprovado":
            self.assertEqual(sales_request.status_code, status.HTTP_404_NOT_FOUND)
        else:

            self.assertEqual(sales_request.status_code, status.HTTP_200_OK)

            """
                valid delete sale by ID.
            """
            headers = {"authorization": "Bearer {}".format(self.__class__.TOKEN)}

            sales_request = self.app.delete(
                "/sales/" + str(self.__class__.SALE_ID), headers=headers
            )
            self.assertEqual(sales_request.status_code, status.HTTP_200_OK)
