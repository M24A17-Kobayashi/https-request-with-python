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

    ntt, kddi, cableTV, origin_line, misc = count_career(origin_tdhkn_df)
    count_list = [ntt, kddi, cableTV, origin_line,misc]
    label=["ntt", "kddi", "cableTV", "origin_line","misc"]

    misc_index = label.index('misc')
    misc_data = count_list.pop(misc_index)
    misc_label = label.pop(misc_index)
    sorted_count_label = sorted(zip(count_list, label), reverse=True)
    sorted_count, sorted_label = zip(*sorted_count_label)
    prov_count = list(sorted_count)+[misc_data]
    prov_label = list(sorted_label)+[misc_label]

    fig, ax = plt.subplots()
    plt.pie(prov_count, labels=prov_label,autopct="%1.1f%%",startangle=90 ,counterclock=False)
    plt.savefig(IMAGE_PATH+"top3_prov_pie.png")


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
        writer.writerow(["var", round(np.array(ping_list).var(),2), round(np.array(download_list).var(),2) , round(np.array(upload_list).var(),2)])
        writer.writerow(["std", round(np.array(ping_list).std(),2), round(np.array(download_list).std(),2) , round(np.array(upload_list).std(),2)])
    return ping_list,download_list ,upload_list

def count_career(origin_tdhkn_df):
    top3_prov_list = make_all_prov_list(origin_tdhkn_df)
    ntt_set = make_career_set("NTT.txt")
    kddi_set = make_career_set("KDDI.txt")
    cableTV_set = make_career_set("CABLETV.txt")
    origin_line_set = make_career_set("ORIGINAL_LINE.txt")

    ntt_count = 0
    kddi_count = 0
    cableTV_count = 0
    origin_line_count = 0
    misc_count = 0

    for prov in top3_prov_list:
        if prov in ntt_set:
            ntt_count += 1
        elif prov in kddi_set:
            kddi_count += 1
        elif prov in cableTV_set:
            cableTV_count += 1
        elif prov in origin_line_set:
            origin_line_count += 1
        else:
            misc_count += 1
    return ntt_count,kddi_count,cableTV_count,origin_line_count, misc_count

def make_all_prov_list(origin_tdhkn_df):
    prov_list = list()
    for i in range(len(origin_tdhkn_df)):
        prov_list.append(origin_tdhkn_df['first_prov'][i])
        prov_list.append(origin_tdhkn_df['second_prov'][i])
        prov_list.append(origin_tdhkn_df['third_prov'][i])
    return prov_list

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

def make_all_prov_set(origin_tdhkn_df):
    prov_set = set()
    for i in range(len(origin_tdhkn_df)):
        if not origin_tdhkn_df['first_prov'][i] in prov_set:
            prov_set.add(origin_tdhkn_df['first_prov'][i])
        if not origin_tdhkn_df['second_prov'][i] in prov_set:
            prov_set.add(origin_tdhkn_df['second_prov'][i])
        if not origin_tdhkn_df['third_prov'][i] in prov_set:
            prov_set.add(origin_tdhkn_df['third_prov'][i])
    return prov_set
main()