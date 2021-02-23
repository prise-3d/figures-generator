import os, sys
import argparse

import numpy as np

# images processing imports
from PIL import Image
from ipfml.processing import transform

def main():
    
    parser = argparse.ArgumentParser(description=" image using p1 and p2 coordinate")

    parser.add_argument('--p1', type=str, help='x coordinate', default='200,800', required=True)
    parser.add_argument('--p2', type=str, help='y coordinare', default='200,800', required=True)
    parser.add_argument('--img', type=str, help='image where to insert border', required=True)
    parser.add_argument('--output', type=str, required=True)

    args = parser.parse_args()

    p1_x, p1_y = list(map(int, args.p1.split(',')))
    p2_x, p2_y = list(map(int, args.p2.split(',')))
    p_img    = args.img
    p_output = args.output

    # open image
    pil_img = Image.open(p_img)
    
    pil_img = pil_img.crop((p1_x, p1_y, p2_x, p2_y))


    p_output_folder, _ = os.path.split(p_output)
        
    if not os.path.exists(p_output_folder):
        os.makedirs(p_output_folder)

    pil_img.save(p_output)
    

if __name__ == "__main__":
    main()