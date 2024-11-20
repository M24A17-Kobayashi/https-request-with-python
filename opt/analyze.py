from config import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from icecream import ic
import csv

"""
TODO
・地域別の分析          :   最大，最小，平均，箱ひげ
・キャリア別の分析      :   最大，最小，平均，箱ひげ
・TOP3のキャリアの内訳  :   円グラフ
"""


def main():
    origin_tdhkn_df = pd.read_csv(CSV_PATH+'todouhuken.csv')

    career_set = make_all_career_set(origin_tdhkn_df)
    ntt_set = make_career_set("NTT.txt")
    kddi_set = make_career_set("KDDI.txt")
    cableTV_set = make_career_set("CABLETV.txt")
    origin_line_set = make_career_set("ORIGINAL_LINE.txt")


    hokkaido_ping, hokkaido_download , hokkaido_upload = calc_region_data("hokkaido.txt",origin_tdhkn_df)
    tohoku_ping, tohoku_download , tohoku_upload = calc_region_data("tohoku.txt",origin_tdhkn_df)
    kanto_ping, kanto_download , kanto_upload = calc_region_data("kanto.txt",origin_tdhkn_df)
    chubu_ping, chubu_download , chubu_upload = calc_region_data("chubu.txt",origin_tdhkn_df)
    kinki_ping, kinki_download , kinki_upload = calc_region_data("kinki.txt",origin_tdhkn_df)
    chugoku_ping, chugoku_download , chugoku_upload = calc_region_data("chugoku.txt",origin_tdhkn_df)
    shikoku_ping, shikoku_download , shikoku_upload = calc_region_data("shikoku.txt",origin_tdhkn_df)
    kyushu_ping, kyushu_download , kyushu_upload = calc_region_data("kyushu.txt",origin_tdhkn_df)

    fig, ax = plt.subplots()
    ax.boxplot((hokkaido_ping,tohoku_ping,kanto_ping,chubu_ping,kinki_ping,chugoku_ping, shikoku_ping,kyushu_ping))
    plt.ylabel('ping')
    plt.xlabel('region')
    ax.set_xticklabels(['hokkaido', 'tohoku', 'kanto', 'chubu', 'kinki', 'chugoku', 'shikoku', 'kyushu'])
    plt.savefig(IMAGE_PATH+"ping_boxplot.png")

    fig, ax = plt.subplots()
    ax.boxplot((hokkaido_download,tohoku_download,kanto_download,chubu_download,kinki_download,chugoku_download, shikoku_download,kyushu_download))
    plt.ylabel('download')
    plt.xlabel('region')
    ax.set_xticklabels(['hokkaido', 'tohoku', 'kanto', 'chubu', 'kinki', 'chugoku', 'shikoku', 'kyushu'])
    plt.savefig(IMAGE_PATH+"download_boxplot.png")

    fig, ax = plt.subplots()
    ax.boxplot((hokkaido_upload,tohoku_upload,kanto_upload,chubu_upload,kinki_upload,chugoku_upload, shikoku_upload,kyushu_upload))
    plt.ylabel('upload')
    plt.xlabel('region')
    ax.set_xticklabels(['hokkaido', 'tohoku', 'kanto', 'chubu', 'kinki', 'chugoku', 'shikoku', 'kyushu'])
    plt.savefig(IMAGE_PATH+"upload_boxplot.png")



def calc_region_data(file_name, tdhkn_df):
    ping_list = list()
    download_list = list()
    upload_list = list()

    region_set = make_region_set(file_name)

    for tdhken in region_set:
        region_df = tdhkn_df[tdhkn_df["tdhkn_yomi"]==tdhken]
        ping = region_df.ave_ping.iloc[0]
        ping_list.append(ping)
        download = region_df.ave_download.iloc[0]
        download_list.append(download)
        upload = region_df.ave_upload.iloc[0]
        upload_list.append(upload)

    with open(CSV_PATH+file_name[:-4]+".csv", 'w') as f:
        writer=csv.writer(f)
        writer.writerow(["","ping", "download", "upload"])
        writer.writerow(["max", np.array(ping_list).max(), np.array(download_list).max(), np.array(upload_list).max()])
        writer.writerow(["min", np.array(ping_list).min(), np.array(download_list).min(), np.array(upload_list).min()])
        writer.writerow(["mean", round(np.array(ping_list).mean(),2), round(np.array(download_list).mean(),2) , round(np.array(upload_list).mean(),2)])
    return ping_list,download_list ,upload_list
        # fig, ax = plt.subplots()
        # plt.savefig(IMAGE_PATH+file_name[:-4]+".png")

# def drow_boxplot():

def make_all_career_set(origin_tdhkn_df):
    career_set = set()
    for i in range(len(origin_tdhkn_df)):
        if not origin_tdhkn_df['first_prov'][i] in career_set:
            career_set.add(origin_tdhkn_df['first_prov'][i])
        if not origin_tdhkn_df['second_prov'][i] in career_set:
            career_set.add(origin_tdhkn_df['second_prov'][i])
        if not origin_tdhkn_df['third_prov'][i] in career_set:
            career_set.add(origin_tdhkn_df['third_prov'][i])
    return career_set

def make_career_set(file_name):
    career_set = set()
    with open(CAREER_PATH+file_name) as f:
        lines = [line.rstrip() for line in f.readlines()]
        for line in lines:
            career_set.add(line)
    return career_set

def make_region_set(file_name):
    region_set = set()
    with open(REGION_PATH+file_name) as f:
        lines = [line.rstrip() for line in f.readlines()]
        for line in lines:
            i,tdhkn_kanji,tdhkn_yomi = line.split("\t")
            region_set.add(tdhkn_yomi)
    return region_set





main()