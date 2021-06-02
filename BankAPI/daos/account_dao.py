from abc import ABC, abstractmethod
from typing import List
from entities.account import Account

class AccountDAO(ABC):

    # CREATE
    @abstractmethod
    def create_account(self, account: Account) -> Account:
        pass

    # READ
    @abstractmethod
    def get_account_by_id(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_accounts_by_client_id(self, client_id: int) -> List[Account]:
        pass

    @abstractmethod
    def get_all_accounts_with_amount(self, client_id: int, lower: int, upper: int):
        pass

    # UPDATE
    @abstractmethod
    def update_account(self, account: Account) -> Account:
        pass

    # DELETE
    @abstractmethod
    def delete_account(self, account_id: int) -> bool:
        pass