from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Certification:
    DB = "road_worker_schema"
    def __init__(self, cert_dict):
        self.id = cert_dict["id"]
        self.user_id = cert_dict["user_id"]
        self.certification_name = cert_dict["certification_name"]
        self.certification_expiration_date = cert_dict["certification_expiration_date"]
        self.certification_number = cert_dict["certification_number"]
        self.created_at = cert_dict["created_at"]
        self.updated_at = cert_dict["updated_at"]

    @classmethod
    def add_cert(cls, data):
        query = """INSERT INTO certifications (user_id, certification_name, certification_expiration_date, certification_number) VALUES (%(user_id)s, %(certification_name)s, %(certification_expiration_date)s, %(certification_number)s)"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def get_user_certs(cls, user_id):
        query = """SELECT * FROM certifications WHERE user_id = %(user_id)s"""
        data = {"user_id": user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)

        certs_list = [cls(cert_dict) for cert_dict in results]
        return certs_list