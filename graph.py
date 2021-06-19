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

class vga_graph():
    def __init__(self):
        self.vga_list = ['2060','2070','2080','3060','3070','3080']
        self.vga_ti_list = ['2080','3060','3070','3080']


    def withoutti(self,df,vga):
        vga_df =df[df.index.str.contains(vga) & ~df.index.str.contains('Ti')]

        # graph 생성
        fig = px.line(vga_df.T)
        po.write_html(fig, file=f'./graph/vga_{vga}_graph.html',auto_open=False)

        # 평균 그래프 생성
        self.average_graph.loc[f'{vga}'] = vga_df.mean()


    def withti(self,df,vga):
        vga_df =df[df.index.str.contains(vga) & df.index.str.contains('Ti')]

        # graph 생성
        fig = px.line(vga_df.T)
        po.write_html(fig, file=f'./graph/vga_{vga}Ti_graph.html',auto_open=False)

        # 평균 그래프 생성
        self.average_graph.loc[f'{vga}Ti'] = vga_df.mean()


    def main(self):
        # 2021년 그래프
        vga_csv_list = glob('./Danawa-Crawler/crawl_data/Last_Data/2021-*/VGA.csv')
        # 시작 설정
        df = pd.read_csv(vga_csv_list[0])

        for vga_path in vga_csv_list[0:]:
            df = df.merge(pd.read_csv(vga_path), how='outer', on='Name')

        # 최신 추가
        df = df.merge(pd.read_csv('./Danawa-Crawler/crawl_data/VGA.csv'), how='outer', on='Name')
        
        # 몇몇 불필요 columns 삭제 ( 해당 부분 재설정 필요 )
        df = df.set_index('Name').drop(['Id_x','Id_y'],axis=1)

        # value를 str 에서 int로 변경
        for col_ in df.columns:
            df[col_] = df[col_].apply(clean_currency)
            df[col_] = pd.to_numeric(df[col_], errors='coerce')

        # 0를 nan으로 변경
        df = df.replace(0, np.NaN)

        self.average_graph = pd.DataFrame(columns=df.columns)

        for vga in self.vga_list:
            self.withoutti(df,vga)

            if vga in self.vga_ti_list:
                self.withti(df,vga)

        # 평균 그래프 생성
        fig = px.line(self.average_graph.T)
        po.write_html(fig, file=f'./graph/Total_average_graph.html',auto_open=False)


if __name__ == '__main__':
    vga_graph = vga_graph()
    vga_graph.main()
