import pandas as pd
import os
from parse_csv import alteration_data


def get_img_dataset(order_file='out/out_order_list.csv'):
    # df_list_download = alteration_data('in/EtsyListingsDownload.csv', 'out_ListingsDownload.csv')

    # подгрузка данных - замена в трех местах ниже
    df_order_items_2019_6 = alteration_data('in/EtsySoldOrderItems2019-6.csv', 'out_SoldOrderItems2019-6.csv')
    df_order_items_2019_5 = alteration_data('in/EtsySoldOrderItems2019-5.csv', 'out_SoldOrderItems2019-5.csv')
    df_order_items_2019_4 = alteration_data('in/EtsySoldOrderItems2019-4.csv', 'out_SoldOrderItems2019-4.csv')
    df_order_items_2019_3 = alteration_data('in/EtsySoldOrderItems2019-3.csv', 'out_SoldOrderItems2019-3.csv')


    df_order_items_2019_6 = df_order_items_2019_6.rename(columns={'Item Name': 'names'})
    df_order_items_2019_5 = df_order_items_2019_5.rename(columns={'Item Name': 'names'})
    df_order_items_2019_4 = df_order_items_2019_4.rename(columns={'Item Name': 'names'})
    df_order_items_2019_3 = df_order_items_2019_3.rename(columns={'Item Name': 'names'})



    assert type(order_file) == str, 'input "order_file" must be a string type'
    df_order_list = pd.read_csv(order_file, sep='\t')
    for i in range(len(df_order_list)):
        df_order_list['names'][i] = df_order_list['names'][i].strip()




    df_res_1 = df_order_list.merge(df_order_items_2019_6[['names', 'Buyer']], how='inner', on='names')
    df_res_2 = df_order_list.merge(df_order_items_2019_5[['names', 'Buyer']], how='inner', on='names')
    df_res_3 = df_order_list.merge(df_order_items_2019_4[['names', 'Buyer']], how='inner', on='names')
    df_res_4 = df_order_list.merge(df_order_items_2019_3[['names', 'Buyer']], how='inner', on='names')

    df_res = pd.concat([df_res_1, df_res_2, df_res_3, df_res_4], ignore_index=True)




    df_res.dropna(how='all')
    out_dir = 'out/'
    name_out = 'analytic_img.csv'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    df_res.to_csv(str(out_dir + name_out), sep='\t', encoding='utf-8', index=False)
    df_res.to_html(str(out_dir + name_out[:-3] + 'html'), index=False)
