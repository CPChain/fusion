"""

pytest

e.g.

pytest -v -s tests/test_contracts.py

"""

import pytest
from cpc_fusion import Web3

from cpc_fusion.default_contracts import RNode

@pytest.fixture()
def cf():
    return Web3(Web3.HTTPProvider('https://civilian.cpchain.io'))

def test_blocknumber(cf):
    print(cf.cpc.blockNumber)


def test_rnode(cf):
    rnode = RNode(cf)
    assert rnode.period > 0
    assert rnode.rnodes_num > 0
    assert len(rnode.rnodes) > 0
    assert (rnode.threshold / 1e18) + 1 > 200000
    print(rnode.supported_version)
