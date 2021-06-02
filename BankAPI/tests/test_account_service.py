from unittest.mock import MagicMock
from daos.account_dao_postgres import AccountDAOPostgres
from daos.client_dao_postgres import ClientDAOPostgres
from entities.account import Account
from entities.client import Client
from services.account_service import AccountService
from services.account_service_impl import AccountServiceImpl
from services.client_service import ClientService
from services.client_service_impl import ClientServiceImpl

accounts = [Account(0, 2, 'checking', 1000),
            Account(0, 2, 'savings', 5),
            Account(0, 2, 'checking', 120000)]

test_client = Client(0, 'Bill', 'Larson')

mock_account_dao = AccountDAOPostgres()
mock_client_dao = ClientDAOPostgres()
#mock_account_dao.get_all_accounts_by_client_id = MagicMock(return_value = accounts)
#mock_client_dao.get_all_clients = MagicMock(return_value = clients)

client_service: ClientService = ClientServiceImpl(mock_client_dao)
account_service: AccountService = AccountServiceImpl(mock_account_dao, mock_client_dao)

return_client: Client = client_service.add_client(test_client)
accounts[0].owner_id = return_client.client_id
accounts[1].owner_id = return_client.client_id
accounts[2].owner_id = return_client.client_id
return_account1: Account = account_service.add_account(accounts[0])
return_account2: Account = account_service.add_account(accounts[1])
return_account3: Account = account_service.add_account(accounts[2])

def test_get_all_accounts_with_amount():
    result = account_service.get_all_accounts_with_amount(return_client.client_id, 0, 10)
    assert result[0].amount == return_account2.amount

def test_change_account_amount():
    result = account_service.change_account_amount(return_account1.account_id, True, 500)
    assert result

def test_account_transfer():
    result = account_service.account_transfer(return_account1, return_account3, 500)
    assert result