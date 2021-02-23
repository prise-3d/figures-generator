import os
import argparse

import numpy as np
from PIL import Image
from rawls.rawls import Rawls

import glob

# TODO:check if required to update the extract_nsamples for rawls
def extract_nsamples(img_path):

    image_extension = img_path.split('.')[-1]

    if image_extension == 'png':
        return int(img_path.split('-S')[-1].split('-')[0])

    if image_extension == 'rawls':
        return None

    return None


def read_image(img_path):

    image_extension = img_path.split('.')[-1]

    if image_extension == 'png':
        return np.array(Image.open(img_path))

    if image_extension == 'rawls':
        return Rawls.load(img_path).data

    return None

def main():

    parser = argparse.ArgumentParser(description="Convert to expected png format")

    parser.add_argument('--folder', type=str, help='folder path with all clusters data', required=True)
    parser.add_argument('--output', type=str, help='output prediction file', required=True)

    args = parser.parse_args()

    p_folder  = args.folder
    p_output  = args.output

    if not os.path.exists(p_output):
        os.makedirs(p_output)

    rawls_images = glob.glob(f'{p_folder}/**/**/*.rawls')
    
    for img_path in rawls_images:

        output_image_path = img_path.replace(p_folder, p_output).replace('.rawls', '.png')
        output_image_folder, image_name = os.path.split(output_image_path)

        if not os.path.exists(output_image_folder):
            os.makedirs(output_image_folder)

        if not os.path.exists(output_image_path):
            print(f'Convert .rawls image into `{image_name}`')
            Rawls.load(img_path).save(output_image_path)
    

if __name__ == "__main__":
    main()