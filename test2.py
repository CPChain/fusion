#!/usr/bin/env python3
import json

from cpc_fusion import Web3
# from web3 import Web3

# cf. https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
from cpc_fusion.middleware import geth_poa_middleware
from cpc_fusion.cpc_keyfile import decode_keyfile_json
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8501'))

def main():
    print("http://127.0.0.1:8545")
    print(web3.cpc.blockNumber)
    # inject the poa compatibility middleware to the innermost layer
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)

    with open('./key1') as keyfile:
        encrypted_key = keyfile.read()
    private_key_for_senders_account1 = web3.cpc.account.decrypt(encrypted_key, 'password')
    print( private_key_for_senders_account1)

    print("================================encrypted_key======================\n")
    print(encrypted_key)
    jjj = json.loads(encrypted_key)
    private_key_for_senders_account = decode_keyfile_json(jjj, 'password')


    print("private_key_for_senders_account:")
    print(private_key_for_senders_account)
    nonce = web3.cpc.getTransactionCount(web3.cpc.coinbase)
    addr = web3.toChecksumAddress('0xc05302acebd0730e3a18a058d7d1cb1204c4a092')
    print(nonce)
    signed_txn = web3.cpc.account.signTransaction(dict(
            nonce=nonce,
            gasPrice=web3.cpc.gasPrice,
            gas=100000,
            to=addr,
            value=12345,
            data=b'',
        ),
        private_key_for_senders_account,
    )

    web3.cpc.sendRawTransaction(signed_txn.rawTransaction)


if __name__ == '__main__':
    main()
