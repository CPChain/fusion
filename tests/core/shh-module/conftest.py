import pytest

from cpc_fusion.shh import (
    Shh,
)


@pytest.fixture(autouse=True)
def include_shh_module(web3):
    Shh.attach(web3, "shh")
