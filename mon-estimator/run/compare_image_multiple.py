import os
import json
import argparse

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as rmse

# {
#     "estimators": [
#         "MON",
#         "reference"
#     ]
# }

def main():
    
    parser = argparse.ArgumentParser(description="Compare multiple image")

    parser.add_argument('--folder', type=str, help="data folder where images are save for each estimators", required=True)
    parser.add_argument('--estimators', type=str, help="specific figure settings", required=True)
    parser.add_argument('--method', type=str, help="specific comparison method to use", choices=['ssim', 'rmse'], required=True)
    parser.add_argument('--output', type=str, required=True)

    args = parser.parse_args()

    p_folder  = args.folder
    p_method = args.method
    p_estimators = args.estimators
    p_output = args.output


    estimators = [ e.strip() for e in p_estimators.split(',') ]
    print(estimators)

    # scenes = os.listdir(p_folder)

    output_file = open(p_output, 'w')

    output_folder, _ = os.path.split(p_output)
    if len(output_folder) > 0 and not os.path.exists(output_folder):
        os.makedirs(output_folder)

    default_estimator_path = os.path.join(p_folder, estimators[0])

    # expected images path have same name
    images = os.listdir(default_estimator_path)

    for img in sorted(images):

        est1_path_image = os.path.join(p_folder, estimators[0], img)
        est2_path_image = os.path.join(p_folder, estimators[1], img)

        img_rgb_1 = np.array(Image.open(est1_path_image))
        img_rgb_2 = np.array(Image.open(est2_path_image))

        scene_name = img.replace('.png', '')

        if p_method == 'ssim':
            sentence = "{0};{1};{2};{3}\n".format(scene_name, img, estimators, ssim(img_rgb_1, img_rgb_2, multichannel=True))
            output_file.write(sentence)

        if p_method == 'rmse':
            sentence = "{0};{1};{2};{3}\n".format(scene_name, img, estimators, rmse(img_rgb_1, img_rgb_2))
            output_file.write(sentence)
                
    
    output_file.close()
            




if __name__ == "__main__":
    main()