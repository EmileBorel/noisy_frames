Randomness is everywhere, structure is rare. 


## Images attributes description
NoisyFrames are composed of 3 individual frames stacked together
Each of the 3333 NoisyFrame were generated as the result of randomn process. 

The lowest the "Combined Randomness" & the "Pixel Sum" the rarest. 
- Combined Randomness = Sum of the humbers sampled from a uniform distribution to set the degree of freedom for each frame's colors.
- Pixel Sum = The sum of the pixels count of the original 3 frames. 


## Attributes generation
- Each of the 3 frame could be of one of the 3 following dimensions: 3x3 with prob= 5.3/100, 3²x3² with prob= 11.3/100, 3⁴x3⁴ with prob = 83.3/100. => see make_collection.set_frame_size()

For each frame, the pixel colors were randomly chosen with a randomly picked degree of freedom.

- 0 degree of freedom with prob 1/10: Fix all of the 3 rgb channels for all pixels (the frame is made of one single color)
- 1 degree of freedom with prob 2/10: Fix 2 of the rgbs for all pixels
- 2 degrees of freedom: With prob 3/10: Fix 1 of the rgbs for all pixels
- 3 degrees of freedom: With prob 4/10: Let all free => make_collection.apply_freedom()


Each of the 3 frames is then scaled to a the destination format to make the final image:

- Final frames sizes are given by: [int(base⁶ * (i / base)) for i in [3, 2, 2/3]] 
- With base 3, the final NoisyFrames are therefore 729x729 with two inner 486x486 and 162x162. 

## Images storage
Images & Metadata are stored on IPFS - I experimented with Infura & Pinata and chose the later as I noticed better performances (better propagation maybe ?)
You can find .py that show how to pin files to these services from CLI. 

## Contracts
The solidity contracts were compiled & deployed on Polygon Mainnet using hardhat and Alchemy's service. 
