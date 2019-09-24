import pandas as pd
import numpy as np
import csv
import os
import sys
from tqdm import tqdm

def alteration_data(name_in, name_out):
    assert type(name_in) == str, 'input "name_in" must be a string type'
    assert type(name_out) == str, 'input "name_out" must be a string type'
    data = pd.DataFrame(None)
    with open(name_in, 'r') as f_1:
        data_1 = csv.reader(f_1)
        index = 0
        columns = []
        for dat in tqdm(data_1):
            '!!!'.join(dat)
            for i in range(len(dat)):
                dat[i] = dat[i].split('!!!')
                if index == 0:
                    columns.append(str(dat[i][0]))
                else:
                    dat[i][0] = dat[i][0].replace('\n',' ')
                    data = pd.DataFrame(data, columns=columns, index = range(index))
                    data.iloc[index-1, i] = dat[i][0]
            index += 1
        f_1.close()
    data.dropna(how='all')
    out_dir = 'out/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    data.to_csv(str(out_dir + name_out), sep='\t', encoding='utf-8', index=False)
    data.to_html(str(out_dir + name_out[:-3] + 'html'), index=False)

    return data
