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

    return None

def main():

    parser = argparse.ArgumentParser(description="Convert to expected png format")

    parser.add_argument('--folder', type=str, help='folder path with all estimator data', required=True)
    parser.add_argument('--nsamples', type=str, help='number of samples', required=True)
    parser.add_argument('--output', type=str, help='output prediction file', required=True)

    args = parser.parse_args()

    p_folder  = args.folder
    p_nsamples = args.nsamples
    p_output  = args.output

    if not os.path.exists(p_output):
        os.makedirs(p_output)
    
    for estimator in sorted(os.listdir(p_folder)):

        estimator_path = os.path.join(p_folder, estimator)

        for scene in sorted(os.listdir(estimator_path)):

            scene_path = os.path.join(estimator_path, scene)

            output_scene_path = os.path.join(p_folder, estimator_path, scene)

            if not os.path.exists(output_scene_path):
                os.makedirs(output_scene_path)

            for i, img in enumerate(sorted(os.listdir(scene_path))):

                index_str = str(i)

                while len(index_str) < 7:
                    index_str = "0" + index_str

                img_prefix = img.split('-')[0]
                outfilename = f'{img_prefix}-S{p_nsamples}-{index_str}.png'
                
                img_path = os.path.join(scene_path, img)
                outfile_path = os.path.join(output_scene_path, outfilename)

                print(f'Copy of {img_path}')
                os.system(f'cp {img_path} {outfile_path}')
        

if __name__ == "__main__":
    main()