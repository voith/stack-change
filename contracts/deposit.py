import json
import os

from eth_utils import  to_hex
from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware

from stackXchange.settings import IPC_PATH, CONTRACT_ADDRESS

abi_path = os.path.join(os.getcwd(), 'contracts/contract_abi.json')
with open(abi_path, 'r') as f:
    abi = json.loads(f.read())
w3 = Web3(Web3.IPCProvider(IPC_PATH))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=to_hex(CONTRACT_ADDRESS), abi=abi)


def deposit(account_id, amount):
    tx_hash = contract.functions.deposit(str(account_id)).transact(
        {'from': w3.eth.accounts[0], 'value': w3.toWei(amount, 'ether')}
    )
    return w3.eth.waitForTransactionReceipt(tx_hash)


def withdraw(account_id, amount):
    return contract.functions.withDraw(
        w3.eth.accounts[1], str(account_id), w3.toWei(amount, 'ether')
    ).transact({'from': w3.eth.accounts[0]})
