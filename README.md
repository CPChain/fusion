# Fusion API

![cpc-fusion](https://github.com/CPChain/fusion/raw/master/fusion.png)

![python3](https://img.shields.io/badge/language-python3-orange.svg)[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)[![Pull Requests](https://img.shields.io/bitbucket/pr-raw/cpchain/chain.svg)](https://bitbucket.org/cpchain/chain/pull-requests/)[![Follow Twitter](https://img.shields.io/twitter/follow/cpchain_io.svg?label=Follow&style=social)](https://twitter.com/intent/follow?screen_name=cpchain_io)

A Python package based on  [web3.py](https://github.com/ethereum/web3.py) to interact with cpchain.

- Python 3.5+ support

## Installation

cpc_fusion.py can be installed (preferably in a virtualenv) using `pip` as follows:

```bash

pip install cpc-fusion

```

Installation from source can be done from the root of the project with the following command.

```bash

pip install .

```

## Using Fusion

To use the web3 library you will need to initialize the `Web3` class.

Use the `auto` module to guess at common node connection options.

```python
from cpc_fusion import Web3
cf = Web3(Web3.HTTPProvider('http://127.0.0.1:8501'))
cf.cpc.blockNumber
>>> 34341
```

Note

If you get the result `UnhandledRequest: No providers responded to the RPC request` then you are not connected to a node.

Read more in the [documentation on CPChain](http://docs.cpchain.io/).
