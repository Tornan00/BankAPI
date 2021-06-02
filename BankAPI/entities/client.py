
class Client:

    def __init__(self, client_id: int, first_name: str, last_name: str):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name


    def __str__(self):
        return f"id: {self.client_id}, first_name: {self.first_name}, last_name: {self.last_name}"

    def as_json_dict(self):
        return {
            "client_id":self.client_id,
            "first_name":self.first_name,
            "last_name":self.last_name
        }