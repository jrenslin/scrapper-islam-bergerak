

# ------------------ Script to automatically archive Rappler articles ------------------ #

#### Import relevant modules
import os, subprocess, time, random
from datetime import datetime

#### Set essential variables
paginated = "http://islambergerak.com/page/"
start_page = 1
end_page = 38

#### Set directories
if not os.path.exists('islambergerak-archive'):
    os.makedirs('islambergerak-archive')

#### Functions
#def links_from_rss

for page_no in range(start_page, end_page):
    print ("\nFetching page " + str(page_no) + "\n")
    p = subprocess.Popen(
        ['curl', paginated + str(page_no) + "/"],
        stdout=subprocess.PIPE
    ).stdout.read().decode()

    p_parts = p.split('p-read-more" id=')
    p_parts[0] = ""

    for i in p_parts:
        if i.find(' rel="nofollow" title="Read More..."><i') > 1:
            link = i[:i.find(' rel="nofollow" title="Read More..."><i')]
            link = link[link.find('http'):].replace('"', '')
            print(link)
            os.system("curl " + link + " >> islambergerak-archive/" + link.replace(":", "").replace("/", "") + ".htm")
            time.sleep (random.randint(3, 15))
                

                
