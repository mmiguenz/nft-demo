from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metada import metadata_template
from pathlib import Path
import requests
import json
import os

breed_to_image_uri = {
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png"
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_colletibles = advanced_collectible.tokenCounter()
    print(f"you have created {number_of_advanced_colletibles} collectibles")

    for token_id in range(number_of_advanced_colletibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        print(metadata_file_name)

        collectible_metadata = metadata_template

        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating metadata file: {metadata_file_name} ")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed}"

            fileName = breed.lower().replace("_", "-")
            image_path = f"./img/{fileName}.png"
            image_uri = None
            if os.getenv("UPLOAD_IPF") == "true":
                image_uri = upload_to_ipfs(image_path)

            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            collectible_metadata["image"] = image_uri
            with (open(metadata_file_name, "w")) as file:
                json.dump(collectible_metadata, file)


# curl -X POST -F file=@myfile "http://127.0.0.1:5001/api/v0/add?quiet=<value>&quieter=<value>&silent=<value>&progress=<value>&trickle=<value>&only-hash=<value>&wrap-with-directory=<value>&chunker=size-262144&pin=true&raw-leaves=<value>&nocopy=<value>&fscache=<value>&cid-version=<value>&hash=sha2-256&inline=<value>&inline-limit=32"


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # ./img/PUB.png -> "PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
