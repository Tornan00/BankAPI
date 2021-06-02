from daos.client_dao import ClientDAO
from daos.client_dao_postgres import ClientDAOPostgres
from entities.client import Client

client_dao: ClientDAO = ClientDAOPostgres()

test_client = Client(0, "Bill", "Charles")

def test_create_client():
    client_dao.create_client(test_client)
    assert test_client.client_id != 0

def test_get_client_by_id():
    client = client_dao.get_client_by_id(test_client.client_id)
    assert test_client.first_name == client.first_name

def test_get_all_clients():
    client1 = Client(0, "Tim", "Timothy")
    client2 = Client(0, "Sarah", "Lynn")
    client3 = Client(0, "Jill", "Jasons")
    client_dao.create_client(client1)
    client_dao.create_client(client2)
    client_dao.create_client(client3)
    clients = client_dao.get_all_clients()
    assert len(clients) >= 3

def test_update_client():
    test_client.first_name = "Jerry"
    updated_client = client_dao.update_client(test_client)
    assert updated_client.first_name == test_client.first_name

def test_delete_client():
    result = client_dao.delete_client(test_client.client_id)
    assert result