"""
    After pinning imgs locally/ to infura.
    And before pinning metadata.
    Add their uris to their metadata.
"""

import json
import pickle
import hashlib


def main():
    imgURIs = pickle.load(open("uris/images_uris_dict.pickle", mode="rb"))

    for im_idx in imgURIs.keys():

        im_uri = imgURIs[im_idx]
        im_path = f"images/{im_idx}.png"
        meta_path = f"metadata/{im_idx}.json"

        with open(im_path,"rb") as f:
            bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest()

        with open(meta_path, "r") as file:
            metadata = json.load(file)
            metadata["dna"] = readable_hash
            metadata["image"] = "ipfs://" + im_uri

        with open(meta_path, "w") as file:
            json.dump(metadata, file)


if __name__ == "__main__":
    main()