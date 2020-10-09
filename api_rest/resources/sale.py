# -*- coding: utf-8 -*-

from flask_api import status
from flask_restful import Resource, reqparse
from api_rest.models.sale import SaleModel
from api_rest.utils.validator import is_valid_cpf, is_valid_date
from flask_jwt_extended import jwt_required
import sqlite3


class Sale(Resource):
    """
        Class responsible for the Sale CRUD.
    """

    atributos = reqparse.RequestParser()
    atributos.add_argument(
        "codigo",
        type=str,
        required=True,
        help="The field 'codigo' cannot be left blank",
    )
    atributos.add_argument(
        "valor",
        type=float,
        required=True,
        help="The field 'valor' cannot be left blank",
    )
    atributos.add_argument(
        "data", type=str, required=True, help="The field 'data' cannot be left blank"
    )
    atributos.add_argument(
        "cpf", type=str, required=True, help="The field 'cpf' cannot be left blank"
    )
    atributos.add_argument("status", type=str)

    def get(self, sale_id=None):
        """
        Returns all Sales or just one by the ID passed.
        @param sale_id:
        @return json and status_code.
            If all done return all sales or specific sale and HTTP_200_OK, 
            if you can't find dealer return HTTP_404_NOT_FOUND
        """

        # Returns Sale by the given ID
        if sale_id:

            sale = SaleModel.find_sale(sale_id)

            if sale:
                return sale.json(), status.HTTP_200_OK
            return {"message": "Sale not found."}, status.HTTP_404_NOT_FOUND

        # Returns all Sales with status != Aprovado
        else:

            connection = sqlite3.connect("api_rest/banco.db")
            try:
                cursor = connection.cursor()
            except sqlite3.Error as e:
                print(e)
                raise

            # Consult all Sales with status != Aprovado
            consulta = "SELECT * FROM sales WHERE status != ?"
            resultado = cursor.execute(consulta, ("Aprovado",))

            sales = []
            for linha in resultado:
                sales.append(
                    {
                        "sale_id": linha[0],
                        "codigo": linha[1],
                        "valor": linha[2],
                        "data": linha[3],
                        "cpf": linha[4],
                        "status": linha[5],
                        "percent_cashback": str(linha[6]) + "%",
                        "valor_cashback": round(linha[7], 2),
                    }
                )

            return {"sales": sales, "status": status.HTTP_200_OK}

    @jwt_required
    def post(self):
        """
        Register a Sale
        @return message and status_code.
            If all done return json and HTTP_201_CREATED,
            if invalid CPF or invalid Data return HTTP_404_NOT_FOUND, 
            if the 'Sale codigo' already exists HTTP_400_BAD_REQUEST, 
            otherwise HTTP_500_INTERNAL_SERVER_ERROR
        """
        dados = Sale.atributos.parse_args()

        # validates CPF.
        if is_valid_cpf(dados.get("cpf")) is False:
            return {"message": "Invalid CPF field"}, status.HTTP_404_NOT_FOUND

        # validates Data.
        if is_valid_date(dados.get("data")) is False:
            return {"message": "Invalid Data field"}, status.HTTP_404_NOT_FOUND

        # Validation for exclusive CPF.
        dados["status"] = (
            "Em validação" if dados.get("cpf") != "15350946056" else "Aprovado"
        )

        # Check if the 'Sale codigo' already exists.
        if SaleModel.find_sale_by_codigo(dados.get("codigo")):
            return {
                "message": "Codigo '{}' already exists.".format(
                    dados.get("codigo"), status.HTTP_400_BAD_REQUEST
                )
            }

        # Cashback rules
        try:
            if dados.get("valor") < 1000.00:
                percent_cashback = 10
                valor_cashback = dados.get("valor") * 0.10
            elif (dados.get("valor") > 1000.00) and (dados.get("valor") < 1500.00):
                percent_cashback = 15
                valor_cashback = dados.get("valor") * 0.15
            else:
                percent_cashback = 20
                valor_cashback = dados.get("valor") * 0.20

            sale = SaleModel(**dados)
            sale.insert_sale(percent_cashback, valor_cashback)

        except Exception as error:
            return (
                {"message": "An internal error occurred trying to save sale."},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return sale.json(), status.HTTP_201_CREATED

    @jwt_required
    def put(self, sale_id=None):
        """
        Change a Sale
        @param sale_id:
        @return message and status_code.
            If all done return json and HTTP_200_OK,
            if invalid CPF or invalid Data return HTTP_404_NOT_FOUND, 
            otherwise HTTP_500_INTERNAL_SERVER_ERROR
        """
        dados = Sale.atributos.parse_args()

        # validates CPF.
        if is_valid_cpf(dados.get("cpf")) is False:
            return {"message": "Invalid CPF field"}, status.HTTP_404_NOT_FOUND

        # validates Data.
        if is_valid_date(dados.get("data")) is False:
            return {"message": "Invalid Data field"}, status.HTTP_404_NOT_FOUND

        # validates Status.
        if dados.get("status") is None:
            dados["status"] = "Em validação"

        sale_found = SaleModel.find_sale(sale_id)

        #  Changes data only with status "Em validação"
        if sale_found:
            try:
                if sale_found.update_sale(**dados):
                    return sale_found.json(), status.HTTP_200_OK
                else:
                    return (
                        {
                            "message": "Sale cannot be updated as it has already been approved."
                        },
                        status.HTTP_404_NOT_FOUND,
                    )
            except Exception as error:
                return (
                    {"message": "An internal error occurred trying to update sale."},
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return {"message": "Sale not found."}, status.HTTP_404_NOT_FOUND

    @jwt_required
    def delete(self, sale_id=None):
        """
        Delete Sale.
        @param sale_id:
        @return message and status_code.
            If all done return json and HTTP_200_OK,
            if status is 'Aprovado' return HTTP_404_NOT_FOUND, 
            otherwise HTTP_500_INTERNAL_SERVER_ERROR
        """
        sale = SaleModel.find_sale(sale_id)
        if sale:
            try:
                if sale.delete_sale() is True:
                    return {"message": "Sale deleted."}, status.HTTP_200_OK
                else:
                    return (
                        {
                            "message": "Sale cannot be deleted as it has already been approved."
                        },
                        status.HTTP_404_NOT_FOUND,
                    )
            except Exception as error:
                return (
                    {"message": "An error occurred trying to delete sale."},
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )  # Internal Server Error

        return {"message": "Sale not found."}, status.HTTP_404_NOT_FOUND
