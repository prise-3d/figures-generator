import os
import cv2
import glob

import argparse

def main():

    parser = argparse.ArgumentParser(description="Convert rawls file into png")

    parser.add_argument('--folder', type=str, help='folder with all png files', required=True)
    parser.add_argument('--output', type=str, help='folder with all png files', required=True)

    args = parser.parse_args()

    p_folder = args.folder
    p_output = args.output

    images_path = glob.glob(f"{p_folder}/*.png")

    for img in sorted(images_path):

        image = cv2.imread(img)

        output_path = img.replace(p_folder, p_output)

        output_folder, _ = os.path.split(output_path)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        print(f'Save image into: {output_path}')

        # resize image
        scale_percent = 50  # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(image, dim)

        cv2.imwrite(output_path, resized)
    

if __name__ == "__main__":
    main()