from config import *
import requests

BASEURL ="https://minsoku.net/speeds/optical/prefectures/"


def main():
    tdhkn_list=get_tdhkn()
    name_list=create_file_name(tdhkn_list)

    for i in range (1,48):
        url=BASEURL+str(i)
        print(url)
        response = requests.get(url)
        with open(name_list[i-1], "w") as f:
            f.write(response.text)


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