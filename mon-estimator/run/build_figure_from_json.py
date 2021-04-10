import os
import argparse
import json
import operator

import numpy as np
from PIL import Image

import uuid

from utils.fonctions import add_border
from utils.fonctions import compare_image
from utils.fonctions import extract_center
from utils.fonctions import extract_zone
from utils.fonctions import get_color
from utils.fonctions import extract_nsamples

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
    expected_scenes = json_data['availables']
    expected_scenes_config = json_data['scenes']
    expected_samples = int(json_data['nsamples'])
    expected_metric = json_data['metric']
    expected_reference = json_data['reference']
    expected_estimators = json_data['estimators']
    expected_figsize = json_data['figsize']
    expected_displays = json_data['displays']
    expected_methods = json_data['methods']
    expected_right_part_width = json_data['rightpart']['width']
    expected_right_part_size = json_data['rightpart']['size']
    expected_right_part_detect = json_data['rightpart']['detect']

    # Store all scenes data in dictionnary
    comparisons_data = {}
    references_data = {} # need to store img_data and crop of reference here

    # store usefull information for each
    for scene in expected_scenes:
        comparisons_data[scene] = {}

    print(f'1. Extraction of data from `{p_output}` using {p_json} configuration...')

    for scene in expected_scenes:

        for e_i, est in enumerate(expected_estimators):
            scene_path = os.path.join(p_input, est, scene)

            if not os.path.exists(scene_path):
                print(f'Stopping process... {scene_path} does not exists...')
                return

            # indicate here what will be store into estimator
            comparisons_data[scene][e_i] = {
                'real_path': None,
                'img_data': None,
                'cropped_data': None,
                'methods': {} # here we store each method data
            }

            img_path = None
            # extract reference image path
            if est == expected_reference:
                img_path = os.path.join(scene_path, os.listdir(scene_path)[0])
            else:
                img_path = os.path.join(scene_path, [ img for img in os.listdir(scene_path) if extract_nsamples(img) == expected_samples ][0])
            
            comparisons_data[scene][e_i]['real_path'] = img_path

            img_data = np.array(Image.open(img_path))
            comparisons_data[scene][e_i]['img_data'] = img_data

            # 1. Crop all desired images from center
            w, h = json_data['scenes'][scene]['resize']

            # get center of image
            cropped_img = extract_center(img_data, w, h)
            comparisons_data[scene][e_i]['cropped_data'] = cropped_img


    # 2. Generate border and cropped images
    print(f'2. Extraction of expected image and crop part')

    for scene in expected_scenes:

        print(f'-- Process methods for scene `{scene}`')
        
        scene_config = expected_scenes_config[scene]
        border_size = scene_config['border_size']

        # get opposite point
        opposite = scene_config['opposite']
        opposite_point = opposite, opposite
        
        for e_i, est in enumerate(expected_estimators):

            current_data = comparisons_data[scene][e_i]['cropped_data']
            method = expected_methods[e_i]
            
            # create border image data
            if method == 'border':

                border_data = current_data.copy()

                for i, p in enumerate(scene_config['crops']):
                    
                    
                    p1 = list(map(int, p))
                    p2 = list(map(int, tuple(map(operator.add, p, opposite_point))))

                    border_data = add_border(border_data, p1, p2, scene_config['colors'][i], border_size)

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

                method_obj = {}

                for i, p in enumerate(scene_config['crops']):
                    
                    crop_data = current_data.copy()

                    p1 = list(map(int, p))
                    p2 = list(map(int, tuple(map(operator.add, p, opposite_point))))

                    crop_data = extract_zone(crop_data, p1, p2)

                    opposite_point_reduced = opposite - border_size, opposite - border_size
                    color_data = add_border(crop_data, (0, 0), opposite_point_reduced, scene_config['colors'][i], border_size)

                    # save color data image
                    output_img = os.path.join(images_folder, str(uuid.uuid4()) + '.png')
                    Image.fromarray(color_data).save(output_img)

                    crop_obj = {
                        'img_data': crop_data,
                        'color_data': color_data,
                        'img_path': output_img,
                        'metric': None
                    }

                    method_obj[i] = crop_obj

            # build reference data (TODO : improve)
            if expected_reference == est and scene not in references_data:
                references_data[scene] = {}

            if expected_reference == est and method not in references_data[scene]:
                references_data[scene][method] = method_obj

            # add method obj inside estimator data
            comparisons_data[scene][e_i]['method'] = method_obj
                    
    # 3. Compare border and cropped images with metrics
    print(f'3. Comparison of all estimators to {expected_reference} using {expected_metric}')
    
    for scene in expected_scenes:
        
        scene_config = expected_scenes_config[scene]
        print(f'-- Process comparisons for scene `{scene}`')
        
        for e_i, est in enumerate(expected_estimators):
            
            method = expected_methods[e_i]

            method_ref =  references_data[scene][method]
            method_object = comparisons_data[scene][e_i]['method']

            if method == 'border':
                
                metric = compare_image(expected_metric, method_ref['img_data'], method_object['img_data'])
                method_object['metric'] = metric
            
            if method == 'crop':

                for i, p in enumerate(scene_config['crops']):
                    current = method_object[i]['img_data']
                    ref = method_ref[i]['img_data']

                    metric = compare_image(expected_metric, ref, current)
                    method_object[i]['metric'] = metric


    # 4. Create expected output LaTeX figure using specific images path
    output_filename = os.path.join(p_output, 'output.tex')
    print(f'4. Write into LaTeX file {output_filename}')
    f = open(output_filename, 'w')

    # 4.1: Create latex header
    for e_i, est in enumerate(expected_displays):

        f.write(f'\\begin{{subfigure}}[b]{{{expected_figsize[e_i]}\\textwidth}}\n')
        f.write(f'\t\\centering\n')
        f.write(f'\t{est}\n')
        f.write(f'\\end{{subfigure}}\n')

        if e_i < len(expected_displays) - 1:
            f.write(f'~\n')
        
    f.write(f'\n~\n')
    f.write(f'\\vspace{{0.5mm}}\\hrulefill\n\n')

    # 4.2: Prepare data depending of border or crop for each scene and estimator
    for s_i, scene in enumerate(expected_scenes):

        scene_config = expected_scenes_config[scene]

        f.write(f'%{scene}\n')

        right_part = False
        cumul_img_text = {}
        cumul_metric_text = {}
        
        if s_i > 0:
            f.write(f'\\vspace{{2mm}}\n\n')

        for e_i, est in enumerate(expected_estimators):
            
            method = expected_methods[e_i]

            method_object = comparisons_data[scene][e_i]['method']

            if method == expected_right_part_detect and right_part == False:
                right_part = True
                f.write(f'\\begin{{subfigure}}[b]{{{expected_right_part_width}\\textwidth}}\n')
                f.write(f'\t\\centering\n')

            if method == 'border':
                f.write(f'\\begin{{subfigure}}[b]{{{expected_figsize[e_i]}\\textwidth}}\n')
                f.write(f'\t\\centering\n')
                f.write(f'\t\\includegraphics[width=\\textwidth]{{{method_object["img_path"]}}}\n')
                #f.write(f'\t\\vspace{{-0.8mm}}\n')
                f.write(f'\t\\footnotesize{{\\textbf{{{expected_metric.upper()}:}} {method_object["metric"]:.4f}}}\n')
                f.write(f'\\end{{subfigure}}\n')

            # here default crop part
            if method == expected_right_part_detect:

                for i, p in enumerate(scene_config['crops']):

                    if i not in cumul_img_text:
                        cumul_img_text[i] = ''

                    if i not in cumul_metric_text:
                        cumul_metric_text[i] = ''

                    #cumul_img_text[i] += f'\t\\vspace{{0.15mm}}\\includegraphics[width={expected_right_part_size}\\textwidth]{{{method_object[i]["img_path"]}}}\n'
                    cumul_img_text[i] += f'\t\\includegraphics[width={expected_right_part_size}\\textwidth]{{{method_object[i]["img_path"]}}}\n'
                    
                    cumul_metric_text[i] += f'\t\\begin{{subfigure}}{{{expected_right_part_size}\\textwidth}}\n'
                    cumul_metric_text[i] += f'\t\t\\centering\n'
                    cumul_metric_text[i] += f'\t\t\\vspace{{-2.5mm}}\n'
                    #cumul_metric_text[i] += f'\t\t\\scriptsize{{\\textbf{{{expected_metric.upper()}:}} {method_object[i]["metric"]:.4f}}}\n'
                    cumul_metric_text[i] += f'\t\t\\scriptsize{{{method_object[i]["metric"]:.4f}}}\n'
                    cumul_metric_text[i] += f'\t\\end{{subfigure}}\n'

        # now we write right part of figure
        for i, k in enumerate(cumul_img_text):

            f.write(cumul_img_text[k])
            f.write(cumul_metric_text[k])

            if i < len(cumul_metric_text.keys()) - 1:
                f.write('\t\\\\[-1.2mm]\n')

        # 4.3 end figure
        f.write(f'\\end{{subfigure}}\n\n')
    f.write(f'\\hrulefill\n\n')

    print(f'Generation is done...')


        



if __name__ == "__main__":
    main()