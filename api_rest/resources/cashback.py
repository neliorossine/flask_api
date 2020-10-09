from flask_api import status
from flask_restful import Resource
from api_rest.utils.validator import is_valid_cpf
import requests


class Cashback(Resource):
    """
        Class responsible for returning cashback data from an API.
    """

    def get(self, cpf):
        """
        Get CPF to return the total cashback
        @param cpf:
        @return credit and status_code.
            If all done return HTTP_200_OK,
            if invalid CPF return HTTP_404_NOT_FOUND,
            otherwise HTTP_500_INTERNAL_SERVER_ERROR
        """
        if is_valid_cpf(cpf) is False:
            return {"message": "Invalid CPF"}, status.HTTP_404_NOT_FOUND

        url = (
            "https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf="
            + cpf
        )
        headers = {"token": "ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm"}

        try:
            req = requests.get(url, headers=headers)
            if req:
                return req.json()["body"], status.HTTP_200_OK
        except ConnectionError:
            return (
                {"message": "Could not connect to external API - Check URI."},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
