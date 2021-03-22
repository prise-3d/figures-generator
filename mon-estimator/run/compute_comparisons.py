import os, sys
import argparse

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse

def write_progress(progress):
    '''
    Display progress information as progress bar
    '''
    barWidth = 180

    output_str = "["
    pos = barWidth * progress
    for i in range(barWidth):
        if i < pos:
           output_str = output_str + "="
        elif i == pos:
           output_str = output_str + ">"
        else:
            output_str = output_str + " "

    output_str = output_str + "] " + str(int(progress * 100.0)) + " %\r"
    print(output_str)
    sys.stdout.write("\033[F")


def rmse(image, ref):
    return np.sqrt(((image - ref) ** 2).mean())

def compare_image(metric, ref, image):

    error = None
    if metric == 'ssim':
        error = ssim(image, ref, multichannel=True)

    if metric == 'mse':
        error = mse(image, ref)

    if metric == 'rmse':
        error = rmse(image, ref)

    return error

def main():
    
    parser = argparse.ArgumentParser(description="Compare all estimators to reference image for few scenes")

    parser.add_argument('--estimators', type=str, help="folder with all estimators", required=True)
    parser.add_argument('--reference', type=str, help="reference folder with scenes", required=True)
    parser.add_argument('--metric', type=str, help="metric choice to use", choices=['ssim', 'rmse'], required=True)
    parser.add_argument('--output', type=str, help="output data file", required=True)

    args = parser.parse_args()

    estimators = args.estimators
    reference = args.reference
    metric = args.metric
    output = args.output

    output_path, _ = os.path.split(output)

    if len(output_path) > 0 and not os.path.exists(output_path):
        os.makedirs(output_path)

    f = open(output, 'w')

    print('Load of reference images')
    reference_images = {}
    for ref_scene in sorted(os.listdir(reference)):
        ref_scene_path = os.path.join(reference, ref_scene)
        image_name = os.listdir(ref_scene_path)[0]

        image_path = os.path.join(ref_scene_path, image_name)
        reference_images[ref_scene] = np.array(Image.open(image_path))

    print('For each estimator start to compare each scene')
    for est in sorted(os.listdir(estimators)):
        
        est_path = os.path.join(estimators, est)
        for scene in sorted(os.listdir(est_path)):


            print(f'Comparisons of {est} to reference on {scene} scene')
            data_line = f'{est};{scene}'

            scene_path = os.path.join(est_path, scene)

            # get all image names
            scene_images = sorted(os.listdir(scene_path))
            nimages = len(scene_images)

            counter = 0

            if scene not in reference_images:
                print(f'{scene} data not available for reference')

            for img in sorted(scene_images):

                # open image data
                img_path = os.path.join(scene_path, img)
                img_data = np.array(Image.open(img_path))

                # compare image
                current_error = compare_image(metric, img_data, reference_images[scene])

                # save data into line
                data_line += f';{current_error}'

                # display information
                counter += 1
                write_progress((counter + 1) / nimages)

            f.write(data_line + '\n')

    f.close()

if __name__ == "__main__":
    main()
