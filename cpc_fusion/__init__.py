import pkg_resources
import sys
import warnings


if (3, 5) <= sys.version_info < (3, 6):
    warnings.warn(
        "Support for Python 3.5 will be removed in web3.py v5",
        category=DeprecationWarning,
        stacklevel=2)

if sys.version_info < (3, 5):
    raise EnvironmentError(
        "Python 3.5 or above is required. "
        "Note that support for Python 3.5 will be remove in web3.py v5")

from eth_account import Account  # noqa: E402
from cpc_fusion.main import Web3  # noqa: E402
from cpc_fusion.providers.rpc import (  # noqa: E402
    HTTPProvider,
)
from cpc_fusion.providers.eth_tester import (  # noqa: E402
    EthereumTesterProvider,
)
from cpc_fusion.providers.tester import (  # noqa: E402
    TestRPCProvider,
)
from cpc_fusion.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from cpc_fusion.providers.websocket import (  # noqa: E402
    WebsocketProvider,
)

__version__ = pkg_resources.get_distribution("cpc_fusion").version

__all__ = [
    "__version__",
    "Web3",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    "TestRPCProvider",
    "EthereumTesterProvider",
    "Account",
]
