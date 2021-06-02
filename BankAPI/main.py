from flask import Flask, request, jsonify
import logging
from daos.account_dao_postgres import AccountDAOPostgres
from daos.client_dao_postgres import ClientDAOPostgres
from entities.account import Account
from entities.client import Client
from exceptions.client_not_found_exception import ClientNotFoundException
from exceptions.invalid_balance_error import InvalidBalanceError
from services.account_service_impl import AccountServiceImpl
from services.client_service_impl import ClientServiceImpl

app: Flask = Flask(__name__)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

client_dao = ClientDAOPostgres()
account_dao = AccountDAOPostgres()
client_service = ClientServiceImpl(client_dao)
account_service = AccountServiceImpl(account_dao, client_dao)

@app.route("/clients", methods = ["POST"])
def create_client():
    body = request.get_json()
    client = Client(body["client_id"], body["first_name"], body["last_name"])
    client_service.add_client(client)
    return f"Created client with id {client.client_id}", 201

@app.route("/clients/<client_id>", methods = ["GET"])
def get_client_by_id(client_id: str):
    client = client_service.retrieve_client_by_id(int(client_id))
    if client is None:
        return "A client with the given id could not be found", 404
    return jsonify(client.as_json_dict())

@app.route("/clients", methods = ["GET"])
def get_all_clients():
    clients = client_service.retrieve_all_clients()
    json_clients = [c.as_json_dict() for c in clients]
    return jsonify(json_clients)

@app.route("/clients/<client_id>", methods = ["PUT"])
def update_client(client_id: str):
    body = request.get_json()
    client = Client(body["client_id"], body["first_name"], body["last_name"])
    client.client_id = int(client_id)
    result = client_service.update_client(client)
    if result is None:
        return "A client with the given id could not be found", 404
    else:
        return f"Client with id {client_id} updated successfully"

@app.route("/clients/<client_id>", methods = ["DELETE"])
def delete_client(client_id: str):
    try:
        result = account_service.retrieve_all_accounts_for_client(int(client_id))
        if len(result) == 0:
            client_service.remove_client(int(client_id))
            return "Deleted Successfully", 205
        else:
            return "Cannot delete a client with active accounts", 422
    except ClientNotFoundException as e:
        return str(e), 404

@app.route("/clients/<client_id>/accounts", methods = ["POST"])
def create_account(client_id: str):
    client = client_service.retrieve_client_by_id(int(client_id))
    if client is None:
        return "A client with the given id could not be found", 404

    body = request.get_json()
    account = Account(body["account_id"], int(client_id), body["account_type"], body["amount"])
    account_service.add_account(account)
    return f"Created account with id {account.account_id}", 201

@app.route("/clients/<client_id>/accounts", methods = ["GET"])
def get_all_accounts_by_client_id(client_id: str):
    client = client_service.retrieve_client_by_id(int(client_id))
    if client is None:
        return "A client with the given id could not be found", 404

    accounts = []
    lower = request.args.get("amountGreaterThan")
    upper = request.args.get("amountLessThan")

    if lower is not None:
        accounts += account_service.get_all_accounts_with_amount(int(client_id), int(lower), int(upper))
    else:
        accounts += account_service.retrieve_all_accounts_for_client(int(client_id))

    json_accounts = [a.as_json_dict() for a in accounts]
    return jsonify(json_accounts)

@app.route("/clients/<client_id>/accounts/<account_id>", methods = ["GET"])
def get_account_by_account_id(client_id: str, account_id: str):
    client = client_service.retrieve_client_by_id(int(client_id))
    if client is None:
        return "A client with the given id could not be found", 404

    account = account_service.retrieve_account_by_id(int(account_id))
    if account is None:
        return "An account with the given id could not be found", 404
    return jsonify(account.as_json_dict())

@app.route("/clients/<client_id>/accounts/<account_id>", methods = ["PUT"])
def update_account(client_id: str, account_id: str):
    client = client_service.retrieve_client_by_id(int(client_id))
    if client is None:
        return "A client with the given id could not be found", 404

    account = account_service.retrieve_account_by_id(int(account_id))
    if account is None:
        return "An account with the given id could not be found", 404

    body = request.get_json()
    account = Account(int(account_id), body["owner_id"], body["account_type"], body["amount"])
    result = account_service.update_account(account)
    return f"Account with id {account_id} updated successfully"

@app.route("/clients/<client_id>/accounts/<account_id>", methods = ["DELETE"])
def delete_account(client_id: str, account_id: str):
    client = client_service.retrieve_client_by_id(int(client_id))
    if client is None:
        return "A client with the given id could not be found", 404

    account = account_service.retrieve_account_by_id(int(account_id))
    if account is None:
        return "An account with the given id could not be found", 404

    account_service.remove_account(int(account_id))
    return "Deleted Successfully", 205

@app.route("/clients/<client_id>/accounts/<account_id>", methods = ["PATCH"])
def account_transaction(client_id: str, account_id: str):
    client = client_service.retrieve_client_by_id(int(client_id))
    if client is None:
        return "A client with the given id could not be found", 404

    account = account_service.retrieve_account_by_id(int(account_id))
    if account is None:
        return "An account with the given id could not be found", 404

    body = request.get_json()
    try:
        deposit = int(body["deposit"])
    except KeyError as e:
        deposit = -1
    try:
        withdraw = int(body["withdraw"])
    except KeyError as e:
        withdraw = -1

    print(f"HERE {deposit} {withdraw}")

    if deposit != -1:
        try:
            account_service.change_account_amount(int(account_id), True, deposit)
            return "Deposited funds successfully", 200
        except InvalidBalanceError as e:
            return str(e), 422
    else:
        try:
            account_service.change_account_amount(int(account_id), False, withdraw)
            return "Withdrew funds successfully", 200
        except InvalidBalanceError as e:
            return str(e), 422

@app.route("/clients/<client_id>/accounts/<account_id>/transfer/<transfer_id>", methods = ["PATCH"])
def account_transfer(client_id: str, account_id: str, transfer_id: str):
    client = client_service.retrieve_client_by_id(int(client_id))
    if client is None:
        return "A client with the given id could not be found", 404

    from_account = account_service.retrieve_account_by_id(int(account_id))
    if from_account is None:
        return "An account with the given id could not be found", 404
    to_account = account_service.retrieve_account_by_id(int(transfer_id))
    if to_account is None:
        return "An account with the given id could not be found", 404

    body = request.get_json()
    amount = int(body["amount"])

    try:
        account_service.account_transfer(from_account, to_account, amount)
        return "Transfer completed successfully", 200
    except InvalidBalanceError as e:
        return str(e), 422

if __name__ == '__main__':
    app.run()
