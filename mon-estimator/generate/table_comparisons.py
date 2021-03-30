import os
import argparse
import pandas as pd

import numpy as np

M = [5, 11, 15, 25]
scenes = ['p3d_bidir', 'p3d_villa-lights-on', 'p3d_contemporary-bathroom', 'p3d_crown']
scenes_label = ['bidir', 'villa', 'bathroom', 'crown']


labels = [r'$G$-MON$_b$', r'$D$-MON', r'$G$-MON', r'$D$-MON$_p$', r'$G$-MON$_p$', r'Mean', r'MON']
order = [5, 6, 2, 0, 1]

def main():

    parser = argparse.ArgumentParser(description="Create a fully table comparisons")

    parser.add_argument('--input', type=str, help='input csv file', required=True)
    parser.add_argument('--index', type=int, help="Index value to dispayed", required=True)
    parser.add_argument('--output', type=str, help='output table file', required=True)

    args = parser.parse_args()

    p_input  = args.input
    p_index = args.index
    p_output  = args.output

    df = pd.read_csv(p_input, sep=";", header=None)

    f = open(p_output, 'w')

    # start writing table
    table_begin = "\\begin{table*}[ht]\n\\centering\n"
    f.write(table_begin)

    columns = '|'
    for i in range(len(labels) * len(M)):
        columns += 'c|'

    tabular_begin = "\\begin{tabular}{" + columns + "}\n\\hline\n"
    f.write(tabular_begin)

    # first header line
    first_header_line = ""
    for i in order:
        first_header_line += f' & \multicolumn{{{len(order)}}}{{c}}{{{labels[i]}}}'
    first_header_line += "\\hline \\\\\n"
    f.write(first_header_line)

    # second header line
    second_header_line = "Scene / M"

    for i in order:
        for m in M:
            second_header_line += " & " + str(m)
    second_header_line += " \\\\\n"
    f.write(second_header_line)

    # display for each estiamtor and M a specific line for scene
    for s_index, scene in enumerate(scenes):

        line = scenes_label[s_index] 

        for m in M:
            scene_df = df[df.iloc[:, 1] == scene]
            scene_df = scene_df[df.iloc[:, 0].str.contains(f'comparisons-M{m}')]
        
            ssim_values = []

            for i in order:
                row = scene_df.iloc[i]
                ssim_values.append(row[201])

            for ssim in ssim_values:
                line += f" & {ssim:.2f}"

            
        line += " \\\\\n"
        f.write(line)

        

    end_table = "\\hline\n\\end{tabular}\n\\caption{SSIM comparison for each image at level sample}\n \
                \\label{table:ssim_indicators_comparisons}\n \
                \\end{table*}\n"
    f.write(end_table)
    
        

if __name__ == "__main__":
    main()