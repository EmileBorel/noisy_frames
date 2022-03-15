"""
    Pin to local instance.
    Save URIS in dict
    Save URIS in .txt for later pin to infura
"""

import pickle
import argparse
import ipfshttpclient



if __name__ == "__main__":

    # get args
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--InputDir", help = "Input Directory")
    parser.add_argument("-dir_only", "--DirOnly", help = "For metadata",
        default= False)

    args = parser.parse_args()
    input_dir = args.InputDir

    # add to ipfs
    client = ipfshttpclient.connect()  # Connects to: /dns/localhost/tcp/5001/http
    response = client.add(input_dir, recursive=True)

    if not args.DirOnly:
        uris = {}
        for rep in response:
            if "png" in rep["Name"]:
                idx = rep["Name"].split("/")[-1].split(".")[0]
                uris[idx] = rep["Hash"]

        # for .py use
        pickle.dump(uris, open("uris/images_uris_dict.pickle", mode= "wb"))

        # for infura pin
        with open(f"uris/local_uris_to_pin.txt", mode= "a+") as f:
            for cid in uris.values():
                f.write(cid + "\n")


    
    else:
        uris = {}
        for rep in response:
            if not "png" in rep["Name"]:
                hash = rep["Hash"]
                
                # for accessibility & infura use
                with open("uris/metadata_uri.txt", mode= "w") as f:
                    f.write(hash)

                # # for infura pin
                # with open("uris/local_uris_to_pin.txt", mode= "a+") as f:
                #     for cid in uris.values():
                #         f.write(cid + "\n")



