"""

Default contracts

+ Addr
+ ABI
"""
import getpass
import sys
import logging
import json

log = logging.getLogger()

class RNode:
    """ RNode contract
    """
    addr = '0x76130DA5aA1851313a7555D3735BED76029560DA'
    abi = "[{\"constant\":true,\"inputs\":[],\"name\":\"getRnodeNum\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_period\",\"type\":\"uint256\"}],\"name\":\"setPeriod\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"quitRnode\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"addr\",\"type\":\"address\"}],\"name\":\"isContract\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"enabled\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"enableContract\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"refundAll\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"\",\"type\":\"address\"}],\"name\":\"Participants\",\"outputs\":[{\"name\":\"lockedDeposit\",\"type\":\"uint256\"},{\"name\":\"lockedTime\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"version\",\"type\":\"uint256\"}],\"name\":\"setSupportedVersion\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"disableContract\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"threshold\",\"type\":\"uint256\"}],\"name\":\"setRnodeThreshold\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"addr\",\"type\":\"address\"}],\"name\":\"isRnode\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"version\",\"type\":\"uint256\"}],\"name\":\"joinRnode\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"rnodeThreshold\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"supportedVersion\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"getRnodes\",\"outputs\":[{\"name\":\"\",\"type\":\"address[]\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"period\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"investor\",\"type\":\"address\"}],\"name\":\"refund\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"lockedDeposit\",\"type\":\"uint256\"},{\"indexed\":false,\"name\":\"lockedTime\",\"type\":\"uint256\"}],\"name\":\"NewRnode\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"}],\"name\":\"RnodeQuit\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"ownerRefund\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"numOfInvestor\",\"type\":\"uint256\"}],\"name\":\"ownerRefundAll\",\"type\":\"event\"}]"

    def __init__(self, cf, addr:str=None, abi:str=None) -> None:
        self.cf = cf
        if addr:
            self.addr = addr
        if abi:
            self.abi = abi
        self.instance = cf.cpc.contract(abi=self.abi, address=self.addr)

    @property
    def period(self):
        return self.instance.functions.period().call()

    @property
    def threshold(self):
        return self.instance.functions.rnodeThreshold().call()
    
    @property
    def supported_version(self):
        return self.instance.functions.supportedVersion().call()

    def is_rnode(self, addr):
        return self.instance.functions.isRnode(self.cf.toChecksumAddress(addr)).call()
    
    @property
    def rnodes_num(self):
        return self.instance.functions.getRnodeNum().call()

    @property
    def rnodes(self):
        return self.instance.functions.getRnodes().call()

    def join(self, keystorePath):
        version = self.supported_version
        log.info('version: %d', version)
        with open(keystorePath, 'r') as fr:
            ks = json.load(fr)
            addr = self.cf.toChecksumAddress(ks['address'])
            is_rnode = self.instance.functions.isRnode(addr).call()
            if is_rnode:
                log.info("This address has already been RNode now.")
                return
            gas_price = self.cf.cpc.gasPrice
            nonce = self.cf.cpc.getTransactionCount(addr)
            if not is_rnode:
                log.info("Start join RNode...")
                tx = self.instance.functions.joinRnode(version).buildTransaction({
                    'gasPrice': gas_price,
                    "nonce": nonce,  
                    "gas": 300000,
                    "from": addr,
                    "value": self.cf.toWei(200000, 'ether'),
                    "type": 0,
                    "chainId": 337
                })
                password = getpass.getpass("Please input your password:")
                decrypted_key = self.cf.cpc.account.decrypt(ks, password)
                password = ""
                signed_txn = self.cf.cpc.account.signTransaction(tx, decrypted_key)
                tx_hash = self.cf.cpc.sendRawTransaction(signed_txn.rawTransaction)
                self.cf.cpc.waitForTransactionReceipt(tx_hash)
                log.info(f'Success')
