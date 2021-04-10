import os
import argparse
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

M = [5, 11, 15, 21, 25]
scenes = ['p3d_bidir', 'p3d_contemporary-bathroom', 'p3d_crown', 'p3d_villa-lights-on']
scenes_label = ['Bidir', 'Bathroom', 'Crown', 'Villa']


labels = [r'$G$-MON$_b$', r'$G$-MON', r'$GG$-MON', r'$D$-MON$_p$', r'$G$-MON$_p$', r'Mean', r'MON']
row_labels = ['gini-binary-mon', 'gini-dmon', 'gini-mon', 'gini-partial-dmon', 'gini-partial-mon', 'mean', 'mon']
order = [5, 6, 0, 1]

def main():

    parser = argparse.ArgumentParser(description="Create a fully table comparisons")

    parser.add_argument('--input', type=str, help='input csv file', required=True)
    parser.add_argument('--output', type=str, help='output table file', required=True)

    args = parser.parse_args()

    p_input  = args.input
    p_output  = args.output

    k_ssim_values = [0.6, 0.7, 0.8]

    df = pd.read_csv(p_input, sep=";", header=None)

    f = open(p_output, 'w')

    # start writing table
    table_begin = "\\begin{table*}[ht]\n\\centering\n\\tiny\n"
    f.write(table_begin)

    # # first multicolumns (M, SSIM and estimator)
    columns = '|c|l|'
    for i in range(len(scenes)):
        for k in k_ssim_values:
            columns += 'r|'

    tabular_begin = "\\begin{tabular}{" + columns + "}\n\\hline\n"
    f.write(tabular_begin)

    # first header line
    first_header_line = f"\\multicolumn{{2}}{{|c|}}{{Scene}}"
    second_header_line = f"\\multicolumn{{2}}{{|c|}}{{SSIM}}"
    for s_index, scene in enumerate(scenes):
        first_header_line += f' & \\multicolumn{{{len(k_ssim_values)}}}{{|c|}}{{{scenes_label[s_index]}}}'

        for k in k_ssim_values:
            second_header_line += f' & \\multicolumn{{1}}{{|c|}}{{{k}}}'

    first_header_line += "\\\\\n"
    second_header_line += "\\\\\n"
    f.write(first_header_line)
    f.write('\\hline\n')
    f.write(second_header_line)

    # display for each M and estimator a specific line
    for m in M:
        
        ssim_values = {}
        scene_spp_kneepoints = {}

        for i in order:

            if i not in ssim_values:
                ssim_values[i] = []

            current_df = df[df.iloc[:, 0].str.contains(f'comparisons-M{m}-{row_labels[i]}')]
            
            for s_index, scene in enumerate(scenes):

                scene_df = current_df[df.iloc[:, 1] == scene]
    
                row = scene_df.iloc[0]

                # linscapre model
                y = np.append(0, row[2:201])
                x = np.arange(len(y))
                
                model = make_interp_spline(x, y)
                xs = np.linspace(np.min(x), np.max(x), 100000)
                
                ys = model(xs)

                ssim_values[i].append(ys)            


        for i in order:

            scene_spp_kneepoints[i] = {}
                
            for s_index, scene in enumerate(scenes):

                scene_spp_kneepoints[i][scene] = []

                for ssim in k_ssim_values:

                    spp_index = None

                    for spp_i, v_ssim in enumerate(ssim_values[i][s_index]):

                        if v_ssim > ssim:
                            spp_index = spp_i + 1
                            break

                    scene_spp_kneepoints[i][scene].append(spp_index)

        # get max expected value

        # write lines
        counter = 0
        for key, arr in scene_spp_kneepoints.items():
            
            line = ""

            if counter == 0:
                f.write('\\hline\n')
                line += f"\\multirow{{{len(order)}}}*{{\\rotatebox{{90}}{{$M = {m}$}}}} & "
            else:
                line += " & "
            
            line += labels[key]

            for s_index, scene in enumerate(scenes):

                # if reduced_max == reduced_current:
                for k_i, k in enumerate(k_ssim_values):
                    
                    # get order of values
                    values = []

                    for i in order:
                         
                        current_v = scene_spp_kneepoints[i][scene][k_i]

                        if current_v == None:
                            current_v = 1000000

                        values.append(current_v)

                    seq = sorted(values)
                    index = [seq.index(v) for v in values]
                    
                    spp_text = scene_spp_kneepoints[key][scene][k_i]

                    if spp_text == None:
                        line += f" & NR ({index[counter]+1})"
                    elif min(values) == spp_text:
                        line += f" & \\textbf{{{spp_text}}} ({index[counter]+1})"
                    else:
                        line += f" & {spp_text} ({index[counter]+1})"
                # else:
                    # line += f" & {reduced_current:.5f} ({index[counter]+1})"
            
            line += " \\\\\n"
            f.write(line)      

            counter += 1

    f.write("\\hline\n\\end{tabular}\n\\caption{SSIM comparison for each scene and different $M$ values for $100,000$ samples}\n")
    f.write("\\label{table:ssim_kneepoint}\n")
    f.write("\\end{table*}\n")

        

if __name__ == "__main__":
    main()