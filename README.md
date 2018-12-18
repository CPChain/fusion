# Fusion API

[![Join the chat at https://gitter.im/ethereum/web3.py](https://badges.gitter.im/ethereum/web3.py.svg)](https://gitter.im/ethereum/web3.py?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build Status](https://circleci.com/gh/ethereum/web3.py.svg?style=shield)](https://circleci.com/gh/ethereum/web3.py.svg?style=shield)

A Python package based on  [web3.py](https://github.com/ethereum/web3.py) to interact with cpchain.

- Python 3.5+ support


## Installation

cpc_fusion.py can be installed (preferably in a virtualenv) using `pip` as follows:

```
$ pip install cpc-fusion
```

Installation from source can be done from the root of the project with the following command.

```
$ pip install .
```

## Using Fusion

To use the web3 library you will need to initialize the `Web3` class.

Use the `auto` module to guess at common node connection options.

```
>>> from cpc_fusion import Web3
>>> cf = Web3(Web3.HTTPProvider('http://127.0.0.1:8501'))
>>> cf.cpc.blockNumber
34341
```

Note

If you get the result `UnhandledRequest: No providers responded to the RPC request` then you are not connected to a node.


Read more in the [documentation on CPChain](http://docs.cpchain.io/).