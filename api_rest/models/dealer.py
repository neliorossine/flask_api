# -*- coding: utf-8 -*-

from api_rest.sql_alchemy import db


class DealerModel(db.Model):
    """
        Class responsible to actions in the table 'dealers'
    """

    __tablename__ = "dealers"

    dealer_id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100))
    cpf = db.Column(db.String(11))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))

    def __init__(self, nome_completo, cpf, email, senha):
        """
        Initialize 'dealer' data.
        @param nome_completo:
        @param cpf:
        @param email:
        @param senha:
        """
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.email = email
        self.senha = senha

    def json(self):
        """
        Return 'dealer' data in json format
        @return json
        """
        return {
            "dealer_id": self.dealer_id,
            "nome_completo": self.nome_completo,
            "cpf": self.cpf,
            "email": self.email,
        }

    @classmethod
    def find_dealer(cls, dealer_id):
        """
        Search 'dealer' by id
        @param dealer_id:
        @return dealer
        """
        dealer = cls.query.filter_by(dealer_id=dealer_id).first()
        if dealer:
            return dealer
        return None

    @classmethod
    def find_by_email(cls, email):
        """
        Search 'dealer' by email
        @param email:
        @return email
        """
        email = cls.query.filter_by(email=email).first()
        if email:
            return email
        return None

    def save_dealer(self):
        """
        Save data to the "dealer" table.
        """
        db.session.add(self)
        db.session.commit()

    def delete_dealer(self):
        """
        Delete data in the "dealer" table.
        """
        db.session.delete(self)
        db.session.commit()
