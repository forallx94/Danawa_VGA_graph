import pandas as pd
import numpy as np
from glob import glob
import argparse

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as po

def clean_currency(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    if isinstance(x, str):
        return(x.replace(',', ''))
    return(x)


def main(contain_str,without_str):
    # 2021년 그래프
    vga_csv_list = glob('./Danawa-Crawler/crawl_data/Last_Data/2021-*/VGA.csv')

    # 시작 설정
    df = pd.read_csv(vga_csv_list[0])
    vga_df = df[df.Name.str.contains(contain_str) & ~df.Name.str.contains(without_str)]

    # 나머지 설정
    for vga_path in vga_csv_list[0:]:
        df = pd.read_csv(vga_path)
        vga_df =vga_df.merge(df[df.Name.str.contains(contain_str) & ~df.Name.str.contains(without_str)], how='outer', on='Name')

    # 최신 추가
    df = pd.read_csv('./Danawa-Crawler/crawl_data/VGA.csv')
    vga_df =vga_df.merge(df[df.Name.str.contains(contain_str) & ~df.Name.str.contains(without_str)], how='outer', on='Name')

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
    po.write_html(fig, file=f'./graph/vga_{contain_str}_graph.html',auto_open=False)

    # 평균 그래프 생성
    fig = px.line(vga_df.mean())
    po.write_html(fig, file=f'./graph/vga_{contain_str}_average_graph.html',auto_open=False)


    # 최신 월 그래프
    df = pd.read_csv('./Danawa-Crawler/crawl_data/VGA.csv')
    vga_df = df[df.Name.str.contains(contain_str) & ~df.Name.str.contains(without_str)]

    # value를 str 에서 int로 변경
    for col_ in vga_df.columns:
        vga_df[col_] = vga_df[col_].apply(clean_currency)
        vga_df[col_] = pd.to_numeric(vga_df[col_], errors='coerce')

    # 0를 nan으로 변경
    vga_df = vga_df.replace(0, np.NaN)

    # graph 생성
    fig = px.line(vga_df.T)
    po.write_html(fig, file=f'./graph/latest_vga_{contain_str}_graph.html',auto_open=False)

    # 평균 그래프 생성
    fig = px.line(vga_df.mean())
    po.write_html(fig, file=f'./graph/latest_vga_{contain_str}_average_graph.html',auto_open=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contain_str", type=str, default="3060",
        help="contain string"
    )

    parser.add_argument(
        "--without_str", type=str, default="Ti",
        help="without string"
    )

    args = parser.parse_args()
    main(**vars(args))
