from config import *
import bs4

def main():
    tdhkn_list=get_tdhkn()
    name_list = create_file_name(tdhkn_list)

    soup = bs4.BeautifulSoup(open(name_list[0],encoding = 'utf-8'),'html.parser')
    target=soup.find_all(attrs={"class":"mb-xxxs"})
    print(type(str(target)))



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