"""queries and links tables"""
#from extraction import *
import importlib
import datetime
import sqlite3,urllib,  urllib.parse
import os, os.path,json
from dates_queries import datelist,querylist,datelist2
import pandas as pd



conn = sqlite3.connect('dash_serp_database.db')
conn2 = sqlite3.connect('focus_database.db')
#root_dir = '/Users/yueyang/Downloads/2019-processed-json'
root_dir = '/Users/yueyang/Downloads/serp-626-75-json'
#queries= ['Bernie Sanders','Elizabeth Warren','Joe Biden','Kamala Harris']
#query_page_converter = dict(zip(list(range(4)),queries))
query_page_converter2= dict(zip(list(range(len(querylist))),querylist))
c = conn.cursor()
c2 = conn2.cursor()
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
#     first_appeared_on text
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


# c2.execute("""CREATE TABLE stories(
#     url text PRIMARY KEY,
#     domain text,
#     title text,
#     query text,
#     snippet text,
#     first_appeared_on text,
#     UNIQUE(url)
# )""")
# conn2.commit()

# c2.execute("""CREATE TABLE appearances (
#     date text,
#     time text,
#     position int,
#     url text,
#     FOREIGN KEY (url) REFERENCES stories(url)
# )""") 
# conn2.commit()

# c.execute("""CREATE TABLE domains(
#     domain text,
#     frequency int,
#     UNIQUE(domain)
# )""")
# # conn.commit()
# c.execute("ALTER TABLE domains ADD COLUMN query text")
# conn.commit()

def insert_story(url,domain,title,query,snippet,first_appeared_on): 
    with conn2:
        c2.execute("""INSERT OR IGNORE INTO stories VALUES(:url, :domain, :title,:query,:snippet,:first_appeared_on)""",{'url':url,'domain':domain,'title':title,'query':query,'snippet':snippet,'first_appeared_on':first_appeared_on})


def insert_appearances(date,time,position,url): 
    with conn:
        c.execute("""INSERT OR IGNORE INTO appearances VALUES(:date, :time, :position, :url)""",{'date':date, 'time':time,'position':position,'url':url})




def update_time(url,date,time,new_date,new_time):
    with conn:
        c.execute("UPDATE appearances SET date=:new_date AND time=:new_time WHERE url=:url AND date=:date AND time=:time",{'url':url,'date':date,'time':time,'new_date':new_date,'new_time':new_time})

def count_total_rows_candidates(query):
    conn = sqlite3.connect('dash_serp_database.db')
    c = conn.cursor()
    with conn:
        c.execute("SELECT count(*) FROM stories WHERE query='{}'".format(query))
        return str(c.fetchone()[0])
    
def count_total_rows_focus_group(query):
    conn2 = sqlite3.connect('focus_database.db')
    c2 = conn2.cursor()
    with conn2:
        c2.execute("SELECT count(*) FROM stories WHERE query='{}'".format(query))
        return str(c2.fetchone()[0])

def get_domains_by_query(query):
    conn = sqlite3.connect('dash_serp_database.db')
    c = conn.cursor()
    with conn:
        c.execute("SELECT domain FROM stories WHERE query='{}'".format(query))
        return c.fetchall()

def get_domains_by_query2(query):
    conn2 = sqlite3.connect('dash_serp_database.db')
    c2 = conn.cursor()
    with conn2:
        c2.execute("SELECT domain FROM stories WHERE query='{}'".format(query))
        return c2.fetchall()

def update_first_appeared_on(url,date):
    with conn:
        c.execute("UPDATE stories SET first_appeared_on=:first_appeared_on WHERE url=:url",{'url':url,'first_appeared_on':date})

def batch_insert_stories(datelist):
    for date in datelist:
            print(date)
            curr_date = date[:10]
            try:
                with open(os.path.join(root_dir,date+".json"), 'r') as fr:
                    all_info = json.load(fr)
                    for key in all_info.keys():
                        for each in querylist:
                            if each in key:
                                curr_query = each
                        for item in range(len(all_info[key])):
                            curr_url = all_info[key][item]['url']
                            curr_domain = urllib.parse.urlparse(curr_url).netloc
                            curr_snippet = all_info[key][item]['snippet']
                            curr_title = all_info[key][item]['title']
                            curr_first_appeared_on = curr_date
                            insert_story(curr_url,curr_domain,curr_title,curr_query,curr_snippet,curr_first_appeared_on)
            except FileNotFoundError:
                print(date)
                continue 
            
def batch_update_date(datelist):
    appearred = []
    for date in datelist:
            curr_date = date[:10]
            try:
                with open(os.path.join(root_dir,date+".json"), 'r') as fr:
                    all_info = json.load(fr)
                    for page in range(3):
                        for item in range(len(all_info[str(page)])):
                            curr_url = all_info[str(page)][item]['url']
                            if curr_url not in appearred:
                                update_first_appeared_on(curr_url,curr_date)
                                appearred.append(curr_url)
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


#--------SQL commands ---------
def getUniqueDomains(query):
    conn = sqlite3.connect('dash_serp_database.db')
    c = conn.cursor()
    with conn:
        c.execute("SELECT domain, count(*) FROM stories WHERE query='{}' GROUP BY domain".format(query))
        names = [ x[0] for x in c.description]
        rows = c.fetchall()
    df = pd.DataFrame(rows, columns=names)
    return df 

def getUniqueDomains2(query):
    conn = sqlite3.connect('focus_database.db')
    c = conn.cursor()
    with conn:
        c.execute("SELECT domain, count(*) FROM stories WHERE query='{}' GROUP BY domain".format(query))
        names = [ x[0] for x in c.description]
        rows = c.fetchall()
    df = pd.DataFrame(rows, columns=names)
    return df 

def getUniqueURLs(query):
    return "SELECT url, title, snippet,first_appeared_on FROM stories WHERE query='{}'".format(query)

def getAppearancesWithURL(url):
    return "SELECT * FROM appearances WHERE url='{}'".format(url)

def getAppearancesWithURL(url):
    return "SELECT * FROM appearances WHERE url='{}'".format(url)




#batch_insert_stories(datelist2)

#print((getUniqueDomains('Bernie Sanders')))