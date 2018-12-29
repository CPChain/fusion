#!/usr/bin/env python3
import json

from cpc_fusion import Web3
# from web3 import Web3

# cf. https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
from cpc_fusion.middleware import geth_poa_middleware
from cpc_fusion.cpc_keyfile import decode_keyfile_json
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

def main():
    from eth_account import Account
    encrypted = Account.encrypt(
        0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364,
        "pppp"
    )
    print("encrypted:")
    print(encrypted)
    # {'address': '5ce9454909639d2d17a3f753ce7d93fa0b9ab12e',
    #  'crypto': {'cipher': 'aes-128-ctr',
    #             'cipherparams': {'iv': '78f214584844e0b241b433d7c3bb8d5f'},
    #             'ciphertext': 'd6dbb56e4f54ba6db2e8dc14df17cb7352fdce03681dd3f90ce4b6c1d5af2c4f',
    #             'kdf': 'pbkdf2',
    #             'kdfparams': {'c': 1000000,
    #                           'dklen': 32,
    #                           'prf': 'hmac-sha256',
    #                           'salt': '45cf943b4de2c05c2c440ef96af914a2'},
    #             'mac': 'f5e1af09df5ded25c96fcf075ada313fb6f79735a914adc8cb02e8ddee7813c3'},
    #  'id': 'b812f3f9-78cc-462a-9e89-74418aa27cb0',
    #  'version': 3}


    # acct = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
    # print(acct.address)
    # '0x5ce9454909639D2D17A3F753ce7d93fa0b9aB12E'
    # acct.privateKey
    # b"\\xb2\\}\\xb3\\x1f\\xee\\xd9\\x12''\\xbf\\t9\\xdcv\\x9a\\x96VK-\\xe4\\xc4rm\\x03[6\\xec\\xf1\\xe5\\xb3d"

    # print("http://127.0.0.1:8545")
    # print(web3.eth.blockNumber)
    # # inject the poa compatibility middleware to the innermost layer
    # web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    #
    with open('./key1') as keyfile:
        encrypted_key = keyfile.read()
    private_key_for_senders_account1 = web3.eth.account.create_keyfile_json(encrypted_key, 'password')
    print( private_key_for_senders_account1)

    print("================================encrypted_key======================\n")
    print(encrypted_key)
    jjj = json.loads(encrypted_key)
    private_key_for_senders_account = decode_keyfile_json(jjj, 'password')

    #
    print("private_key_for_senders_account:")
    # print(private_key_for_senders_account)
    nonce = web3.eth.getTransactionCount(web3.eth.coinbase)
    addr = web3.toChecksumAddress('0xc05302acebd0730e3a18a058d7d1cb1204c4a092')
    print(nonce)
    print(nonce)
    signed_txn = web3.eth.account.signTransaction(dict(
            nonce=nonce,
            gasPrice=web3.eth.gasPrice,
            gas=100000,
            to=addr,
            value=12345,
            data=b'',
        ),
        acct.privateKey,
    )
    print(signed_txn)

    web3.eth.sendRawTransaction(signed_txn.rawTransaction)


if __name__ == '__main__':
    main()
