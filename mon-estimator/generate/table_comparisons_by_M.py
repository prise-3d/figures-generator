import os
import argparse
import pandas as pd

import numpy as np

M = [5, 11, 15, 21, 25]
scenes = ['p3d_bidir', 'p3d_contemporary-bathroom', 'p3d_crown', 'p3d_villa-lights-on']
scenes_label = ['Bidir', 'Bathroom', 'Crown', 'Villa']


labels = [r'Jung et al.', r'$G$-MoN$_b$', r'$G$-MoN', r'$GG$-MoN', r'$D$-MoN$_p$', r'$G$-MoN$_p$', r'Mean', r'MoN']
row_labels = ['djung', 'gini-binary-mon', 'gini-dmon', 'gini-mon', 'gini-partial-dmon', 'gini-partial-mon', 'mean', 'mon']
order = [6, 7, 0, 1, 2]

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

    mean_values = [] # keep same values for mean

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

                if labels[i] == 'Mean' and len(mean_values) < len(scenes):
                    mean_values.append(row[201])
        
        # get max expected value
        max_scene_ssim = {}
        scene_ssim = {}

        for key, arr in ssim_values.items():

            current_values = arr

            if labels[key] == 'Mean':
                current_values = mean_values
            
            for s_index, scene in enumerate(scenes):
                
                if scene not in max_scene_ssim:
                    max_scene_ssim[scene] = current_values[s_index]
                elif max_scene_ssim[scene] < current_values[s_index]:
                    max_scene_ssim[scene] = current_values[s_index]
                
                if scene not in scene_ssim:
                    scene_ssim[scene] = [current_values[s_index]]
                else:
                    scene_ssim[scene].append(current_values[s_index])

        # write lines
        counter = 0
        for key, arr in ssim_values.items():
            
            current_values = arr

            if labels[key] == 'Mean':
                current_values = mean_values


            line = ""

            if counter == 0:
                f.write('\\hline\n')
                line += f"\\multirow{{{len(order)}}}*{{\\rotatebox{{90}}{{$M = {m}$}}}} & "
            else:
                line += " & "
            
            line += labels[key]

            for s_index, scene in enumerate(scenes):

                seq = sorted(scene_ssim[scene], reverse=True)
                index = [seq.index(v) for v in scene_ssim[scene]]
                
                reduced_max = float(f'{max_scene_ssim[scene]:.5f}')
                reduced_current = float(f'{current_values[s_index]:.5f}')

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