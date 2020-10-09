# -*- coding: utf-8 -*-

from api_rest.sql_alchemy import db


class SaleModel(db.Model):
    """
        Class responsible to actions in the table 'sales'
    """

    __tablename__ = "sales"

    sale_id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20))
    valor = db.Column(db.Float(precision=2))
    data = db.Column(db.Text)
    cpf = db.Column(db.String(11))
    status = db.Column(db.String(20))
    percent_cashback = db.Column(db.Integer)
    valor_cashback = db.Column(db.Float(precision=2))

    def __init__(self, codigo, valor, data, cpf, status):
        """
        Initialize 'sale' data.
        @param codigo:
        @param valor:
        @param data:
        @param cpf:
        @param status:
        """
        self.codigo = codigo
        self.valor = valor
        self.data = data
        self.cpf = cpf
        self.status = status

    def json(self):
        """
        Return 'sale' data in json format
        @return json
        """
        return {
            "sale_id": self.sale_id,
            "codigo": self.codigo,
            "valor": self.valor,
            "data": self.data,
            "cpf": self.cpf,
            "status": self.status,
            "percent_cashback": str(self.percent_cashback) + "%",
            "valor_cashback": round(self.valor_cashback, 2),
        }

    @classmethod
    def find_sale(cls, sale_id):
        """
        Search 'sale' by id
        @param sale_id:
        @return 'sale json' if find sale, otherwise None
        """
        sale = cls.query.filter_by(
            sale_id=sale_id
        ).first()  # SELECT * FOM sales WHERE sale_id = $sale_id LIMIT 1

        if sale:
            return sale
        return None

    @classmethod
    def find_sale_by_codigo(cls, codigo):
        """
        Search 'dealer' by codigo
        @param codigo:
        @return 'sale json' if find sale, otherwise None
        """
        sale = cls.query.filter_by(
            codigo=codigo
        ).first()  # SELECT * FOM sales WHERE codigo = $codigo LIMIT 1

        if sale:
            return sale
        return None

    def save_sale(self):
        """
        Save data to the "sales" table.
        @return True
        """
        db.session.add(self)
        db.session.commit()
        return True

    def insert_sale(self, percent_cashback, valor_cashback):
        """
        Insert data in the "sales" table
        @param percent_cashback:
        @param valor_cashback:
        @return True
        """
        self.percent_cashback = percent_cashback
        self.valor_cashback = valor_cashback
        self.save_sale()
        return True

    def update_sale(self, codigo, valor, data, cpf, status):
        """
        Updates data in the "sales" table
        @param codigo:
        @param valor:
        @param data:
        @param cpf:
        @param status:
        @return False if status is not Aprovado, otherwise True
        """
        if self.status == "Aprovado":
            return False

        self.codigo = codigo
        self.valor = valor
        self.data = data
        self.cpf = cpf
        self.status = status
        self.save_sale()
        return True

    def delete_sale(self):
        """
        Delete data in the "sale" table and check if it gets 'Aprovado' status
        @return False if status is not Aprovado, otherwise True
        """
        if self.status == "Aprovado":
            return False

        db.session.delete(self)
        db.session.commit()
        return True
