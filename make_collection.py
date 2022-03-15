"""
    Full code to generate the noisy_frames
"""

import os
import json
import pickle
import random

import numpy as np
import matplotlib.pyplot as plt


#######--------------------------collection info--------------------##########

MAX_NB_IMAGES = 3333
NB_FRAME_PER_IMG = 3


#######--------------------------img specifics (default) -------------------##########
## smallest frame is a basexbase
base = 3

# frames are matrices, 
# there are 3 different matrice size, each (i,j) component is a pixel
# each type is a power of base
matrices_sizes = [base**i for i in [4, 2, 1]]

## final_size = is the size of the assembled image
final_size = base**6

# once frame are generated
# every final image is composed of 3 frames of different size
frames_final_size = [int(final_size * (i / base)) for i in [3, 2, 2/3]] 

def set_frame_size():
    """
        Smallest definition frames are the rarest
        With base 3 & current parameters sizes are: [81, 9, 3]

        Choose size X with prob X/100
        Choose one of the 3 with prob 7/100
    """
    sorted_types = sorted(int(x) for x in matrices_sizes)
    randomness = np.random.randint(100)
    
    if randomness >= max(sorted_types):
        sampled_type = random.choice(sorted_types)
    else:                
        for frame_type in sorted_types:
            if frame_type > randomness:
                sampled_type = frame_type
                break
    return sampled_type

        
def set_pixel_values(idx, mat_size):
    """
        O deg freedom: With prob 1/10 fix the 3 rgbs for all pixels
        1 deg freedom: With prob 2/10 fix 2 of the rgbs for all pixels
        2 deg freedom: With prob 3/10 fix 1 of the rgbs for all pixels
        3 deg freedom: With prob 4/10 let all free
        
    """
    def apply_freedom(colors, randomness):
        if randomness < 1:
            rgbs = np.random.choice(range(256), size= 3)
            return [rgbs for _ in range(mat_size*mat_size)]
        
        else:
            if randomness < 2:
                rgbs = np.random.choice(range(256), size= 2)
                rgbs_dims = np.random.choice(range(3), size = 2)
            
            else:
                rgbs = [np.random.choice(range(256))]
                rgbs_dims = [np.random.choice(range(3))]

            for color_idx, full_rgb in enumerate(colors):
                for dim_idx, dim in enumerate(rgbs_dims):
                    full_rgb[dim] = rgbs[dim_idx]
                colors[color_idx] = full_rgb

            return colors
        
    # initially set all pixels as random
    colors =  [np.random.choice(range(256), size=3) for _ in range(mat_size*mat_size)]
    randomness = np.random.choice(range(10))

    
    rgbs = np.random.choice(range(256), size= 3)
    
    if randomness < 5:
        colors = apply_freedom(colors, randomness)
    
    mat = np.array(colors).reshape((mat_size,mat_size,3))
    
    return mat, randomness
    

def stack_frames(frames):
    """
        Map each frame to destination size. 
        1st frame is base ect...
        Then stack them. 
    """
    def scale_frame(frame, destination_size):
        current_size = frame.shape[0]
        ratio = int(destination_size / current_size)
        scaled_mat = np.zeros(shape = (current_size*ratio, current_size*ratio, 3))
        
        for i in range(current_size):
            for j in range(current_size):
                pixel = frame[i,j]
                colors = [pixel for _ in range(ratio**2)]
                pixel_mat = np.array(colors).reshape((ratio, ratio,3))
                
                row_start = i * ratio
                col_start = j * ratio
                scaled_mat[row_start: row_start + ratio, col_start: col_start + ratio] = pixel_mat
        
        return scaled_mat.astype("uint8")
                
    scaled_frames = []  
    for frame, destination_size in zip(frames, frames_final_size):
        scaled_frame = scale_frame(frame, destination_size)
        scaled_frames.append(scaled_frame)
        
    
    final_img = scaled_frames[0]
    for mat in scaled_frames[1:]:
        size = mat.shape[0]
        
        # center frame
        idx_start = int((final_img.shape[0] - size) / 2)
        idx_end = int(final_img.shape[0] - ((final_img.shape[0] - size) / 2))
        final_img[idx_start: idx_end, idx_start: idx_end] = mat
        
    return final_img
    


def main():
    i= 0
    
    while i < MAX_NB_IMAGES:
        i+= 1
        
        metadata = {"attributes": []}
        combined_randomness = 0
        pixel_sum = 0
        frames = []
        for frame in range(NB_FRAME_PER_IMG):
            mat_size = set_frame_size()
            mat, randomness = set_pixel_values(i, mat_size)
            
            frames.append(mat)
            
            # add frame info to metadata
            r, g, b = (int(val) for val in mat.mean(axis= (0,1)))
            mean_hex_code = "#{:02x}{:02x}{:02x}".format(r,g,b)
            metadata["attributes"].append({"trait_type": f"frame_{frame+1}_mean_hex", 
                                           "value": mean_hex_code })   
            combined_randomness += randomness
            pixel_sum += mat_size**2
        
        
        metadata["attributes"].append({"trait_type": f"color_freedom", 
                                       "value": str(combined_randomness) })
        metadata["attributes"].append({"trait_type": f"pixel_sum", 
                                       "value": str(pixel_sum) })
        
        # make final image
        final_image = stack_frames(frames)
        
        metadata["name"] = f"NoisyFrame #{i}"

        
        # plt.imshow(final_image)
        # plt.show()
        # print(metadata)
            
        plt.imsave(f'images/{i}.png', final_image)

        with open(f'metadata/{i}.json', "w") as file:
            json.dump(metadata, file)

        if int(i) % 33 == 0:
            print(f"{i}/{MAX_NB_IMAGES}") 


if __name__ == "__main__":
    main()