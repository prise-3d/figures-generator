import os
import numpy as np

from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import peak_signal_noise_ratio as psnr

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

    if color == 'lightgreen':   
        return np.array([46, 184, 46])

    if color == 'lightyellow': 
        return np.array([255, 255, 153])

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
        for x in np.arange(p1_x, p2_x + size):
            img_arr[p1_y + i][x] = get_color(color)
            img_arr[p2_y + i][x] = get_color(color)

        for y in np.arange(p1_y, p2_y + size):
            img_arr[y][p1_x + i] = get_color(color)
            img_arr[y][p2_x  + i] = get_color(color)

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
