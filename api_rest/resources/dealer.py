# -*- coding: utf-8 -*-

from flask_api import status
from flask_restful import Resource, reqparse
from api_rest.models.dealer import DealerModel
from api_rest.utils.validator import is_valid_blank_field, is_valid_cpf, is_valid_email
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from api_rest.blacklist import BLACKLIST


class Dealer(Resource):
    """
        Class responsible for the Dealer CRUD.
    """

    def get(self, dealer_id):
        """
        Get dealer by the given id.
        @param dealer_id:
        @return json 
            if is valid HTTP_200_OK,
            otherwise HTTP_404_NOT_FOUND
        """
        dealer = DealerModel.find_dealer(dealer_id)
        if dealer:
            return dealer.json(), status.HTTP_200_OK
        return {"message": "Dealer not found."}, status.HTTP_404_NOT_FOUND

    @jwt_required
    def delete(self, dealer_id):
        """
        Delete dealer by the given id.
        @param dealer_id:
        @return message and status_code.
            If all done return HTTP_200_OK, 
            if you can't find dealer return HTTP_404_NOT_FOUND, 
            otherwise HTTP_500_INTERNAL_SERVER_ERROR
        """
        dealer = DealerModel.find_dealer(dealer_id)
        if dealer:
            try:
                dealer.delete_dealer()
            except Exception as error:
                return (
                    {"message": "An error occurred trying to delete dealer."},
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return {"message": "Dealer deleted."}, status.HTTP_200_OK
        return {"message": "Dealer not found."}, status.HTTP_404_NOT_FOUND


class DealerRegister(Resource):
    """
        Class responsible for registering a Dealer.
    """

    def post(self):
        """
        Register informed data of the Dealer.
        @return json and status_code. 
            If all done return HTTP_201_CREATED,
            if invalid CPF return HTTP_404_NOT_FOUND, 
            otherwise HTTP_404_NOT_FOUND
        """

        atributos = reqparse.RequestParser(bundle_errors=True)

        atributos.add_argument(
            "email",
            type=is_valid_email,
            required=True,
            nullable=False,
            trim=True,
            help="The field 'email' cannot be left blank or is not a format valid",
        )
        atributos.add_argument(
            "senha",
            type=is_valid_blank_field,
            required=True,
            nullable=False,
            trim=True,
            help="The field 'senha' cannot be left blank or is not a format valid",
        )

        atributos.add_argument(
            "nome_completo",
            type=is_valid_blank_field,
            required=True,
            nullable=False,
            trim=True,
            help="The field 'nome_completo' cannot be left blank or is not a format valid",
        )
        atributos.add_argument(
            "cpf",
            type=is_valid_blank_field,
            required=True,
            nullable=False,
            trim=True,
            help="The field 'cpf' cannot be left blank or is not a format valid",
        )

        dados = atributos.parse_args()

        # validates CPF.
        if is_valid_cpf(dados.get("cpf")) is False:
            return {"message": "Invalid CPF field"}, status.HTTP_404_NOT_FOUND

        # validates if email already exists.
        if DealerModel.find_by_email(dados.get("email")):
            return (
                {
                    "message": "The email '{}' already exists.".format(
                        dados.get("email")
                    )
                },
                status.HTTP_400_BAD_REQUEST,
            )

        dados["senha"] = generate_password_hash(dados.get("senha"), method="sha256")

        dealer = DealerModel(**dados)
        dealer.save_dealer()
        return dealer.json(), status.HTTP_201_CREATED

    @classmethod
    def get(cls):
        """
        validate Get method
        @return HTTP_405_METHOD_NOT_ALLOWED.
        """
        response = {"message": "Cannot login with GET method"}
        return response, status.HTTP_405_METHOD_NOT_ALLOWED


class DealerLogin(Resource):
    """
        Class responsible for the Dealer login.
    """

    @classmethod
    def post(cls):
        """
        Validates the login
        @return json and status_code. 
            If all done return HTTP_200_OK, 
            otherwise HTTP_401_UNAUTHORIZED
        """
        atributos = reqparse.RequestParser()
        atributos.add_argument(
            "email",
            type=str,
            required=True,
            help="The field 'email' cannot be left blank",
        )
        atributos.add_argument(
            "senha",
            type=str,
            required=True,
            help="The field 'senha' cannot be left blank",
        )

        dados = atributos.parse_args()
        dealer = DealerModel.find_by_email(dados.get("email"))

        # validates reported data.
        if dealer and check_password_hash(dealer.senha, dados.get("senha")):
            token_de_acesso = create_access_token(identity=dealer.dealer_id)
            return {"access_token": token_de_acesso}, status.HTTP_200_OK

        response = {"message": "The email or password is incorrect"}
        return response, status.HTTP_401_UNAUTHORIZED

    @classmethod
    def get(cls):
        """
        validate Get method
        @return HTTP_405_METHOD_NOT_ALLOWED.
        """
        response = {"message": "Cannot login with GET method"}
        return response, status.HTTP_405_METHOD_NOT_ALLOWED


class DealerLogout(Resource):
    """
        Class responsible for the Dealer's logout.
    """

    @jwt_required
    def post(self):
        """
        Log off Dealer and add the token to the blacklist.
        @return message and status_code. 
            If all done return HTTP_200_OK
        """
        jwt_id = get_raw_jwt()["jti"]  # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out successfully!"}, status.HTTP_200_OK

    @classmethod
    def get(cls):
        """
        validate Get method
        @return HTTP_405_METHOD_NOT_ALLOWED.
        """
        response = {"message": "Cannot login with GET method"}
        return response, status.HTTP_405_METHOD_NOT_ALLOWED
