import os
import argparse
import json

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

import uuid

# Expected JSON format
# folder need to have same number of files of each elements in json

#  {
#     "estimators": [
#         "RNN",
#         "human",
#         "reference",
#         "RNN",
#         "human",
#         "reference"
#     ],
#     "figsize": [
#         "0.16",
#         "0.16",
#         "0.16",
#         "0.16",
#         "0.16",
#         "0.16"
#     ],
#     "scenes": [
#         "arcsphere",
#         "kitchen",
#         "cornel-box",
#         "coffee",
#         "living-room",
#         "pavillon"
#     ],
#     "methods": [
#         "border",
#         "border",
#         "border",
#         "crop",
#         "crop",
#         "crop"
#     ]
#  }

# 0 => figure size
# 1 => prefix path
# 2 => border or crop
# 3 => estimator
# 4 => image_path
# 5 => score
figure_str = "\\begin{{subfigure}}[t]{{{0}\\textwidth}}\n\t\centering\n\t\includegraphics[width=\\textwidth]{{{1}}}\n\t\\footnotesize{{{2}: {3:.2f}}}\n\end{{subfigure}}\n"

end_str = "\\begin{{subfigure}}[t]{{{0}\\textwidth}}\n\t\centering\n\t{1}\n\end{{subfigure}}\n"

def main():
    
    parser = argparse.ArgumentParser(description="Compute image figure as output")

    parser.add_argument('--json', type=str, help="specific figure settings", required=True)
    parser.add_argument('--output', type=str, required=True)

    args = parser.parse_args()

    p_json = args.json
    p_output = args.output

    output_f = open(p_output, 'w')

    json_data = None

    with open(p_json, 'r') as json_file:
        json_data = json.load(json_file)

    p_folder = os.path.join(json_data['output'], json_data['nsamples'], 'metrics')

    comparisons = []
    comparisons_data = sorted(os.listdir(p_folder))

    for comp in comparisons_data:
        comp_path = os.path.join(p_folder, comp)

        with open(comp_path, 'r') as f:

            current_comparisons = {}
            for line in f.readlines():

                data = line.split(';')

                current_comparisons[data[0]] = (data[1], float(data[-1]))
            
            comparisons.append(current_comparisons)

    unique_output_folder = os.path.join(json_data['output'], str(uuid.uuid4()))

    if not os.path.exists(unique_output_folder):
        os.makedirs(unique_output_folder)

    for id_scene, scene in enumerate(json_data["scenes"]):
        
        output_f.write("% {0}\n".format(scene))
        for index, est in enumerate(json_data["estimators"]):
            
            figsize = json_data["figsize"][index]
            method = json_data["methods"][index]
            
            img_name, score = comparisons[index][scene]

            # 0 => figure size
            # 1 => prefix path
            # 2 => border or crop
            # 3 => estimator
            # 4 => image_path
            # 5 => score
            current_image_name = os.path.join(json_data['output'], json_data['nsamples'], 'processing', method, est, img_name)

            # HERE for each line create unique identifier
            output_unique_image = str(uuid.uuid4()) + '.png'
            output_image_path = os.path.join(unique_output_folder, output_unique_image)

            os.system(f'cp {current_image_name} {output_image_path}')

            output_f.write(figure_str.format(figsize, output_image_path, json_data["metric"].upper(), score))


        if id_scene < len(json_data["scenes"]) - 1:
            output_f.write("\n\\vspace{2mm}\n~\n\n")

    output_f.write("\n\\vspace{5mm}\hrulefill\n~\n\n")

    for index, est in enumerate(json_data["displays"]):

        figsize = json_data["figsize"][index]
        output_f.write(end_str.format(figsize, est))




if __name__ == "__main__":
    main()