
class Account:

    def __init__(self, account_id: int, owner_id: int, account_type: str,  amount: int):
        self.account_id = account_id
        self.owner_id = owner_id
        self.account_type = account_type
        self.amount = amount

    def __str__(self):
        return f"id: {self.account_id}, owner: {self.owner_id}, type: {self.account_type} amount: {self.amount}"

    def as_json_dict(self):
        return {
            "account_id":self.account_id,
            "owner_id":self.owner_id,
            "account_type":self.account_type,
            "amount":self.amount
        }