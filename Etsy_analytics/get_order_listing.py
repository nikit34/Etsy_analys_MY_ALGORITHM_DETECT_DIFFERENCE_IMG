import requests
from lxml import html
import pandas as pd
import os


def get_img(url):
    assert type(url) == str, 'input "url" must be a string type'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    photo = []
    i = 1
    get_img = tree.xpath('//*[@id="content"]/div[3]/div[1]/ul/li[{}]/a/div[1]/div/div[1]/div/div/div/img/@src'.format(i))
    photo.append(get_img[0].replace('\n',''))
    while get_img != []:
        i += 1
        get_img = tree.xpath('//*[@id="content"]/div[3]/div[1]/ul/li[{}]/a/div[1]/div/div[1]/div/div/div/img/@src'.format(i))
        if get_img == []: break
        photo.append(get_img[0].replace('\n',''))
    photos = pd.Series(photo)
    return photos

def get_name_img(url):
    assert type(url) == str, 'input "url" must be a string type'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    name_img = []
    i = 1
    get_name = tree.xpath('//*[@id="content"]/div[3]/div[1]/ul/li[{}]/a/div[2]/div/h2/text()'.format(i))
    name_img.append(get_name[0].replace('\n',''))
    while get_name != []:
        i += 1
        get_name = tree.xpath('//*[@id="content"]/div[3]/div[1]/ul/li[{}]/a/div[2]/div/h2/text()'.format(i))
        if get_name == []: break
        name_img.append(get_name[0].replace('\n',''))
    names = pd.Series(name_img)
    return names


def get_order_list(url='https://www.etsy.com/shop/StudioOlyalya/sold', name_out= 'out_order_list.csv'):
    assert type(name_out) == str, 'input "name_out" must be a string type'
    assert type(url) == str, 'input "url" must be a string type'
    photos = get_img(url)
    names = get_name_img(url)
    order_list = pd.DataFrame(columns = ['names', 'photos'])
    order_list['names'] = names
    order_list['photos'] = photos
    order_list.dropna(how='all')
    out_dir = 'out/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    order_list.to_csv(str(out_dir + name_out), sep='\t', encoding='utf-8', index=False)
    order_list.to_html(str(out_dir + name_out[:-3] + 'html'), index=False)
    return order_list
