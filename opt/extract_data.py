from config import *
import bs4
import re
from icecream import ic

def main():
    ave_list=[]
    #　ファイル名の読み込み
    tdhkn_list=get_tdhkn()
    name_list1 = create_file_name1(tdhkn_list)

    for html_name in name_list1:
        ave_list.append(extract_ave(html_name))
        top3_list = create_file_name2(html_name)
        for top3 in top3_list:
            extract_ave(top3)







def get_tdhkn():
    with open(TODOUHUKEN) as f:
        tdhkn_list = [s.rstrip() for s in f.readlines()]
    return tdhkn_list

def create_file_name1(tdhkn_list):
    name_list=[]
    for line in tdhkn_list:
        i,tdhkn_kanji,tdhkn = line.split("\t")
        name_list.append(HTML_PATH+str(i)+"_"+str(tdhkn)+".html")
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

main()