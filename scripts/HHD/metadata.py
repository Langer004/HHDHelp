from email.mime import image
from importlib.metadata import metadata
from brownie import HypeDiscoNFT, network
from metadata import sample_metadata
from scripts.helpfulscripts import get_status
from pathlib import Path
import os
import requests
import json

status_to_image_uri = {
    "VIP": "https://ipfs.io/ipfs/QmPxhtGAiWrRAvgu8QjSrAQ3pPb9qbmDtgscwm2m822Qzq?filename=vip.png",
    "GOLD": "https://ipfs.io/ipfs/QmbZwzfdM8mq1MkFdv7xF5arnH3Qfq7TWytJvRy8BNFy9C?filename=gold.png",
    "GENERAL": "https://ipfs.io/ipfs/QmRsp8c2zFXUtgPxBb8fTikH83kReJjVnJpCyxZuawb749?filename=general.png"
}


def main():
    print("Working on " + network.show_active())
    hypedisco_nft = HypeDiscoNFT[len(HypeDiscoNFT) - 1] 
    number_of_tokens = hypedisco_nft.tokenCounter()
    print("The Number of Hyenas at the Disco is {}" .format(number_of_tokens))
    write_metadata(number_of_tokens, hypedisco_nft) 

def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        hypedisco_metadata = sample_metadata.metadata_template
        status = get_status(nft_contract.tokenIdToHyena(token_id)) 
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active()) + str(token_id)
            + "-" + status + ".json" 
        )
        # matadata/rinkeby/6-GENERAL.json
        if Path(metadata_file_name).exists():
            print("{} Already Found!".format(metadata_file_name))
        else: 
            print("Creating Metadata File {}".format(metadata_file_name))
            hypedisco_metadata["name"] = get_status(
                nft_contract.tokenIdToHyena(token_id))
            hypedisco_metadata["description"] = "Your exclusive membership to see all your favorite artists!"
            print(hypedisco_metadata)
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(
                    status.lower())
                image_to_upload = upload_to_ipfs(
                    image_path)
            image_to_upload = status_to_image_uri[status] if not image_to_upload else image_to_upload
            hypedisco_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(hypedisco_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

#  0xa2039831D0ffacBa2739bEd17e9B000a2765CC6F 
# http://127.0.0.1:5001
# curl -X POST -F file=@img/vip.png http://localhost:5001/api/v0/add

def upload_to_ipfs(filepath): 
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(
        ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
        return image_uri
    return None
