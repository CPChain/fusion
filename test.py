from cpc_fusion import Web3
from multiprocessing import Pool,Process


def sendtx():
    print('sending')
    for i in range(30):
        cf.cpc.sendTransaction(
            {'to': account2, 'from': cf.cpc.coinbase,
             'value': int(10), 'gas': 200000, 'gasPrice': 234512334421})


cf = Web3(Web3.HTTPProvider('http://18.136.195.148:8503'))
cf = Web3(Web3.HTTPProvider('http://127.0.0.1:8501'))

account1 = cf.toChecksumAddress('0xe94b7b6c5a0e526a4d97f9768ad6097bde25c62a')
account2 = cf.toChecksumAddress('0xc05302acebd0730e3a18a058d7d1cb1204c4a092')
# cf.personal.sendTransaction({'to': account2, 'from': cf.cpc.coinbase, 'value': 10})
if __name__ == '__main__':


    print(cf.cpc.blockNumber)



    print('\nunlock:')
    print(cf.personal.unlockAccount(account1, 'password'))
    sendtx()