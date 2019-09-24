from get_order_listing import get_order_list
import pandas as pd
from analytic_img import get_rbg_value_colors
from building_analytics_img import get_img_dataset
from graphics import build_graphics
import os


def main():
    pd.set_option('display.max_columns', 500)  # опция для отображения датасета в ширину


    # df_order_list = get_order_list()  # запарсить страницу Etsy с фото проданных товаров
    get_img_dataset()  # сформировать датасет из фото и покупателей
    get_rbg_value_colors()  # получить RGB
    build_graphics()  # построить 3d модель


if __name__ == '__main__':
    main()
