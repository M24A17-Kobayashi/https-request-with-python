from config import *
import bs4
import re
from icecream import ic
import pandas as pd

def main():
    ave_data_list=[]
    top3_data_list=[]
    top3_name_list=[]
    #　ファイル名の読み込み
    tdhkn_text=get_tdhkn_text()
    name_list1 = create_file_name1(tdhkn_text)

    for html_name1 in name_list1:
        top3_ave_list=[]
        ave_data_list.append(extract_ave(html_name1))
        top3_name_list.append(extract_top3_name(html_name1))
        name_list2 = create_file_name2(html_name1)
        for html_name2 in name_list2:
             top3_ave_list.append(extract_ave(html_name2))
        top3_data_list.append(top3_ave_list)
    # ic(ave_data_list)
    # ic(top3_data_list)
    # ic(top3_name_list)
    data_csv=convert_ave_data(tdhkn_text,ave_data_list,top3_data_list,top3_name_list)
    save_csv(data_csv)


def get_tdhkn_text():
    tdhkn_lines=[]
    with open(TODOUHUKEN) as f:
        lines = [s.rstrip() for s in f.readlines()]
        for line in lines:
            tdhkn_lines.append(line)
    return tdhkn_lines

def create_file_name1(tdhkn_text):
    name_list=[]
    for line in tdhkn_text:
        i,tdhkn_kanji,tdhkn_yomi = line.split("\t")
        name_list.append(HTML_PATH+str(i)+"_"+str(tdhkn_yomi)+".html")
    return name_list

def create_file_name2(html_name):
    name_list=[]
    for i in range(1,4):
        name_list.append(html_name[:-5]+"_"+str(i)+"_of_3.html")
    return name_list

def extract_ave(html_name):
    # ファイルから平均ping，平均ダウンロード速度，平均アップロード速度の抽出
    ave={}
    soup = bs4.BeautifulSoup(open(html_name,encoding = 'utf-8'),'html.parser')
    element=soup.find(attrs={"class":"mb-xxxs"})
    if element:
        spans=element.find_all('span', {"class": "text-bold"})
        # ic(spans)
        if len(spans):
            ping_texts = [span.get_text(strip=True) for span in spans]
            matchs=[]
            pattern1 = r'^([0-9]+\.[0-9]+)ms$' # ping用
            pattern2 = r'^([0-9]+\.[0-9]+)Mbps$' # download,upload用
            matchs.append(re.search(pattern1, ping_texts[0])) # ping
            matchs.append(re.search(pattern2, ping_texts[1])) # download
            matchs.append(re.search(pattern2, ping_texts[2])) # upload
            # ic(matchs)
            if len(matchs):
                print(html_name.split("/")[-1])
                ave_ping_value = matchs[0].group(1)
                ave_download_value = matchs[1].group(1)
                ave_upload_value = matchs[2].group(1)
                print(f"平均Ping値: {ave_ping_value} ms")
                print(f"平均ダウンロード速度: {ave_download_value} Mbps")
                print(f"平均アップロード速度: {ave_upload_value} Mbps")
                ave["ave_ping"]=ave_ping_value
                ave["ave_download"]=ave_download_value
                ave["ave_upload"]=ave_upload_value
            else:
                print("正規表現にマッチしませんでした")
        else:
            print("spanがありません")
    else:
        print("mb-xxxsがありません")
    return ave

def extract_top3_name(html_name):
    name_list = []
    soup = bs4.BeautifulSoup(open(html_name, encoding='utf-8'), 'html.parser')
    element = soup.find(attrs={"class": "mt-6"})
    if element:
        top3_name = element.find_all("a")
        # ic(top3_name)
        if len(top3_name):
            # 正規表現パターンを修正して全角括弧に対応
            pattern = r'^(.*?)[（(][^）)]+[）)]$'
            for name in top3_name:
                text = name.get_text(strip=True)
                # ic(repr(text))
                # 末尾の'(数字+件)'を削除
                text_without_count = re.sub(r'[（(]\d+件[）)]$', '', text)
                # ic(repr(text_without_count))
                print(text_without_count)
                name_list.append(text_without_count)
        else:
            print("aタグがない")
    else:
        print("elementがない")
    return name_list

def convert_ave_data(tdhkn_text,ave_data_list,top3_data_list,top3_name_list):
    tdhkn_num_list=[]
    tdhkn_kanji_list=[]
    tdhkn_yomi_list=[]

    for line in tdhkn_text:
        tdhkn_num,tdhkn_kanji,tdhkn_yomi = line.split("\t")
        tdhkn_num_list.append(tdhkn_num)
        tdhkn_kanji_list.append(tdhkn_kanji)
        tdhkn_yomi_list.append(tdhkn_yomi)

    ave_ping_list=[]
    ave_download_list=[]
    ave_upload_list=[]

    for ave_data in ave_data_list:
        ave_ping_list.append(ave_data["ave_ping"])
        ave_download_list.append(ave_data["ave_download"])
        ave_upload_list.append(ave_data["ave_upload"])

    first_prov_list=[]
    second_prov_list=[]
    third_prov_list=[]

    for prov_name in top3_name_list:
        first_prov_list.append(prov_name[0])
        second_prov_list.append(prov_name[1])
        third_prov_list.append(prov_name[2])


    first_prov_ping=[]
    first_prov_download=[]
    first_prov_upload=[]
    second_prov_ping=[]
    second_prov_download=[]
    second_prov_upload=[]
    third_prov_ping=[]
    third_prov_download=[]
    third_prov_upload=[]


    for top3_data in top3_data_list:
        first_prov_ping.append(top3_data[0]['ave_ping'])
        first_prov_download.append(top3_data[0]['ave_download'])
        first_prov_upload.append(top3_data[0]['ave_upload'])
        second_prov_ping.append(top3_data[1]['ave_ping'])
        second_prov_download.append(top3_data[1]['ave_download'])
        second_prov_upload.append(top3_data[1]['ave_upload'])
        third_prov_ping.append(top3_data[2]['ave_ping'])
        third_prov_download.append(top3_data[2]['ave_download'])
        third_prov_upload.append(top3_data[2]['ave_upload'])


    df=pd.DataFrame({
        "tdhkn_number"          :   tdhkn_num_list,
        "tdhkn_kanji"           :   tdhkn_kanji_list,
        "tdhkn_yomi"            :   tdhkn_yomi_list,
        "ave_ping"              :   ave_ping_list,
        "ave_download"          :   ave_download_list,
        "ave_upload"            :   ave_upload_list,
        "first_prov"            :   first_prov_list,
        "first_prov_ping"       :   first_prov_ping,
        "first_prov_download"   :   first_prov_download,
        "first_prov_upload"     :   first_prov_upload,
        "second_prov"           :   second_prov_list,
        "second_prov_ping"      :   second_prov_ping,
        "second_prov_download"  :   second_prov_download,
        "second_prov_upload"    :   second_prov_upload,
        "third_prov"            :   third_prov_list,
        "third_prov_ping"       :   third_prov_ping,
        "third_prov_download"   :   third_prov_download,
        "third_prov_upload"     :   third_prov_upload
        })
    print(df)
    return df


def save_csv(data):
    data.to_csv(CSV_PATH+"todouhuken.csv")

main()