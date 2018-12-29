#!/usr/bin/env python3
import json

from cpc_fusion import Web3
# from web3 import Web3

# cf. https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
from cpc_fusion.middleware import geth_poa_middleware
from cpc_fusion.cpc_keyfile import decode_keyfile_json

# def tx1():
#     web3 = Web3(Web3.HTTPProvider('http://192.168.50.251:8501'))
#     print("http://192.168.50.251:8545")
#     print(web3.cpc.blockNumber)
#     # inject the poa compatibility middleware to the innermost layer
#     web3.middleware_stack.inject(geth_poa_middleware, layer=0)
#     print('to  ', web3.cpc.getBalance(web3.toChecksumAddress('c05302acebd0730e3a18a058d7d1cb1204c4a092')))
#     print('from', web3.cpc.getBalance(web3.toChecksumAddress('e94b7b6c5a0e526a4d97f9768ad6097bde25c62a')))
#
#     print(web3.personal.sendTransaction({'to': web3.toChecksumAddress('c05302acebd0730e3a18a058d7d1cb1204c4a092'),
#                                           'from': web3.toChecksumAddress('e94b7b6c5a0e526a4d97f9768ad6097bde25c62a'),
#                                           'value': 321},
#                                          'password').hex())
#     print('to  ', web3.cpc.getBalance(web3.toChecksumAddress('c05302acebd0730e3a18a058d7d1cb1204c4a092')))
#
#     print('from', web3.cpc.getBalance(web3.toChecksumAddress('e94b7b6c5a0e526a4d97f9768ad6097bde25c62a')))
#
#
def tx2():
    web3 = Web3(Web3.HTTPProvider('http://192.168.50.251:8501'))
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    with open('./keys/key1') as keyfile:
        encrypted_key = keyfile.read()
    # print(web3.cpc.getBalance(web3.cpc.accounts))
    print(web3.cpc.accounts)
    print('balance:', web3.cpc.getBalance(web3.cpc.accounts[0]))
    print("================================encrypted_key======================\n")
    print(encrypted_key)
    jjj = json.loads(encrypted_key)
    private_key_for_senders_account = decode_keyfile_json(jjj, 'password')
    print("private_key_for_senders_account:")
    print(private_key_for_senders_account)

    nonce = web3.cpc.getTransactionCount(web3.cpc.coinbase)
    addr = web3.toChecksumAddress('0xc05302acebd0730e3a18a058d7d1cb1204c4a092')
    fromA = web3.toChecksumAddress('0xe94b7b6c5a0e526a4d97f9768ad6097bde25c62a')
    print(nonce)
    gasPrice = web3.cpc.gasPrice
    print('gasPrice:', web3.cpc.gasPrice)
    ddd = dict(
        type=0,
        nonce=nonce,
        gasPrice=18000000000,
        gas=90000,
        to=addr,
        value=123,
        data=b'',
        extra=b'',
        chainId=41,
    )
    ddd['from'] =  fromA
    signed_txn = web3.cpc.account.signTransaction(ddd,
                 private_key_for_senders_account,
    )
    print("signed_txn:")
    print(signed_txn)

    print("sendRawTransaction:")
    print(web3.toHex(signed_txn.rawTransaction))
    print(web3.cpc.sendRawTransaction(signed_txn.rawTransaction))

def main():
    # tx1()
    tx2()

if __name__ == '__main__':
    main()
