from config import *
import bs4
import re
from icecream import ic

def main():
    ave_list=[]
    #　ファイル名の読み込み
    tdhkn_list=get_tdhkn()
    name_list = create_file_name(tdhkn_list)
   
    for html_name in name_list:
        ave_list.append(extract_ave(html_name))
    print(ave_list)


def extract_ave(html_name):
    # ファイルから平均ping，平均ダウンロード速度，平均アップロード速度，
    # ランキング上位3件の事業者名，平均の抽出
    ave={}
    soup = bs4.BeautifulSoup(open(html_name,encoding = 'utf-8'),'html.parser')
    element=soup.find(attrs={"class":"mb-xxxs"})
    if element:
        spans=element.find_all('span', {"class": "text-bold"})
        # ic(spans)
        if len(spans):
            ping_texts = [span.get_text(strip=True) for span in spans]
            matchs=[]
            pattern1 = r'^([0-9]+\.[0-9]+)ms$'
            pattern2 = r'^([0-9]+\.[0-9]+)Mbps$'
            matchs.append(re.search(pattern1, ping_texts[0]))
            matchs.append(re.search(pattern2, ping_texts[1]))
            matchs.append(re.search(pattern2, ping_texts[2]))
            # ic(matchs)
            if len(matchs):
                print(html_name.split("/")[-1])
                ave_ping_value = matchs[0].group(1)
                print(f"平均Ping値: {ave_ping_value} ms")
                ave_download_value = matchs[1].group(1)
                print(f"平均ダウンロード速度: {ave_download_value} ms")
                ave_upload_value = matchs[2].group(1)
                print(f"平均アップロード速度: {ave_upload_value} ms")
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

def get_tdhkn():
    with open(TODOUHUKEN) as f:
        tdhkn_list = [s.rstrip() for s in f.readlines()]
    return tdhkn_list

def create_file_name(tdhkn_list):
    name_list=[]
    for line in tdhkn_list:
        i,tdhkn_kanji,tdhkn = line.split("\t")
        name_list.append(HTML_PATH+str(i)+"_"+str(tdhkn)+".html")
    return name_list

main()