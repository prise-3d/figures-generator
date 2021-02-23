import os, sys
import argparse

import numpy as np

# images processing imports
from PIL import Image
from ipfml.processing import transform

folder_output = 'data/border'

def get_color(color):

    if color == 'red':
        return np.array([255, 0, 0])
    
    if color == 'green':
        return np.array([0, 255, 0])

    if color == 'blue':
        return np.array([0, 0, 255])

def main():
    
    parser = argparse.ArgumentParser(description="Add border to image using p1 and p2 coordinate")

    parser.add_argument('--p1', type=str, help='x coordinate', default='200,800', required=True)
    parser.add_argument('--p2', type=str, help='y coordinare', default='200,800', required=True)
    parser.add_argument('--img', type=str, help='image where to insert border', required=True)
    parser.add_argument('--color', type=str, choices=['red', 'green', 'blue'], default='red')
    parser.add_argument('--output', type=str, required=True)

    args = parser.parse_args()

    p1_x, p1_y = list(map(int, args.p1.split(',')))
    p2_x, p2_y = list(map(int, args.p2.split(',')))
    p_img    = args.img
    p_color  = args.color
    p_output = args.output

    # open image
    img_arr = np.array(Image.open(p_img))

    for i in range(3):

        for x in np.arange(p1_x + i, p2_x + 1 + i):

            img_arr[p1_y + i][x] = get_color(p_color)
            img_arr[p2_y + i][x] = get_color(p_color)

        for y in np.arange(p1_y + i, p2_y + 1 + i):

            img_arr[y][p1_x + i] = get_color(p_color)
            img_arr[y][p2_x + i] = get_color(p_color)

    # save new image
    pil_img = Image.fromarray(img_arr)

    if not os.path.exists(folder_output):
        os.makedirs(folder_output)

    p_output_folder, _ = os.path.split(os.path.join(folder_output, p_output))
        
    if not os.path.exists(p_output_folder):
        os.makedirs(p_output_folder)

    pil_img.save(os.path.join(folder_output, p_output))
    

if __name__ == "__main__":
    main()