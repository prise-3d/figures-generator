import os
import argparse

import numpy as np
from PIL import Image
from rawls.rawls import Rawls

import json
import glob
import shutil

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

    parser.add_argument('--folder', type=str, help='folder path with all estimator data', required=True)
    parser.add_argument('--json', type=str, help='Expected current configuration', required=True)

    args = parser.parse_args()

    p_folder  = args.folder
    p_json = args.json

    json_data = None

    with open(p_json, 'r') as json_file:
        json_data = json.load(json_file)

    nsamples = int(json_data['nsamples'])
    reference = json_data['reference']
    output = os.path.join(json_data['output'], json_data['nsamples'], 'png')

    if not os.path.exists(output):
        os.makedirs(output)

    estimators_path = [ p for p in glob.glob(f'{p_folder}/**/**/*.png') if extract_nsamples(p) == nsamples ]

    reference_path = glob.glob(f'{p_folder}/{reference}/**/*.png')

    # construct output estimator
    estimators_full_path = list(set(estimators_path) | set(reference_path)) 
    
    for img_path in sorted(estimators_full_path):

        output_image_path = img_path.replace(p_folder, output)
        output_image_folder, _ = os.path.split(output_image_path)

        if not os.path.exists(output_image_folder):
            os.makedirs(output_image_folder)

        if not os.path.exists(output_image_path):
            print(f'Copy `{img_path}` image into {output}')
            shutil.copy2(img_path, output_image_path)
    

if __name__ == "__main__":
    main()