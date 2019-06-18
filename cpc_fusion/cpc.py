from cpc_fusion.pkgs.account import (
    Account,
)
from eth_utils import (
    apply_to_return_value,
    is_checksum_address,
    is_string,
)
from hexbytes import (
    HexBytes,
)

from cpc_fusion._utils.blocks import (
    select_method_for_block_identifier,
)
from cpc_fusion._utils.decorators import (
    deprecated_for,
)
from cpc_fusion._utils.empty import (
    empty,
)
from cpc_fusion._utils.encoding import (
    to_hex,
)
from cpc_fusion._utils.filters import (
    BlockFilter,
    LogFilter,
    TransactionFilter,
)
from cpc_fusion._utils.threads import (
    Timeout,
)
from cpc_fusion._utils.toolz import (
    assoc,
    merge,
)
from cpc_fusion._utils.transactions import (
    assert_valid_transaction_params,
    extract_valid_transaction_params,
    get_buffered_gas_estimate,
    get_required_transaction,
    replace_transaction,
    wait_for_transaction_receipt,
)
from cpc_fusion.contract import (
    Contract,
)
from cpc_fusion.exceptions import (
    TimeExhausted,
)
from cpc_fusion.iban import (
    Iban,
)
from cpc_fusion.module import (
    Module,
)


def Web3():
    from cpc_fusion import Web3
    return Web3


class CPC(Module):
    account = Account()
    defaultAccount = empty
    defaultBlock = "latest"
    defaultContractFactory = Contract
    iban = Iban
    gasPriceStrategy = None

    @deprecated_for("doing nothing at all")
    def enable_unaudited_features(self):
        pass

    def namereg(self):
        raise NotImplementedError()

    def icapNamereg(self):
        raise NotImplementedError()

    @property
    def protocolVersion(self):
        return self.web3.manager.request_blocking("eth_protocolVersion", [])

    @property
    def syncing(self):
        return self.web3.manager.request_blocking("eth_syncing", [])

    @property
    def coinbase(self):
        return self.web3.manager.request_blocking("eth_coinbase", [])

    @property
    def mining(self):
        return self.web3.manager.request_blocking("eth_mining", [])

    @property
    def gasPrice(self):
        return self.web3.manager.request_blocking("eth_gasPrice", [])

    @property
    def accounts(self):
        return self.web3.manager.request_blocking("eth_accounts", [])

    @property
    def blockNumber(self):
        return self.web3.manager.request_blocking("eth_blockNumber", [])

    def getBalance(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "eth_getBalance",
            [account, block_identifier],
        )

    def getStorageAt(self, account, position, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "eth_getStorageAt",
            [account, position, block_identifier]
        )

    def getCode(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "eth_getCode",
            [account, block_identifier],
        )

    def getBlock(self, block_identifier, full_transactions=False):
        """
        `eth_getBlockByHash`
        `eth_getBlockByNumber`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='eth_getBlockByNumber',
            if_hash='eth_getBlockByHash',
            if_number='eth_getBlockByNumber',
        )

        return self.web3.manager.request_blocking(
            method,
            [block_identifier, full_transactions],
        )

    def getBlockTransactionCount(self, block_identifier):
        """
        `eth_getBlockTransactionCountByHash`
        `eth_getBlockTransactionCountByNumber`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='eth_getBlockTransactionCountByNumber',
            if_hash='eth_getBlockTransactionCountByHash',
            if_number='eth_getBlockTransactionCountByNumber',
        )
        return self.web3.manager.request_blocking(
            method,
            [block_identifier],
        )

    def getTransaction(self, transaction_hash):
        return self.web3.manager.request_blocking(
            "eth_getTransactionByHash",
            [transaction_hash],
        )

    @deprecated_for("w3.eth.getTransactionByBlock")
    def getTransactionFromBlock(self, block_identifier, transaction_index):
        """
        Alias for the method getTransactionByBlock
        Depreceated to maintain naming consistency with the json-rpc API
        """
        return self.getTransactionByBlock(block_identifier, transaction_index)

    def getTransactionByBlock(self, block_identifier, transaction_index):
        """
        `eth_getTransactionByBlockHashAndIndex`
        `eth_getTransactionByBlockNumberAndIndex`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='eth_getTransactionByBlockNumberAndIndex',
            if_hash='eth_getTransactionByBlockHashAndIndex',
            if_number='eth_getTransactionByBlockNumberAndIndex',
        )
        return self.web3.manager.request_blocking(
            method,
            [block_identifier, transaction_index],
        )

    def getAllTransactionsByBlock(self, block_number, frm=0, to=None, batch=10000):
        """
        `eth_getAllTransactionsByBlockNumberAndIndex`
        """
        method = 'eth_getAllTransactionsByBlockNumberAndIndex'
        if not to:
            to = self.getBlockTransactionCount(block_number)
        results = []
        for i in range(frm, to, batch):
            right = i
            left = i + batch - 1 if i + batch - 1 < to else to
            batch_data = self.web3.manager.request_blocking(
                method,
                [block_number, right, left],
            )
            results += batch_data
            if left >= to:
                break
        return results

    def waitForTransactionReceipt(self, transaction_hash, timeout=120):
        try:
            return wait_for_transaction_receipt(self.web3, transaction_hash, timeout)
        except Timeout:
            raise TimeExhausted(
                "Transaction {} is not in the chain, after {} seconds".format(
                    transaction_hash,
                    timeout,
                )
            )

    @property
    def getRNodes(self):
        return self.web3.manager.request_blocking(
            "eth_getRNodes",
            [],
        )

    @property
    def getCurrentView(self):
        return self.web3.manager.request_blocking(
            "eth_getCurrentView",
            [],
        )

    @property
    def getCurrentTerm(self):
        return self.web3.manager.request_blocking(
            "eth_getCurrentTerm",
            [],
        )

    @property
    def getBlockGenerationInfo(self):
        return self.web3.manager.request_blocking(
            "eth_getBlockGenerationInfo",
            [],
        )

    def confirmBlock(self, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        try:
            block = self.getBlock(block_identifier)
            hash = block.get('hash')
            number = block.get('number')
        except AttributeError:
            return False
        try:
            parentHash = self.getBlock(number + 1).get('parentHash')
        except AttributeError:
            return False
        return parentHash == hash

    def getProposerByBlock(self, block):
        if not isinstance(block, str):
            block = self.web3.toHex(block)
        return self.web3.manager.request_blocking(
            "eth_getProposerByBlock",
            [block],
        )

    def getTransactionReceipt(self, transaction_hash):
        return self.web3.manager.request_blocking(
            "eth_getTransactionReceipt",
            [transaction_hash],
        )

    def getTransactionCount(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "eth_getTransactionCount",
            [
                account,
                block_identifier,
            ],
        )

    def replaceTransaction(self, transaction_hash, new_transaction):
        current_transaction = get_required_transaction(self.web3, transaction_hash)
        return replace_transaction(self.web3, current_transaction, new_transaction)

    def modifyTransaction(self, transaction_hash, **transaction_params):
        assert_valid_transaction_params(transaction_params)
        current_transaction = get_required_transaction(self.web3, transaction_hash)
        current_transaction_params = extract_valid_transaction_params(current_transaction)
        new_transaction = merge(current_transaction_params, transaction_params)
        return replace_transaction(self.web3, current_transaction, new_transaction)

    def sendTransaction(self, transaction):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        if 'type' not in transaction:
            transaction['type'] = '0x0'
        else:
            if type(transaction['type'] == int):
                transaction['type'] = hex(transaction['type'])

            # TODO: move gas estimation in middleware
        if 'gas' not in transaction:
            transaction = assoc(
                transaction,
                'gas',
                get_buffered_gas_estimate(self.web3, transaction),
            )
        return self.web3.manager.request_blocking(
            "eth_sendTransaction",
            [transaction],
        )

    def sendRawTransaction(self, raw_transaction):
        return self.web3.manager.request_blocking(
            "eth_sendRawTransaction",
            [raw_transaction],
        )

    def sign(self, account, data=None, hexstr=None, text=None):
        message_hex = to_hex(data, hexstr=hexstr, text=text)
        return self.web3.manager.request_blocking(
            "eth_sign", [account, message_hex],
        )

    @apply_to_return_value(HexBytes)
    def call(self, transaction, block_identifier=None):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        # TODO: move to middleware
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "eth_call",
            [transaction, block_identifier],
        )

    def estimateGas(self, transaction, block_identifier=None):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        if block_identifier is None:
            params = [transaction]
        else:
            params = [transaction, block_identifier]

        return self.web3.manager.request_blocking(
            "eth_estimateGas",
            params,
        )

    def filter(self, filter_params=None, filter_id=None):
        if filter_id and filter_params:
            raise TypeError(
                "Ambiguous invocation: provide either a `filter_params` or a `filter_id` argument. "
                "Both were supplied."
            )
        if is_string(filter_params):
            if filter_params == "latest":
                filter_id = self.web3.manager.request_blocking(
                    "eth_newBlockFilter", [],
                )
                return BlockFilter(self.web3, filter_id)
            elif filter_params == "pending":
                filter_id = self.web3.manager.request_blocking(
                    "eth_newPendingTransactionFilter", [],
                )
                return TransactionFilter(self.web3, filter_id)
            else:
                raise ValueError(
                    "The filter API only accepts the values of `pending` or "
                    "`latest` for string based filters"
                )
        elif isinstance(filter_params, dict):
            _filter_id = self.web3.manager.request_blocking(
                "eth_newFilter",
                [filter_params],
            )
            return LogFilter(self.web3, _filter_id)
        elif filter_id and not filter_params:
            return LogFilter(self.web3, filter_id)
        else:
            raise TypeError("Must provide either filter_params as a string or "
                            "a valid filter object, or a filter_id as a string "
                            "or hex.")

    def getFilterChanges(self, filter_id):
        return self.web3.manager.request_blocking(
            "eth_getFilterChanges", [filter_id],
        )

    def getFilterLogs(self, filter_id):
        return self.web3.manager.request_blocking(
            "eth_getFilterLogs", [filter_id],
        )

    def getLogs(self, filter_params):
        return self.web3.manager.request_blocking(
            "eth_getLogs", [filter_params],
        )

    def uninstallFilter(self, filter_id):
        return self.web3.manager.request_blocking(
            "eth_uninstallFilter", [filter_id],
        )

    def contract(self,
                 address=None,
                 **kwargs):
        ContractFactoryClass = kwargs.pop('ContractFactoryClass', self.defaultContractFactory)

        ContractFactory = ContractFactoryClass.factory(self.web3, **kwargs)

        if address:
            return ContractFactory(address)
        else:
            return ContractFactory

    def setContractFactory(self, contractFactory):
        self.defaultContractFactory = contractFactory

    def getCompilers(self):
        return self.web3.manager.request_blocking("eth_getCompilers", [])

    def generateGasPrice(self, transaction_params=None):
        if self.gasPriceStrategy:
            return self.gasPriceStrategy(self.web3, transaction_params)

    def setGasPriceStrategy(self, gas_price_strategy):
        self.gasPriceStrategy = gas_price_strategy

    @property
    def getCurrentSpan(self):
        return self.web3.manager.request_blocking(
            "eth_getCurrentSpan",
            [],
        )

    def getBlockReward(self, block_identifier=0):
        block_identifier = self.web3.toHex(block_identifier)
        return self.web3.manager.request_blocking(
            "eth_getBlockReward",
            [block_identifier],
        )
