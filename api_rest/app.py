from flask import jsonify
from api_rest import create_app, initialize_api, initialize_jwt, initialize_db
from api_rest.blacklist import BLACKLIST
from api_rest.resources.dealer import Dealer, DealerRegister, DealerLogin, DealerLogout
from api_rest.resources.sale import Sale
from api_rest.resources.cashback import Cashback
from api_rest.config import Config

config = Config()
app = create_app(config=config)
api = initialize_api(app)
jwt = initialize_jwt(app)
db = initialize_db(app)


@app.before_first_request
def create_bd():
    """
    Creates connection with the database
    """
    db.create_all()


@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    """
    Check if token is on the blacklist
    @param token:
    @return token
    """
    return token["jti"] in BLACKLIST


@jwt.revoked_token_loader
def token_invalidado():
    """
    Checks invalid token
    @return 401
    """
    return jsonify({"message": "You have been logged out."}), 401


api.add_resource(Sale, "/sales", "/sales/<string:sale_id>")
api.add_resource(Dealer, "/dealers/<int:dealer_id>")
api.add_resource(DealerRegister, "/cadastro")
api.add_resource(DealerLogin, "/login")
api.add_resource(DealerLogout, "/logout")
api.add_resource(Cashback, "/cashback/<string:cpf>")


def test_client():
    """
    Tests
    @return:
    """
    return None
