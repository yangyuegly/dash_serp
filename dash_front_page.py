import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import app
from app import app
import sqlite3
import os
import pandas as pd
import sys
sys.path.append(os.path.join(os.path.abspath("/Users/yigezhu/Desktop/SummerResearch18/SERP-Obeservatory")))
#import UniqueLinks
#import Top10
import json


# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
# overview.config.suppress_callback_exceptions = True

news_topics =  ['Bernie Sanders','Elizabeth Warren','Joe Biden','Kamala Harris']
focus_group_topics = []

path = '/Users/yigezhu/Desktop/SummerResearch18/SERP-Obeservatory/manually_added-results'

def getAverageUniqueLinks(cat):
    dateList = UniqueLinks.getDateListFromDir(path)
    count = 0
    for query in cat:
        count += len(UniqueLinks.getUniqueResult(query, dateList))
    return float(count / len(cat))






#-----------------------Database Connection -------------------------

def run_query_withparms(sql):
    conn = sqlite3.connect('dash_serp_database.db')
    df = pd.read_sql_query(sql , conn)
    return df    

#-----------------------DataFrame Creation-------------

#------------Generate Table with Data Frame------------

def generate_table(dataframe, max_rows=10):
    return html.Table(
# Header
    [html.Tr([html.Th(col) for col in dataframe.columns])] +
    # Body
    [html.Tr([
        html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
    ]) for i in range(min(len(dataframe), max_rows))]
)


#-----------------------Layout-------------------------

sql2 = ('SELECT * FROM stories')
df = run_query_withparms(sql2)

layout = html.Div([

    html.Div([html.H1("Welcome to the SERP Observatory"),
    html.H6("By Wellesley CRED lab")], style = 
    {'fontFamily': 'Titillium Web', 'text-align': 'center'}),
    html.Br(),
    
    #explanation paragraph
    html.Textarea(id = 'introduction', children = "\tWith the aim to observe \
changes in SERPs and understand SEO-based manipulation techniques, Wellesley\
 CRED lab implement the SERP observatory by collecting the SERPs for a \
series of queries of different kinds on a daily basis.",
    style = {'width':'800px', 'height': '90px', 'backgroundColor': 'FloralWhite',
    'color': 'black', 'border':'none', 'padding': '2%', 'margin': 'auto',
    'display': 'block', 'fontFamily': 'Dosis', 'fontSize': '17'}),
    
    html.Br(),
    html.Div(
        [html.H6("Long-standing Topics"),]+
        [html.Div([
            dcc.Link(query, href = '/apps/page_app/'+ query), 
            html.Br()
            ]) for query in focus_group_topics],
        
        className = 'four columns'),

        html.Div([
        
        html.Div(
        [html.H6("2020 Election Candidates"),]+
        [html.Div([
            dcc.Link(query, href = '/apps/page_app/'+ query), 
            html.Br()
            ]) for query in news_topics],
        
        className = 'four columns'),
        
        # html.Div(
        # [html.H6("Topics in the News")] +
        # [html.Div([
        #     dcc.Link(query, href = '/apps/page_app/'+ query), 
        #     html.Br()
        #     ]) for query in news_topics],
        
        # className = 'four columns'),
        
        # html.Div(
        # [html.H6("Opinion-based Queries")] +
        # [html.Div([
        #     dcc.Link(query, href = '/apps/page_app/'+ query), 
        #     html.Br()
        #     ]) for query in opinion_topics]+ 
            
        # [html.Br(), html.H6("Question-based Queries")] +
        # [html.Div([
        #     dcc.Link(query, href = '/apps/page_app/'+ query), 
        #     html.Br()
        #     ]) for query in question_topics],
        
        # className = 'four columns')
    ], className = 'row', style = {'text-align': 'center', 'fontFamily': 'Titillium Web'}),
    
    # html.Div([
    #     html.Div([dcc.Graph(id = 'unique_links_bar',
    #     figure = {
    #     'data': [go.Bar(
    #         x=['Long-standing Topics', 'Topics in the News', 'Opinion-based Queries',
    #         "Question-based Queries"],
    #         y=[getAverageUniqueLinks(news_topics), getAverageUniqueLinks(long_standing_topics),
    #         getAverageUniqueLinks(opinion_topics), getAverageUniqueLinks(question_topics)],
    #         )],
    #     "layout": {
    #         "title": "Number of Unique Links"}
    #         })], className = 'four columns')
    # ],className = 'row')
    
])






if __name__ == '__main__':
    app.run_server(debug=True)