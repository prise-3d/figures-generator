import os
import json
import argparse

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as rmse

def main():
    
    parser = argparse.ArgumentParser(description="Compare multiple image using metric on different estimators")

    parser.add_argument('--json', type=str, help="json with all build figure data", required=True)

    args = parser.parse_args()

    p_json = args.json

    # extract data from json configuration
    json_data = None

    with open(p_json, 'r') as json_file:
        json_data = json.load(json_file)

    reference = json_data["reference"]
    estimators = json_data["estimators"]
    metric = json_data["metric"]

    p_folder = os.path.join(json_data['output'], json_data['nsamples'], 'processing')
    p_output = os.path.join(json_data['output'], json_data['nsamples'], 'metrics')

    print(f"Comparisons of {reference} with {estimators}")

    if not os.path.exists(p_output):
        os.makedirs(p_output)

    counter = 0
    
    for method in ["border", "crop"]:

        default_estimator_path = os.path.join(p_folder, method, reference)

        # expected images path have same name
        images = os.listdir(default_estimator_path)

        for est in estimators:

            # prepare output filename
            counter_str = str(counter)

            while len(counter_str) < 3:
                counter_str = "0" + counter_str
                
            output_filename = os.path.join(p_output, f"{counter_str}_{method}_{reference}_{est}_{metric}.csv")
            output_file = open(output_filename, 'w')

            for img in sorted(images):

                est1_path_image = os.path.join(p_folder, method, reference, img)
                est2_path_image = os.path.join(p_folder, method, est, img)

                img_rgb_1 = np.array(Image.open(est1_path_image))
                img_rgb_2 = np.array(Image.open(est2_path_image))

                scene_name = img.replace('.png', '')

                if metric == 'ssim':
                    sentence = "{0};{1};{2};{3}\n".format(scene_name, img, estimators, ssim(img_rgb_1, img_rgb_2, multichannel=True))
                    output_file.write(sentence)

                if metric == 'rmse':
                    sentence = "{0};{1};{2};{3}\n".format(scene_name, img, estimators, rmse(img_rgb_1, img_rgb_2))
                    output_file.write(sentence)

            counter += 1
                    
        output_file.close()
            


if __name__ == "__main__":
    main()