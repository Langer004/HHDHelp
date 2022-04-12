from brownie import HypeDiscoNFT, accounts, config, network
from scripts.helpfulscripts import get_status, listen_for_event 
import time
import os
import requests
import json


def main():
    print("Working on " + network.show_active())
    dev = accounts.add(config['wallets']['from_key'])
    hypedisco_nft = HypeDiscoNFT[len(HypeDiscoNFT) - 1]
    transaction = hypedisco_nft.createHyena("None", {"from": dev})
    print("Waiting for Trasnsaction...")
    transaction.wait(1)
    listen_for_event(
        hypedisco_nft, "ReturnedHyena", timeout=200, poll_interval=10
    )
    requestId = transaction.events['requestedHyena']['requestId']
    token_id = hypedisco_nft.requestIdToTokenId(requestId)
    status = get_status(hypedisco_nft.tokenIdToHyena(token_id))
    print ('Status of tokenId {} is {}'.format(token_id, status))

