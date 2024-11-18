from config import *
import requests
import bs4
from icecream import ic
import os

BASEURL1 ="https://minsoku.net/speeds/optical/prefectures/"
BASEURL2 ="https://minsoku.net"

def main():
    tdhkn_list=get_tdhkn()
    name_list1=create_file_name1(tdhkn_list)

    for i in range (1,48):
        url=BASEURL1+str(i)
        if os.path.exists(name_list1[i-1]):
            pass
        else:
            response = requests.get(url)
            with open(name_list1[i-1], "w") as f:
                f.write(response.text)
                ic(name_list1[i-1])

    for html_name in name_list1:
        name_list2=create_file_name2(html_name)
        soup = bs4.BeautifulSoup(open(html_name,encoding = 'utf-8'),'html.parser')
        element1=soup.find(attrs={"class":"mb-xxs mt-22"})
        element2=element1.find_all('a', attrs={'class': 'text-bold'})
        for i in range (1,4):
            url = BASEURL2+element2[i-1].get("href")
            ic(url)
            response=requests.get(url)
            with open(name_list2[i-1], "w") as f:
                f.write(response.text)
            ic(name_list2[i-1])





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

def extract_href(response):
    soup = bs4.BeautifulSoup(open(response,encoding = 'utf-8'),'html.parser')
    element1=soup.find(attrs={"class":"mb-xxs mt-22"})
    element2=soup.find_all('a', attrs={'class': 'text-bold'})
    # ic(element2[0].get("href"))
    return element2.get("herf")

main()