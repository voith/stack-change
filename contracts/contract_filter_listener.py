from stackXchange.wsgi import application
import json
import os
import time


from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware

from app.models import Balance,  User
from stackXchange.settings import IPC_PATH, CONTRACT_ADDRESS


abi_path = os.path.join(os.getcwd(), 'contracts/contract_abi.json')
with open(abi_path, 'r') as f:
    abi = json.loads(f.read())

w3 = Web3(Web3.IPCProvider(IPC_PATH))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)


def deposit_balance(account_id, amount):
    user = User.objects.get(account_id=account_id)
    balance = Balance.objects.get_or_create(user_id=user.id)[0]
    balance.amount += w3.fromWei(amount, 'ether')
    balance.save()


def run_forever():
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
    deposit_filter = contract.events.emitDeposit.createFilter(fromBlock=2631584)

    while True:
        deposit_entries = deposit_filter.get_new_entries()
        if deposit_entries:
            print('got deposit')
            for entry in deposit_entries:
                account_id = int(entry.args.accountId)
                amount = entry.args._amt
                deposit_balance(account_id, amount)
        time.sleep(10)

if __name__ == '__main__':
    run_forever()
