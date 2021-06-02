from abc import ABC, abstractmethod
from entities.account import Account

class AccountService(ABC):

    @abstractmethod
    def add_account(self, account: Account):
        pass

    @abstractmethod
    def retrieve_all_accounts_for_client(self, client_id: int):
        pass

    @abstractmethod
    def retrieve_account_by_id(self, account_id: int):
        pass

    @abstractmethod
    def update_account(self, account: Account):
        pass

    @abstractmethod
    def remove_account(self, account_id: int):
        pass

    @abstractmethod
    def get_all_accounts_with_amount(self, client_id: int, lower: int, upper: int) -> list[Account]:
        pass

    @abstractmethod
    def change_account_amount(self, account_id: int, deposit: bool, amount: int) -> bool:
        pass

    @abstractmethod
    def account_transfer(self, giver: Account, receiver: Account, amount: int) -> bool:
        pass