import os
from dotenv import load_dotenv

def create_file_name(tdhkn_list):
    #   .envを有効化
    load_dotenv()

    name_list=[]
    for line in tdhkn_list:
        i,tdhkn_kanji,tdhkn = line.split("\t")
        name_list.append(HTML_PATH+str(i)+"_"+str(tdhkn)+".html")
    return name_list