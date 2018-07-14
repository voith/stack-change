import json
import os
import time

from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware

from stackXchange.settings import IPC_PATH, CONTRACT_ADDRESS


def run_forever():
    abi_path = os.path.join(os.getcwd(), 'contracts/contract_abi.json')
    with open(abi_path, 'r') as f:
        abi = json.loads(f.read())

    w3 = Web3(Web3.IPCProvider(IPC_PATH))
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
    deposit_filter = contract.events.emitDeposit.createFilter(fromBlock=2631584)
    withdraw_filter = contract.events.emitWithdrawn.createFilter(fromBlock=2631584)

    while True:
        deposit_entries = deposit_filter.get_new_entries()
        withdraw_entries = withdraw_filter.get_new_entries()
        if deposit_entries:
            print('got deposit')
            print(deposit_entries)
        if withdraw_entries:
            print('got withdraw')
            print(withdraw_entries)
        time.sleep(10)

if __name__ == '__main__':
    run_forever()
