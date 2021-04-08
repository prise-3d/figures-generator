import os
import argparse
import json
import operator

import numpy as np
from PIL import Image

from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import peak_signal_noise_ratio as psnr

import uuid

def compare_image(metric, ref, target):

    if metric == 'ssim':
        return ssim(ref, target, multichannel=True)

    if metric == 'psnr':
        return psnr(ref, target)

    if metric == 'mse':
        return mse(ref, target)

    return None

def extract_nsamples(img_path):
    _, img = os.path.split(img_path)
    return int(img.split('-')[-2].replace('S', ''))

def get_color(color):

    if color == 'red':
        return np.array([255, 0, 0])
    
    if color == 'green':
        return np.array([0, 255, 0])

    if color == 'blue':
        return np.array([0, 0, 255])
    
    if color == 'yellow':
        return np.array([255, 204, 0])

    if color == 'lightblue':
        return np.array([0, 153, 255])

def add_border(img_arr, p1, p2, color, size):

    img_arr = img_arr.copy()
    p1_x, p1_y = p1
    p2_x, p2_y = p2

    for i in range(size):

        for x in np.arange(p1_x + i, p2_x + 1 + i):

            img_arr[p1_y + i][x] = get_color(color)
            img_arr[p2_y + i][x] = get_color(color)

        for y in np.arange(p1_y + i, p2_y + 1 + i):

            img_arr[y][p1_x + i] = get_color(color)
            img_arr[y][p2_x + i] = get_color(color)

    return img_arr

def extract_zone(img_arr, p1, p2):

    img_arr = img_arr.copy()
    
    p1_x, p1_y = p1
    p2_x, p2_y = p2

    return img_arr[p1_y:p2_y, p1_x:p2_x, :]


def extract_center(img_arr, w, h):

    m_w, m_h = int(w / 2), int(h / 2) # get middle to add
    h_i, w_i, _ = img_arr.shape # get shape
    w_center, h_center = (int(w_i / 2), int(h_i / 2)) # get center coords

    return img_arr[h_center - m_h:h_center + m_h, w_center - m_w:w_center + m_w, :]


def main():
    
    parser = argparse.ArgumentParser(description="Compute image figure as output")

    parser.add_argument('--input', type=str, help="specific expected folder as input", required=True)
    parser.add_argument('--json', type=str, help="specific figure settings", required=True)
    parser.add_argument('--output', type=str, required=True)

    args = parser.parse_args()

    p_input = args.input
    p_json = args.json
    p_output = args.output

    # default output image path
    images_folder = os.path.join(p_output, 'images')

    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    json_data = None

    with open(p_json, 'r') as json_file:
        json_data = json.load(json_file)

    # 0. Extract common json key
    expected_scenes = json_data['scenes'].keys()
    expected_scenes_config = json_data['scenes']
    expected_samples = int(json_data['nsamples'])
    expected_metric = json_data['metric']
    expected_reference = json_data['reference']
    expected_estimators = json_data['estimators']
    expected_figsize = json_data['figsize']
    expected_displays = json_data['displays']
    expected_methods = json_data['methods']

    # Store all scenes data in dictionnary
    comparisons_data = {}

    # store usefull information for each
    for scene in expected_scenes:
        comparisons_data[scene] = {}

    print(f'1. Extracted data from {p_output} using {p_json} configuration...')

    for scene in expected_scenes:

        for est in expected_estimators:
            scene_path = os.path.join(p_input, est, scene)

            if not os.path.exists(scene_path):
                print(f'Stopping process... {scene_path} does not exists...')
                return

            # indicate here what will be store into estimator
            comparisons_data[scene][est] = {
                'real_path': None,
                'img_data': None,
                'cropped_data': None,
                'methods': [] # here we store each method data
            }

            img_path = None
            # extract reference image path
            if est == expected_reference:
                img_path = os.path.join(scene_path, os.listdir(scene_path)[0])
            else:
                img_path = os.path.join(scene_path, [ img for img in os.listdir(scene_path) if extract_nsamples(img) == expected_samples ][0])
            
            comparisons_data[scene][est]['real_path'] = img_path

            img_data = np.array(Image.open(img_path))
            comparisons_data[scene][est]['img_data'] = img_data

            # 1. Crop all desired images from center
            w, h = json_data['scenes'][scene]['resize']

            # get center of image
            cropped_img = extract_center(img_data, w, h)
            comparisons_data[scene][est]['cropped_data'] = cropped_img


    # 2. Generate border and cropped images
    print(f'2. Extraction of expected image and crop part')
    for m_i, method in enumerate(expected_methods):

        for scene in expected_scenes:

            print(f'-- Process method {m_i + 1} of {len(expected_methods)} of scene `{scene}`')
            
            scene_config = expected_scenes_config[scene]

            # get opposite point
            opposite = scene_config['opposite']
            opposite_point = opposite, opposite
            
            for est in expected_estimators:

                current_data = comparisons_data[scene][est]['cropped_data']
                
                method_obj = {}

                # create border image data
                if method == 'border':

                    border_data = current_data.copy()

                    for i, p in enumerate(scene_config['crops']):
                        
                        
                        p1 = list(map(int, p))
                        p2 = list(map(int, tuple(map(operator.add, p, opposite_point))))

                        border_data = add_border(border_data, p1, p2, scene_config['colors'][i], 3)

                    # save border data image
                    output_img = os.path.join(images_folder, str(uuid.uuid4()) + '.png')
                    Image.fromarray(border_data).save(output_img)

                    method_obj = { 
                        'img_data': current_data,
                        'color_data': border_data,
                        'img_path': output_img,
                        'metric': None
                    }

                # create cropped image data with border or not
                if method == 'crop':

                    method_obj = []

                    for i, p in enumerate(scene_config['crops']):
                        
                        crop_data = current_data.copy()

                        p1 = list(map(int, p))
                        p2 = list(map(int, tuple(map(operator.add, p, opposite_point))))

                        crop_data = extract_zone(crop_data, p1, p2)

                        opposite_point_reduced = opposite - 3, opposite - 3
                        color_data = add_border(crop_data, (0, 0), opposite_point_reduced, scene_config['colors'][i], 3)

                        # save color data image
                        output_img = os.path.join(images_folder, str(uuid.uuid4()) + '.png')
                        Image.fromarray(color_data).save(output_img)

                        crop_obj = {
                            'img_data': crop_data,
                            'color_data': color_data,
                            'img_path': output_img,
                            'metric': None
                        }

                        method_obj.append(crop_obj)

                # add method obj inside estimator data
                comparisons_data[scene][est]['methods'].append(method_obj)
                    
    # 3. Compare border and cropped images with metrics
    print(f'3. Comparison of all estimators to {expected_reference} using {expected_metric}')
    
    for scene in expected_scenes:
        
        scene_config = expected_scenes_config[scene]
        
        for e_i, est in enumerate(expected_estimators):
            
            print(f'-- Process esttimator {e_i + 1} of {len(expected_estimators)} of scene `{scene}`')

            methods_ref = comparisons_data[scene][expected_reference]['methods']
            current_data = comparisons_data[scene][est]['cropped_data']
            methods_object = comparisons_data[scene][est]['methods']

            for m_index, method in enumerate(expected_methods):
                
                if method == 'border':
                    metric = compare_image(expected_metric, methods_ref[m_index], methods_object[m_index])
                    methods_object[m_index]['metric'] = metric
                
                if method == 'crop':

                    for i, p in enumerate(scene_config['crops']):
                        current = methods_object[m_index][i]
                        ref = methods_ref[m_index][i]

                        metric = compare_image(expected_metric, ref, current)
                        methods_object[m_index][i]['metric'] = metric


    # 6. Create expected output LaTeX figure using specific images path




if __name__ == "__main__":
    main()