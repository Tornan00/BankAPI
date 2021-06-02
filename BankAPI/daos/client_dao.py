from abc import ABC, abstractmethod
from typing import List
from entities.client import Client

class ClientDAO(ABC):

    # CREATE
    @abstractmethod
    def create_client(self, client: Client) -> Client:
        pass

    # READ
    @abstractmethod
    def get_client_by_id(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def get_all_clients(self) -> List[Client]:
        pass

    # UPDATE
    @abstractmethod
    def update_client(self, client: Client) -> Client:
        pass

    # DELETE
    @abstractmethod
    def delete_client(self, client_id: int) -> bool:
        pass