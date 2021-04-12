"""

Default contracts

+ Addr
+ ABI
"""
import getpass
import sys
import logging
import json

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
                log.info("You have already been RNode.")
                return
            gas_price = self.cf.cpc.gasPrice
            nonce = self.cf.cpc.getTransactionCount(addr)
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

    def quit(self, keystorePath):
        with open(keystorePath, 'r') as fr:
            ks = json.load(fr)
            addr = self.cf.toChecksumAddress(ks['address'])
            is_rnode = self.instance.functions.isRnode(addr).call()
            if not is_rnode:
                log.info("You are not RNode now.")
                return
            gas_price = self.cf.cpc.gasPrice
            nonce = self.cf.cpc.getTransactionCount(addr)
            log.info("Start quit RNode...")
            tx = self.instance.functions.quitRnode().buildTransaction({
                'gasPrice': gas_price,
                "nonce": nonce,  
                "gas": 300000,
                "from": addr,
                "value": 0,
                "type": 0,
                "chainId": 337
            })
            password = getpass.getpass("Please input your password:")
            decrypted_key = self.cf.cpc.account.decrypt(ks, password)
            password = ""
            signed_txn = self.cf.cpc.account.signTransaction(tx, decrypted_key)
            tx_hash = self.cf.cpc.sendRawTransaction(signed_txn.rawTransaction)
            receipt = self.cf.cpc.waitForTransactionReceipt(tx_hash)
            if receipt.status == 0:
                log.info('Sorry, quit failed, maybe this because you quitted in the locked period. Or maybe you are a proposer now.')
            else:
                log.info('Success')
            log.info(f'Please check https://cpchain.io/explorer/address/{addr}')


class Campaign:
    """ Campaign
    """
    addr = '0x2A186bE66Dd20c1699Add34A49A3019a93a7Fcd0'
    abi = '[{\"constant\":true,\"inputs\":[],\"name\":\"termLen\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"_termIdx\",\"type\":\"uint256\"}],\"name\":\"candidatesOf\",\"outputs\":[{\"name\":\"\",\"type\":\"address[]\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_termsToCampaign\",\"type\":\"uint256\"},{\"name\":\"_cpuNonce\",\"type\":\"uint64\"},{\"name\":\"_cpuBlockNumber\",\"type\":\"uint256\"},{\"name\":\"_memoryNonce\",\"type\":\"uint64\"},{\"name\":\"_memoryBlockNumber\",\"type\":\"uint256\"},{\"name\":\"version\",\"type\":\"uint256\"}],\"name\":\"claimCampaign\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"termIdx\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"minNoc\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"numPerRound\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"viewLen\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_supportedVersion\",\"type\":\"uint256\"}],\"name\":\"updateSupportedVersion\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_maxNoc\",\"type\":\"uint256\"}],\"name\":\"updateMaxNoc\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_minNoc\",\"type\":\"uint256\"}],\"name\":\"updateMinNoc\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"acceptableBlocks\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_addr\",\"type\":\"address\"}],\"name\":\"setAdmissionAddr\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_termLen\",\"type\":\"uint256\"}],\"name\":\"updateTermLen\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"supportedVersion\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_acceptableBlocks\",\"type\":\"uint256\"}],\"name\":\"updateAcceptableBlocks\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"_candidate\",\"type\":\"address\"}],\"name\":\"candidateInfoOf\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"},{\"name\":\"\",\"type\":\"uint256\"},{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"maxNoc\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_addr\",\"type\":\"address\"}],\"name\":\"setRnodeInterface\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"name\":\"_admissionAddr\",\"type\":\"address\"},{\"name\":\"_rnodeAddr\",\"type\":\"address\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"fallback\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"candidate\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"startTermIdx\",\"type\":\"uint256\"},{\"indexed\":false,\"name\":\"stopTermIdx\",\"type\":\"uint256\"}],\"name\":\"ClaimCampaign\",\"type\":\"event\"}]'

    def __init__(self, cf, addr:str=None, abi:str=None) -> None:
        self.cf = cf
        if addr:
            self.addr = addr
        if abi:
            self.abi = abi
        self.instance = cf.cpc.contract(abi=self.abi, address=self.addr)


    @property
    def supported_version(self):
        return self.instance.functions.supportedVersion().call()

    @property
    def term_idx(self):
        return self.instance.functions.termIdx().call()
    
    @property
    def view_len(self):
        return self.instance.functions.viewLen().call()

    @property
    def term_len(self):
        return self.instance.functions.termLen().call()

    @property
    def min_noc(self):
        return self.instance.functions.minNoc().call()
    
    @property
    def max_noc(self):
        return self.instance.functions.maxNoc().call()
