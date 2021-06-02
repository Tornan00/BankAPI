from daos.account_dao import AccountDAO
from daos.account_dao_postgres import AccountDAOPostgres
from daos.client_dao import ClientDAO
from daos.client_dao_postgres import ClientDAOPostgres
from entities.account import Account
from entities.client import Client

client_dao: ClientDAO = ClientDAOPostgres()
account_dao: AccountDAO = AccountDAOPostgres()

test_client = Client(0, "Bill", "Charles")
test_account = Account(0, 0, "checking", 1000000)

def test_create_account():
    client_dao.create_client(test_client)
    test_account.owner_id = test_client.client_id
    account_dao.create_account(test_account)
    assert test_account.account_id != 0

def test_get_account_by_id():
    account = account_dao.get_account_by_id(test_account.account_id)
    assert test_account.amount == account.amount

def test_get_all_accounts_by_client_id():
    account1 = Account(0, test_client.client_id, "savings", 5)
    account2 = Account(0, test_client.client_id, "retirement", 50000)
    account_dao.create_account(account1)
    account_dao.create_account(account2)
    accounts = account_dao.get_all_accounts_by_client_id(test_client.client_id)
    assert len(accounts) >= 2

def test_get_all_accounts_with_amount():
    accounts = account_dao.get_all_accounts_with_amount(test_client.client_id,0,10)
    assert len(accounts) >= 1

def test_update_account():
    test_client.amount = -100
    updated_account = account_dao.update_account(test_account)
    assert updated_account.amount == test_account.amount

def test_delete_client():
    result = account_dao.delete_account(test_account.account_id)
    assert result