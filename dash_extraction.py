#!/usr/local/bin/python3.6

from datetime import datetime
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import json
from dates_queries import datelist, datelist2
import re
import urllib.parse
from urllib.parse import urlparse
import cProfile


root_dir = '/Users/yueyang/Downloads/June26-July5'
# root_dir = '/Users/daphka/Desktop/SERPs to compare/emma-in-virginia'


def get_query_folders(root_dir, today):
    """Returns a list of the recently added query folders (of HTMLs) that match the given query each day"""

    pat = r'(\d*-\d*-\d*-\d\s\s)' #regex for the folder of the type that the SERPs are saved in
    query_folder_list = []

    for f in os.listdir(root_dir):
        #match = re.search(pat, f) #search for the format in the regex in the folder name
        #if match:
            #dir_name = match.group(1) #extract query term
        #   date = match.group(1) #extract date

        if os.path.isdir(os.path.join(root_dir, f)) and (f == today):
            query_folder_list.append(os.path.join(root_dir, f))
        else:
            pass
    if not query_folder_list: #if empty, no htmls were collected for that query term for that day
        print(" does not match a recent dir with same query name in {0}".format(root_dir))

    return query_folder_list


def get_html_files_for_candidates(f_name):
    """Returns a list of html pages/files from a given folder"""
    candidates = ['Joe Biden','Kamala Harris','Elizabeth Warren','Bernie Sanders']
    candidates_files = ['{}.html'.format(candidate) for candidate in candidates]
    results = []
    files = sorted([os.path.join(f_name, f) for f in os.listdir(f_name) if os.path.isfile(os.path.join(f_name, f))]) #extra check if is file unnecessary
    for file in files:
        for c in candidates_files:
            if c in file:
                results.append(file)
    print(results)
    return results

def get_html_files(f_name):
    """Returns a list of html pages/files from a given folder"""
    files = sorted([os.path.join(f_name, f) for f in os.listdir(f_name) if os.path.isfile(os.path.join(f_name, f))]) #extra check if is file unnecessary
    return files

def get_recently_added_htmls(folder_list):
    return list(map(get_html_files, folder_list))



def find_rc(soup):
    """A function to find "rc" elements (i.e. ordinary search results)"""
    lst = soup.find_all('div', attrs={"class":"rc"})
    if len(lst)==0:
        return None

    sites = []
    for elt in lst:
        try:
            #class r is just url and title
            url = elt.find("h3", attrs={"class":"r"}).find("a").get("href")
            title = elt.find("h3", attrs={"class":"r"}).get_text()

        except:
            url = elt.find("div", attrs={"class":"r"}).find("a").get("href")
            title = elt.find("div", attrs={"class":"r"}).find("h3", attrs={"class":"LC20lb"}).get_text()


        snippet1 = elt.find("div", attrs={"class":"s"}) #text from page
        snippet2 = elt.find("div", attrs={"class":"P1usbc"}) #extra text

        #we're grabbing one or the other or showing missing message
        if snippet1 != None and snippet1.find("span", attrs={"class":"st"}) != None:
            snippet = snippet1.find("span", attrs={"class":"st"}).get_text()
        elif snippet2 != None:
            snippet = snippet2.get_text()
        else:
            snippet = ""
            # print("------------")
            # print("MISSING snippet -", url, title)
            # print("------------")

        sites.append({'url':url, 'title': title, 'snippet': snippet})

    return sites



def get_results_from_page(files):
    result_dict = defaultdict(list)

    for i, f in enumerate(files):
        with open(f, 'rb') as f:
            html = f.read()
            #.decode('utf-8')
            soup = BeautifulSoup(html, "html5lib")
            site_lst = find_rc(soup)
            print(f)
            result_dict['{}'.format(str(f).replace('.html',''))] = site_lst
            

    return result_dict


def save_to_file(result, date):
    """Writes results (dict of titles and urls of each html page) to a json file."""
    try:
        os.mkdir('/Users/yueyang/Downloads/serp-626-75-json', mode=0o744)
    except FileExistsError:
        # print('Directory already exists.')
        pass

    filename = '{0}.json'.format(date) #datetime.today().strftime('%m-%d-%Y'), query)
    with open(os.path.join('/Users/yueyang/Downloads/serp-626-75-json', filename), 'w') as f:
        json.dump(result, f, indent=4)
        print('Saved search results to {0}'.format(f.name))


if __name__ == '__main__':
    for each_date in datelist2:
         query_folders = get_query_folders(root_dir, each_date) #get the folders containing htmls
         htmls = get_recently_added_htmls(query_folders) #extracting html files from the folders 
         result_dict = list(map(get_results_from_page, htmls)) #parsing html files into dictionaries
         if not result_dict:
             print("Empty result, {0}, won't be written to json file.".format(result_dict))
         else: 
             save_to_file(result_dict[0], each_date)

    #cProfile.run('re.compile("foo|bar")', 'restats')
