from brownie import HypeDiscoNFT, accounts, network, config
from scripts.helpfulscripts import fund_hypedisconft 

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(network.show_active())
    publish_source = False
    hypedisco_nft = HypeDiscoNFT.deploy(
       config['networks'][network.show_active()]['vrf_coordinator'],
       config['networks'][network.show_active()]['link_token'],
       config['networks'][network.show_active()]['keyhash'],
       {"from": dev},
       publish_source=publish_source
    )
    fund_hypedisconft(hypedisco_nft)
    return hypedisco_nft
