import pandas as pd
import numpy as np
from glob import glob
import argparse

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as po

vga_list = ['2060','2070','2080','3060','3070','3080']
vga_ti_list = ['2080','3060','3070','3080']


def clean_currency(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    if isinstance(x, str):
        return(x.replace(',', ''))
    return(x)


def withoutti(df,vga):
    vga_df =df[df.Name.str.contains(vga) & ~df.Name.str.contains('Ti')]

    # 몇몇 불필요 columns 삭제 ( 해당 부분 재설정 필요 )
    vga_df = vga_df.set_index('Name').drop(['Id_x','Id_y'],axis=1)

    # value를 str 에서 int로 변경
    for col_ in vga_df.columns:
        vga_df[col_] = vga_df[col_].apply(clean_currency)
        vga_df[col_] = pd.to_numeric(vga_df[col_], errors='coerce')

    # 0를 nan으로 변경
    vga_df = vga_df.replace(0, np.NaN)

    # graph 생성
    fig = px.line(vga_df.T)
    po.write_html(fig, file=f'./graph/vga_{vga}_graph.html',auto_open=False)

    # 평균 그래프 생성
    fig = px.line(vga_df.mean())
    po.write_html(fig, file=f'./graph/vga_{vga}_average_graph.html',auto_open=False)


def withti(df,vga):
    vga_df =df[df.Name.str.contains(vga) & df.Name.str.contains('Ti')]

    # 몇몇 불필요 columns 삭제 ( 해당 부분 재설정 필요 )
    vga_df = vga_df.set_index('Name').drop(['Id_x','Id_y'],axis=1)

    # value를 str 에서 int로 변경
    for col_ in vga_df.columns:
        vga_df[col_] = vga_df[col_].apply(clean_currency)
        vga_df[col_] = pd.to_numeric(vga_df[col_], errors='coerce')

    # 0를 nan으로 변경
    vga_df = vga_df.replace(0, np.NaN)

    # graph 생성
    fig = px.line(vga_df.T)
    po.write_html(fig, file=f'./graph/vga_{vga}Ti_graph.html',auto_open=False)

    # 평균 그래프 생성
    fig = px.line(vga_df.mean())
    po.write_html(fig, file=f'./graph/vga_{vga}Ti_average_graph.html',auto_open=False)


def main():
    # 2021년 그래프
    vga_csv_list = glob('./Danawa-Crawler/crawl_data/Last_Data/2021-*/VGA.csv')
    # 시작 설정
    df = pd.read_csv(vga_csv_list[0])

    for vga_path in vga_csv_list[0:]:
        df = df.merge(pd.read_csv(vga_path), how='outer', on='Name')

    # 최신 추가
    df = df.merge(pd.read_csv('./Danawa-Crawler/crawl_data/VGA.csv'), how='outer', on='Name')

    for vga in vga_list:
        withoutti(df,vga)

        if vga in vga_ti_list:
            withti(df,vga)



if __name__ == '__main__':
    main()
