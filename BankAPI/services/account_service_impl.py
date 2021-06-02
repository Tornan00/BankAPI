from daos.account_dao import AccountDAO
from daos.client_dao import ClientDAO
from entities.account import Account
from entities.client import Client
from exceptions.account_not_found_exception import AccountNotFoundException
from exceptions.invalid_balance_error import InvalidBalanceError
from services.account_service import AccountService

class AccountServiceImpl(AccountService):

    def __init__(self, account_dao: AccountDAO, client_dao: ClientDAO):
        self.account_dao = account_dao
        self.client_dao = client_dao

    def add_account(self, account: Account):
        return self.account_dao.create_account(account)

    def retrieve_all_accounts_for_client(self, client_id: int):
        return self.account_dao.get_all_accounts_by_client_id(client_id)

    def retrieve_account_by_id(self, account_id: int):
        return self.account_dao.get_account_by_id(account_id)

    def update_account(self, account: Account):
        return self.account_dao.update_account(account)

    def remove_account(self, account_id: int):
        result = self.account_dao.delete_account(account_id)
        if result:
            return result
        else:
            raise AccountNotFoundException(f"account with id: {account_id} was not found")

    def get_all_accounts_with_amount(self, client_id: int, lower: int, upper: int) -> list[Account]:
        return self.account_dao.get_all_accounts_with_amount(client_id, lower, upper)

    def change_account_amount(self, account_id: int, deposit: bool, amount: int) -> bool:
        account = self.account_dao.get_account_by_id(account_id)
        if deposit:
            account.amount = account.amount + amount
            self.update_account(account)
            return True
        else:
            if account.amount >= amount:
                account.amount = account.amount - amount
                self.update_account(account)
                return True
            else:
                raise InvalidBalanceError(f"account with id: {account_id} doesn't have enough for this withdrawal")


    def account_transfer(self, giver: Account, receiver: Account, amount: int) -> bool:
        if giver.amount >= amount:
            giver.amount = giver.amount - amount
            receiver.amount = receiver.amount + amount
            self.account_dao.update_account(giver)
            self.account_dao.update_account(receiver)
            return True
        else:
            raise InvalidBalanceError(f"account with id: {giver.account_id} doesn't have enough for this transfer")