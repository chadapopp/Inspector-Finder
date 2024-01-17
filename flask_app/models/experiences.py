from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Experiences:
    DB = "road_worker_schema"
    def __init__(self, experience_dict):
        self.id = experience_dict["id"]
        self.user_id = experience_dict["user_id"]
        self.position = experience_dict["position"]
        self.description = experience_dict["description"]
        self.company_name = experience_dict["company_name"]
        self.start_date = experience_dict["start_date"]
        self.end_date = experience_dict["end_date"]
        self.created_at = experience_dict["created_at"]
        self.updated_at = experience_dict["updated_at"]
    
    @classmethod
    def add_experience(cls, data):
        query = """INSERT INTO experiences (user_id, position, company_name, description, start_date, end_date ) VALUES (%(user_id)s, %(position)s, %(company_name)s, %(description)s, %(start_date)s, %(end_date)s)"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def get_user_experience(cls, user_id):
        query = """SELECT * FROM experiences WHERE user_id = %(user_id)s"""
        data = {"user_id": user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)

        experience_list = [cls(experience_dict) for experience_dict in results]

        # Sort the experience_list based on end_date with None values first
        experience_list = sorted(experience_list, key=lambda x: (x.end_date is None, x.end_date), reverse=True)

        return experience_list
    
    @classmethod
    def get_experience_by_id(cls, experience_id):
        query = """SELECT * FROM experiences WHERE id = %(id)s"""
        data = {"id": experience_id}
        result = connectToMySQL(cls.DB).query_db(query, data)

        if result:
            return cls(result[0])  # Assuming result is a list and you want the first item
        else:
            return None  # Return None if no experience found with the given ID
        
    @classmethod
    def update_experience(cls, data):
        query = """
            UPDATE experiences
            SET position = %(position)s,
                company_name = %(company_name)s,
                description = %(description)s,
                start_date = %(start_date)s,
                end_date = %(end_date)s
            WHERE id = %(experience_id)s
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    


