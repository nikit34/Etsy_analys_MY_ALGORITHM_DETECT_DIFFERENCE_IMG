import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import math
from tqdm import tqdm


def del_col(arr_rgb):
    n = np.shape(arr_rgb)[1]-1
    m = np.shape(arr_rgb)[0]
    calc_col = []
    for i in range(m):
        calc_col.append([0] * n)

    for w in range(n):
        for h in range(m):
            calc_col[h][w] = abs(arr_rgb[h][w]-arr_rgb[h][w+1])

    max_sum_col_r = max(np.sum(calc_col[0], axis=0))
    max_sum_col_g = max(np.sum(calc_col[1], axis=0))
    max_sum_col_b = max(np.sum(calc_col[2], axis=0))

    del_count = 0
    for w in range(n):
        sum_col = 0
        for h in range(m):
            sum_col += sum(calc_col[h][w])
        if sum_col < (0.2*(max_sum_col_r+max_sum_col_g+max_sum_col_b)):
            arr_rgb = np.delete(arr_rgb, w-del_count, axis=1)
            del_count += 1
    arr_rgb = np.delete(arr_rgb, np.shape(arr_rgb)[1]-1, axis=1)
    return arr_rgb


def del_row(arr_cut_col):
    n = np.shape(arr_cut_col)[1]
    m = np.shape(arr_cut_col)[0]-1
    calc_row = []
    for i in range(m):
        calc_row.append([0] * n)

    for w in range(n):
        for h in range(m):
            calc_row[h][w] = abs(arr_cut_col[h][w]-arr_cut_col[h+1][w])

    max_sum_row_r = max(np.sum(calc_row[0], axis=1))
    max_sum_row_g = max(np.sum(calc_row[1], axis=1))
    max_sum_row_b = max(np.sum(calc_row[2], axis=1))

    del_count = 0
    for w in range(n):
        sum_row = 0
        for h in range(m):
            sum_row += sum(calc_row[h][w])
        if sum_row < (0.2*(max_sum_row_r+max_sum_row_g+max_sum_row_b)):
            arr_cut_col = np.delete(arr_cut_col, h-del_count, axis=0)
            del_count += 1
    arr_cut_col = np.delete(arr_cut_col, np.shape(arr_cut_col)[0]-1, axis=0)
    return arr_cut_col


def mean_rectangles(arr_cut, k_field=7):
    means = []
    y_last = 0
    for y_rec in range(1,k_field+1):
        x_last = 0
        y_tmp = int((y_rec/k_field)*np.shape(arr_cut)[0])
        for x_rec in range(1,k_field+1):
            mean_r = mean_g = mean_b = 0
            x_tmp = int((x_rec/k_field)*np.shape(arr_cut)[1])
            for y in range(y_last, y_tmp):
                for x in range(x_last, x_tmp):
                    mean_r += arr_cut[y][x][0]
                    mean_g += arr_cut[y][x][1]
                    mean_b += arr_cut[y][x][2]
            means.append([int(mean_r/((x_tmp-x_last)*(y_tmp-y_last))),int(mean_g/((x_tmp-x_last)*(y_tmp-y_last))),int(mean_b/((x_tmp-x_last)*(y_tmp-y_last)))])
            x_last = x_tmp
        y_last = y_tmp
    return means


def difference(means, len_means):
    diff_items = []
    for i in range(int(len_means), int((len_means-2)**2)):
        diff_items.append(np.array(np.int64(abs(np.array(means[i-1])-np.array(means[i])))) + np.array(np.int64(abs(np.array(means[i+1])-np.array(means[i])))) + np.array(np.int64(abs(np.array(means[i-int(len_means)])-np.array(means[i])))) + np.array(np.int64(abs(np.array(means[i+int(len_means)])-np.array(means[i])))) + np.array(np.int64(abs(np.array(means[i-int(len_means)-1])-np.array(means[i])))) + np.array(np.int64(abs(np.array(means[i-int(len_means)+1])-np.array(means[i])))) + np.array(np.int64(abs(np.array(means[i+int(len_means)-1])-np.array(means[i])))) + np.array(np.int64(abs(np.array(means[i+int(len_means)+1])-np.array(means[i])))))
    return diff_items


def get_rbg_value_colors(img_file='out/analytic_img.csv'):
    assert type(img_file) == str, 'input "img_file" must be a string type'
    data = pd.read_csv(img_file, sep='\t')
    rgb_ratio = []

    for i in tqdm(range(len(data))):
        response = requests.get(str(data.iloc[i,1]))
        img = Image.open(BytesIO(response.content))
        img_rgb = img.convert('RGB')
        arr_rgb = np.array(img_rgb)
        arr_cut_col = del_col(arr_rgb)
        arr_cut = del_row(arr_cut_col)
        k_field = 13
        means = mean_rectangles(arr_cut, k_field)
        difference_means = difference(means, int(math.sqrt(len(means))))
        rgb_ratio.append(np.round((sum(difference_means)/len(difference_means))/(256*3), 3))

    data['RGB'] = pd.Series(rgb_ratio)

    name_out = 'names_buyer_rgb.csv'
    out_dir = 'out/'
    data.to_csv(out_dir + name_out, sep='\t', encoding='utf-8', index=False)
    data.to_html(str(out_dir + name_out[:-3] + 'html'), index=False)

get_rbg_value_colors()
