import os

from solc import compile_source
from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware

from stackXchange.settings import IPC_PATH


def deploy():
    contract_path = os.path.join(os.getcwd(), 'contracts/StackXchange.sol')
    with open(contract_path) as f:
        contract_code = f.read()
    w3 = Web3(Web3.IPCProvider(IPC_PATH))
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)
    w3.personal.unlockAccount(w3.eth.accounts[0], 'voith123')
    compiled_code = compile_source(contract_code)
    contract_interface = compiled_code['<stdin>:StackXchange']
    contract_cls = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = contract_cls.constructor().transact({'from': w3.eth.accounts[0]})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print('deployed contract to: {0}'.format(tx_receipt.contractAddress))


if __name__ == '__main__':
    deploy()
