from flask_app.config.mysqlconnection import connectToMySQL

class User:
    DB = "road_worker_schema"
    def __init__(self, user_dict):
        self.id = user_dict["id"]
        self.first_name = user_dict["first_name"]
        self.last_name = user_dict["last_name"]
        self.email = user_dict["email"]
        self.phone_number = user_dict["phone_number"]
        self.city = user_dict["city"]
        self.state = user_dict["state"]
        self.profile_picture = user_dict["profile_picture"]
        self.password = user_dict["password"]
        self.created_at = user_dict["created_at"]
        self.updated_at = user_dict["updated_at"]

    # write a method to save a user to the database under the certain company name inputed from the admin
    @classmethod
    def create_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def get_user_by_id(cls, user_id):
        query = """SELECT * FROM users WHERE id = %(user_id)s"""
        data = {"user_id": user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def update_user(cls, data):
        query = """UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, phone_number = %(phone_number)s, profile_picture = %(profile_picture)s, password = %(password)s, city = %(city)s, state = %(state)s WHERE id = %(id)s"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def delete_user(cls, user_id):
        query = """DELETE FROM users WHERE id = %(user_id)s"""
        data = {"user_id": user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
