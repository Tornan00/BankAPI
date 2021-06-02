from daos.account_dao import AccountDAO
from daos.client_dao import ClientDAO
from entities.client import Client
from exceptions.client_not_found_exception import ClientNotFoundException
from services.client_service import ClientService


class ClientServiceImpl(ClientService):

    def __init__(self, client_dao: ClientDAO):
        self.client_dao = client_dao

    def add_client(self, client: Client):
        return self.client_dao.create_client(client)

    def retrieve_all_clients(self):
        return self.client_dao.get_all_clients()

    def retrieve_client_by_id(self, client_id: int):
        return self.client_dao.get_client_by_id(client_id)

    def update_client(self, client: Client):
        existing_client = self.client_dao.get_client_by_id(client.client_id)
        if existing_client is None:
            return None
        else:
            return self.client_dao.update_client(client)

    def remove_client(self, client_id: int):
        client = self.retrieve_client_by_id(client_id)
        if client is not None:
                result = self.client_dao.delete_client(client_id)
                return result
        else:
            raise ClientNotFoundException(f"client of id: {client_id} doesn't exist")