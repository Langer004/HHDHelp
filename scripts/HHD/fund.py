from brownie import HypeDiscoNFT
from scripts.helpfulscripts import fund_hypedisconft 

def main():
    hypedisco_nft = HypeDiscoNFT[len(HypeDiscoNFT) - 1]
    fund_hypedisconft(hypedisco_nft)