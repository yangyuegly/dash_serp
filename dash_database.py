"""queries and links tables"""
#from extraction import *
import importlib
import datetime
import sqlite3,urllib,  urllib.parse
import os, os.path,json
from dates_queries import datelist




conn = sqlite3.connect('dash_serp_database.db')
root_dir = '/Users/yueyang/Downloads/2019-processed-json'
queries= ['Bernie Sanders','Elizabeth Warren','Joe Biden','Kamala Harris']
query_page_converter = dict(zip(list(range(3)),queries))
c = conn.cursor()
conn.commit()
#---------create tables---------------
#no date datatype avaliable, thus stored date as text  "YYYY-MM-DD HH:MM:SS.SSS"


#---------create tables---------------

# c.execute("""CREATE TABLE stories(
#     url text PRIMARY KEY,
#     domain text,
#     title text,
#     query text,
#     snippet text,
#     UNIQUE(url)
# )""")
# conn.commit()


# c.execute("""CREATE TABLE appearances (
#     date text,
#     time text,
#     position int,
#     url text,
#     FOREIGN KEY (url) REFERENCES stories(url)
# )""") 
# conn.commit()



def insert_story(url,domain,title,query,snippet): 
    with conn:
        c.execute("""INSERT OR IGNORE INTO stories VALUES(:url, :domain, :title,:query,:snippet)""",{'url':url,'domain':domain,'title':title,'query':query,'snippet':snippet})


def insert_appearances(date,time,position,url): 
    with conn:
        c.execute("""INSERT OR IGNORE INTO appearances VALUES(:date, :time, :position, :url)""",{'date':date, 'time':time,'position':position,'url':url})




def update_time(url,date,time,new_date,new_time):
    with conn:
        c.execute("UPDATE appearances SET date=:new_date AND time=:new_time WHERE url=:url AND date=:date AND time=:time",{'url':url,'date':date,'time':time,'new_date':new_date,'new_time':new_time})


def batch_insert_stories(datelist):
    for date in datelist:
            try:
                with open(os.path.join(root_dir,date+".json"), 'r') as fr:
                    all_info = json.load(fr)
                    for page in range(3):
                        for item in range(len(all_info[str(page)])):
                            curr_url = all_info[str(page)][item]['url']
                            curr_query = query_page_converter[page]
                            curr_domain = urllib.parse.urlparse(curr_url).netloc
                            curr_snippet = all_info[str(page)][item]['snippet']
                            curr_position = page + 1 
                            curr_title = all_info[str(page)][item]['title']
                            insert_story(curr_url,curr_domain,curr_title,curr_query,curr_snippet)
            except FileNotFoundError:
                print(date)
                continue 
            

def batch_insert_appearances(datelist):
    for date in datelist:
            curr_date = date[:10]
            curr_time = '12pm'
            try:
                with open(os.path.join(root_dir,date+".json"), 'r') as fr:
                    all_info = json.load(fr)
                    for page in range(3):
                        for item in range(len(all_info[str(page)])):
                            curr_url = all_info[str(page)][item]['url']
                            curr_position = item + 1 
                            insert_appearances(curr_date,curr_time,curr_position,curr_url)
            except FileNotFoundError:
                print(date)
                continue 

#batch_insert_appearances(datelist)
#batch_insert_appearances(data)
#calculate_time(data)
