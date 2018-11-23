from eth_utils import (
    add_0x_prefix,
    apply_to_return_value,
    from_wei,
    is_address,
    is_checksum_address,
    keccak as eth_utils_keccak,
    remove_0x_prefix,
    to_checksum_address,
    to_wei,
)
from hexbytes import (
    HexBytes,
)

from ens import ENS
from cpc_fusion._utils.abi import (
    map_abi_data,
)
from cpc_fusion._utils.decorators import (
    combomethod,
    deprecated_for,
)
from cpc_fusion._utils.empty import (
    empty,
)
from cpc_fusion._utils.encoding import (
    hex_encode_abi_type,
    to_bytes,
    to_hex,
    to_int,
    to_text,
)
from cpc_fusion._utils.normalizers import (
    abi_ens_resolver,
)
from cpc_fusion.admin import (
    Admin,
)
from cpc_fusion.eth import (
    Eth,
)
from cpc_fusion.cpc import (
    Cpc,
)
from cpc_fusion.iban import (
    Iban,
)
from cpc_fusion.manager import (
    RequestManager,
)
from cpc_fusion.miner import (
    Miner,
)
from cpc_fusion.net import (
    Net,
)
from cpc_fusion.parity import (
    Parity,
)
from cpc_fusion.personal import (
    Personal,
)
from cpc_fusion.providers.eth_tester import (
    EthereumTesterProvider,
)
from cpc_fusion.providers.ipc import (
    IPCProvider,
)
from cpc_fusion.providers.rpc import (
    HTTPProvider,
)
from cpc_fusion.providers.tester import (
    TestRPCProvider,
)
from cpc_fusion.providers.websocket import (
    WebsocketProvider,
)
from cpc_fusion.testing import (
    Testing,
)
from cpc_fusion.txpool import (
    TxPool,
)
from cpc_fusion.version import (
    Version,
)


def get_default_modules():
    return {
        "eth": Eth,
        "net": Net,
        "personal": Personal,
        "version": Version,
        "txpool": TxPool,
        "miner": Miner,
        "admin": Admin,
        "parity": Parity,
        "testing": Testing,
        "cpc": Cpc,
    }


class Web3:
    # Providers
    HTTPProvider = HTTPProvider
    IPCProvider = IPCProvider
    TestRPCProvider = TestRPCProvider
    EthereumTesterProvider = EthereumTesterProvider
    WebsocketProvider = WebsocketProvider

    # Managers
    RequestManager = RequestManager

    # Iban
    Iban = Iban

    # Encoding and Decoding
    toBytes = staticmethod(to_bytes)
    toInt = staticmethod(to_int)
    toHex = staticmethod(to_hex)
    toText = staticmethod(to_text)

    # Currency Utility
    toWei = staticmethod(to_wei)
    fromWei = staticmethod(from_wei)

    # Address Utility
    isAddress = staticmethod(is_address)
    isChecksumAddress = staticmethod(is_checksum_address)
    toChecksumAddress = staticmethod(to_checksum_address)

    def __init__(self, providers=empty, middlewares=None, modules=None, ens=empty):
        self.manager = RequestManager(self, providers, middlewares)

        if modules is None:
            modules = get_default_modules()

        for module_name, module_class in modules.items():
            module_class.attach(self, module_name)

        self.ens = ens

    @property
    def middleware_stack(self):
        return self.manager.middleware_stack

    @property
    def providers(self):
        return self.manager.providers

    @providers.setter
    def providers(self, providers):
        self.manager.providers = providers

    @staticmethod
    @deprecated_for("This method has been renamed to keccak")
    @apply_to_return_value(HexBytes)
    def sha3(primitive=None, text=None, hexstr=None):
        return Web3.keccak(primitive, text, hexstr)

    @staticmethod
    @apply_to_return_value(HexBytes)
    def keccak(primitive=None, text=None, hexstr=None):
        if isinstance(primitive, (bytes, int, type(None))):
            input_bytes = to_bytes(primitive, hexstr=hexstr, text=text)
            return eth_utils_keccak(input_bytes)

        raise TypeError(
            "You called keccak with first arg %r and keywords %r. You must call it with one of "
            "these approaches: keccak(text='txt'), keccak(hexstr='0x747874'), "
            "keccak(b'\\x74\\x78\\x74'), or keccak(0x747874)." % (
                primitive,
                {'text': text, 'hexstr': hexstr}
            )
        )

    @combomethod
    def soliditySha3(cls, abi_types, values):
        """
        Executes sha3 (keccak256) exactly as Solidity does.
        Takes list of abi_types as inputs -- `[uint24, int8[], bool]`
        and list of corresponding values  -- `[20, [-1, 5, 0], True]`
        """
        if len(abi_types) != len(values):
            raise ValueError(
                "Length mismatch between provided abi types and values.  Got "
                "{0} types and {1} values.".format(len(abi_types), len(values))
            )

        if isinstance(cls, type):
            w3 = None
        else:
            w3 = cls
        normalized_values = map_abi_data([abi_ens_resolver(w3)], abi_types, values)

        hex_string = add_0x_prefix(''.join(
            remove_0x_prefix(hex_encode_abi_type(abi_type, value))
            for abi_type, value
            in zip(abi_types, normalized_values)
        ))
        return cls.sha3(hexstr=hex_string)

    def isConnected(self):
        for provider in self.providers:
            if provider.isConnected():
                return True
        else:
            return False

    @property
    def ens(self):
        if self._ens is empty:
            return ENS.fromWeb3(self)
        else:
            return self._ens

    @ens.setter
    def ens(self, new_ens):
        self._ens = new_ens
