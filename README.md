Randomness is everywhere, structure is rare. 

Images are combinations of randomly generated .pngs with different pixel definitions. 
The lowest the "Combined Randomness" & the "Pixel Sum" the rarest. 

Each NoisyFrame has been generated like so:


# create
run make_collection.py

# set-up
start ipfs daemon instance
create infura project

# pin images locally
python3 utils/add_to_ipfs.py -d images/ 


# pin metadata locally as a folder
python3 add_uri_to_metadata.py
python3 utils/add_to_ipfs.py -d metadata/ -dir_only True

# pin imgs to infura 
run utils/pin_to_infura.py
# pin metadata infura (change path in between pins or add metadata & imgs CIDs in same .txt)
run utils/pin_to_infura.py

# upload contract (I used remix for this)



To do:
    - remove info from pin_to_infura
    - push
    - mainnet
    - froooooooontside bbay


