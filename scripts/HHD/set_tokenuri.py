from brownie import HypeDiscoNFT, network
from scripts.helpfulscripts import get_status

hyena_metadata_dic


def main():
    print("Working on " + network.show_active())
    hypedisco_nft = HypeDiscoNFT[len(HypeDiscoNFT) - 1]
    number_of_hyenas = hypedisco_nft.tokenCounter()
    print("The Number of Hyenas At The Disco is: "
        + str(number_of_hyenas)
        )
    for token_id in range(number_of_hyenas):
        status = get_status(hypedisco_nft.tokenIdToHyena(token_id))
        if not hypedisco_nft.tokenURI(tokenId).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, hypedisco_nft, ????)
