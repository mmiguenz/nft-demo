from brownie import network
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time


def test_can_create_advanced_collectible_integration():
    # deploy contract
    # create an nft
    # get a random breed back
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for integration test")

    advanced_collectible, _ = deploy_and_create()
    time.sleep(300)
    assert advanced_collectible.tokenCounter() == 1
