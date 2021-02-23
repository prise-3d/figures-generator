import os
import json
import argparse
import subprocess
import operator

opposite_point = 50, 50

# scenes_points = {
#     "living-room-3-view0": (950, 338),
#     "villa-view0": (1232, 401),
#     "san-miguel-view0": (1071, 462),
# }

# scenes_points = {
#     "villa-view0-5": (1232, 401),
#     "villa-view0-11": (1232, 401),
#     "villa-view0-21": (1232, 401),
# }

# estimators = [
#     'human',
#     'RNN',
#     'reference'
# ]

# JSON file example
# {
#     "scenes_points": {
#         "arcsphere": [152, 482],
#         "coffee": [119, 509],
#         "cornel-box": [136, 326],
#         "kitchen": [229, 559],
#         "living-room": [422, 381],
#         "pavillon": [241, 339]
#     },
#     "estimators": [
#         "MON",
#         "reference"
#     ]
# }

def main():
    
    parser = argparse.ArgumentParser(description="Add multiple border image using dictionnary")

    parser.add_argument('--folder', type=str, help="data folder where images are save for each estimators", required=True)
    parser.add_argument('--json', type=str, help="specific figure settings", required=True)
    parser.add_argument('--method', type=str, help="specific script to use", choices=['crop', 'border'], required=True)
    parser.add_argument('--output', type=str, required=True)

    args = parser.parse_args()

    p_folder  = args.folder
    p_method = args.method
    p_output = args.output
    p_json = args.json

    json_data = None

    with open(p_json, 'r') as json_file:
        json_data = json.load(json_file)

    estimators = json_data["estimators"]
    scenes_points = json_data["scenes_points"]



    for est in estimators:

        estimator_path = os.path.join(p_folder, est)

        for key, p in scenes_points.items():

            image_path = os.path.join(estimator_path, key + '.png')

            p1 = ','.join(list(map(str, p)))
            p2 = ','.join(list(map(str, tuple(map(operator.add, p, opposite_point)))))

            #images = os.listdir(scene_path)

            # for img in images:

                # img_path = os.path.join(scene_path, img)

            output_image_path = os.path.join(p_output, est, key + '.png')

            if p_method == 'border':
                command_border = "python run/border_image.py --p1 {0} --p2 {1} --img {2} --color {3} --output {4}" \
                    .format(p1, p2, image_path, "red", output_image_path)

                subprocess.call(command_border, shell=True)

            if p_method == 'crop':
                command_crop = "python run/crop_image.py --p1 {0} --p2 {1} --img {2} --output {3}" \
                    .format(p1, p2, image_path, output_image_path)

                subprocess.call(command_crop, shell=True)


if __name__ == "__main__":
    main()