import os
import argparse
import pandas as pd

import numpy as np

M = [5, 11, 15, 21, 25]
scenes = ['p3d_bidir', 'p3d_contemporary-bathroom', 'p3d_crown', 'p3d_villa-lights-on']
scenes_label = ['bidir', 'bathroom', 'crown', 'villa']


labels = [r'$G$-MON$_b$', r'$D$-MON', r'$G$-MON', r'$D$-MON$_p$', r'$G$-MON$_p$', r'Mean', r'MON']
row_labels = ['gini-binary-mon', 'gini-dmon', 'gini-mon', 'gini-partial-dmon', 'gini-partial-mon', 'mean', 'mon']
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

    # first multicolumns (M and estimator)
    columns = '|c|l|'
    for i in range(len(scenes)):
        columns += 'c|'

    tabular_begin = "\\begin{tabular}{" + columns + "}\n\\hline\n"
    f.write(tabular_begin)

    # first header line
    first_header_line = f"\\multicolumn{{2}}{{|c|}}{{Scene}}"
    for s_index, scene in enumerate(scenes):
        first_header_line += f' & {{{scenes_label[s_index]}}}'
    first_header_line += "\\\\\n"
    f.write(first_header_line)

    # display for each M and estimator a specific line
    for m in M:
        
        ssim_values = {}

        for i in order:

            if i not in ssim_values:
                ssim_values[i] = []

            current_df = df[df.iloc[:, 0].str.contains(f'comparisons-M{m}-{row_labels[i]}')]
            
            for s_index, scene in enumerate(scenes):

                scene_df = current_df[df.iloc[:, 1] == scene]
    
                row = scene_df.iloc[0]
                ssim_values[i].append(row[201])    
        
        # get max expected value
        max_scene_ssim = {}
        scene_ssim = {}

        for _, arr in ssim_values.items():
            
            for s_index, scene in enumerate(scenes):
                
                if scene not in max_scene_ssim:
                    max_scene_ssim[scene] = arr[s_index]
                elif max_scene_ssim[scene] < arr[s_index]:
                    max_scene_ssim[scene] = arr[s_index]
                
                if scene not in scene_ssim:
                    scene_ssim[scene] = [arr[s_index]]
                else:
                    scene_ssim[scene].append(arr[s_index])

        # write lines
        counter = 0
        for key, arr in ssim_values.items():
            
            line = ""

            if counter == 0:
                f.write('\\hline\n')
                line += f"\\multirow{{{len(order)}}}*{{$M = {m}$}} & "
            else:
                line += " & "
            
            line += labels[key]

            for s_index, scene in enumerate(scenes):

                seq = sorted(scene_ssim[scene], reverse=True)
                index = [seq.index(v) for v in scene_ssim[scene]]
                
                reduced_max = float(f'{max_scene_ssim[scene]:.5f}')
                reduced_current = float(f'{arr[s_index]:.5f}')

                if reduced_max == reduced_current:
                    line += f" & \\textbf{{{reduced_current:.5f}}} ({index[counter]+1})"
                else:
                    line += f" & {reduced_current:.5f} ({index[counter]+1})"
            
            line += " \\\\\n"
            f.write(line)      

            counter += 1

    f.write("\\hline\n\\end{tabular}\n\\caption{SSIM comparison for each scene and different $M$ values for $100,000$ samples}\n")
    f.write("\\label{table:ssim_indicators_comparisons}\n")
    f.write("\\end{table*}\n")

        

if __name__ == "__main__":
    main()