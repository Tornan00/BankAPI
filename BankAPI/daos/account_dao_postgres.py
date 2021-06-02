from typing import List
from daos.account_dao import AccountDAO
from entities.account import Account
from utils.connection_util import connection

class AccountDAOPostgres(AccountDAO):

    def create_account(self, account: Account) -> Account:
        sql = """insert into account values (default, %s, %s, %s) returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.owner_id, account.account_type, account.amount))
        connection.commit()
        a_id = cursor.fetchone()[0]
        account.account_id = a_id
        return account

    def get_account_by_id(self, account_id: int) -> Account:
        sql = """select * from account where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql,[account_id])
        record = cursor.fetchone()
        if record is None:
            return None
        else:
            return Account(*record)

    def get_all_accounts_by_client_id(self, client_id: int) -> List[Account]:
        sql = """select * from account where owner_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql,[client_id])
        records = cursor.fetchall()
        return [Account(*record) for record in records]

    def get_all_accounts_with_amount(self, client_id: int, lower: int, upper: int):
        sql = """select * from account where owner_id = %s and amount > %s and amount < %s"""
        cursor = connection.cursor()
        cursor.execute(sql,(client_id, lower, upper))
        records = cursor.fetchall()
        return [Account(*record) for record in records]

    def update_account(self, account: Account) -> Account:
        sql = """update account set account_type = %s, amount = %s where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.account_type, account.amount, account.account_id))
        connection.commit()
        return account

    def delete_account(self, account_id: int) -> bool:
        sql = """delete from account where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        connection.commit()
        return True