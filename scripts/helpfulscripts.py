from brownie import network, accounts, config, interface, web3
import os
import time

from brownie.network import priority_fee

def get_status(hyena_number):
    switch = {0: 'VIP', 1: 'GOLD', 2: 'GENERAL'}
    return switch[hyena_number]

def fund_hypedisconft(nft_contract):
    dev = accounts.add(config['wallets']['from_key'])
    link_token = interface.LinkTokenInterface(
        config['networks'][network.show_active()]['link_token'])
    link_token.transfer(nft_contract, 1000000000000000000, {"from": dev})

def listen_for_event(brownie_contract, event, timeout=200, poll_interval=2):
    
    web3_contract = web3.eth.contract(
        address=brownie_contract.address, abi=brownie_contract.abi
    )
    start_time = time.time()
    current_time = time.time()
    event_filter = web3_contract.events[event].createFilter(fromBlock="latest")
    while current_time - start_time < timeout:
        for event_response in event_filter.get_new_entries():
            if event in event_response.event:
                print("Found event!")
                return event_response
        time.sleep(poll_interval)
        current_time = time.time()
    print("Timeout reached, no event found.")
    return {"event": None}
