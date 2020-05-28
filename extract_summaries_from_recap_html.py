import os, sys
import datetime
import time
import codecs
import re, datetime
import argparse
from bs4 import BeautifulSoup
import urllib2
from tqdm import tqdm
import glob
import random 

# def setProxy():
#     proxy_list = [
#         "50.206.25.106:80",
#         "50.206.25.111:80",
#         "50.206.25.107:80",
#         "50.206.25.108:80",
#         "50.206.25.109:80",
#         "50.206.25.110:80",
#         "50.206.25.104:80",
#         "68.188.59.198:80",
#         "71.13.131.142:80",
#         "52.179.231.206:80",
#         "54.156.164.61:80",
#         "12.139.101.100:80",
#         "108.74.113.180:80",
#         "68.185.57.66:80",
#         "12.139.101.98:80",
#         "103.105.49.53:80"]
#     ip = random.choice(proxy_list)
#     proxy = {'http':'http://{0}'.format(ip)}
#     print(proxy)
#     proxy_handler = urllib2.ProxyHandler(proxy)
#     opener = urllib2.build_opener(proxy_handler)
#     urllib2.install_opener(opener)

def extract_summary(input_filenames, output_folder):
    downloaded_files = glob.glob(os.path.join(output_folder, "*"))
    for filename in tqdm(input_filenames):
        # output file
        out_file = os.path.join(output_folder, filename)
        if out_file in downloaded_files:
            continue
        
        game_id = filename[:filename.index("_")]
        recap_url = "http://www.espn.com/mlb/recap?"+game_id
            
        try:
            response = urllib2.urlopen(recap_url)
        except urllib2.HTTPError, e:
            if e.getcode()/100 == 5:
                print 'error3 ',e.getcode()
                continue
            else:
                raise
        html = response.read().decode('utf-8', 'ignore')
        with codecs.open(output_folder + filename, "w+", "utf-8") as f:
            f.write(html)
        soup = BeautifulSoup(html,"lxml")
        article = soup.find('div', attrs={'class': 'article-body'})
        if article == None:
            return
        paras = article.find_all('p')
        # save a file
        with codecs.open(out_file, "w+", "utf-8") as f:
            for para in paras:
                f.write(para.get_text().replace("\n"," "))
                f.write("\n")
        f.close()
        time.sleep(1)  # delay between url request


parser = argparse.ArgumentParser(description='Extract summaries from html')
parser.add_argument('-recaps',type=str,
                    help='file containing the names of recaps')
parser.add_argument('-output_folder',type=str,
                    help='output folder')
args = parser.parse_args()

recaps = args.recaps
output_folder = args.output_folder
with codecs.open(recaps) as f:
    content = f.readlines()

input_filenames = [x.strip() for x in content]
extract_summary(input_filenames, output_folder)
