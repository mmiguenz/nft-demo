from scripts.helpful_scripts import (
    fund_with_link,
    get_account,
    OPEN_SEA_URL,
    get_contract,
)
from brownie import AdvancedCollectible, config, network
import time


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyHash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    token_counter = advanced_collectible.tokenCounter({"from": account})
    print(f"new token has been created. Tokens {token_counter}")
    return advanced_collectible, creating_tx


def main():
    deploy_and_create()
