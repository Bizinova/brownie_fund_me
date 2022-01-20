from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract

    # if we are on persistent network like rinkeby, use associated address
    # otherwise, deploy mocks function
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # Based on config, publish_source set to True if network, publishes code Etherscan
    # If development then set to false
    # could've used just ["verify"], the .get is used in case you forget to state it in config
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # print(f "...") allows you to add a parameter/variable into print statement
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
