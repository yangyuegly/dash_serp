# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime as dt
from dash.dependencies import Input, Output
import os
import sqlite3
import sys
import dash_table.DataTable
from dash_database import getUniqueURLs, getUniqueDomains,getUniqueDomains2
from dates_queries import datelist, querylist


sys.path.append(os.path.join(os.path.abspath("/Users/yigezhu/Desktop/SummerResearch18/SERP-Obeservatory/scripts")))
#from SERPStatistics import getResultDctFromData
#from query_analysis import getDateListFromDir, getTopNURL, getPosition, createDataFrameOverTime, getDateList, getAveragePosition
from app import app
# app = dash.Dash()
# server = app.server
# app.config.suppress_callback_exceptions = True
# 
# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
    
path = '/Users/yigezhu/Desktop/SummerResearch18/SERP-Obeservatory/SERP-results'
query = " "
default_df = pd.DataFrame()

#-----------sql commands---------
url_by_query = getUniqueURLs(query) 

startDate = datelist[1]

def run_query_withparms(sql,connect):
    df = pd.read_sql_query(sql , connect)
    return df    
#---dataframes----------
#df = run_query_withparms(url_by_query,conn1)
#df2 = run_query_withparms(url_by_query,conn2)


       

def generate_table(df, max_rows=10):
    df[' index'] = range(1, len(df) + 1)
    return dash_table.DataTable(
    id="-table",
    columns=[
        {'name': i, 'id': i, 'deletable': True} for i in sorted(df.columns)
    ],
    #data=df.to_dict('records'),
    page_current=0,
    page_size=100,
    page_action='custom',
    sort_action='custom',
    sort_mode='single',
    sort_by=[]
)

    
    # html.Table(
    #     # Header
    #     [html.Tr(
    #         [html.Th(html.Div(col)) for col in dataframe.columns]
    #     )]
    #     +#Body
    #     [html.Tr([
    #         html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
    #     ]) for i in range(min(len(dataframe), max_rows))]
    #     ,
    #     id = query + "-table",
    # ))


    
def generate_lineGraph(df, query):
    """the line graph showing the changes in the top10 url"""

    return dcc.Graph(id = query + "-line-graph", 
    
    style = {'height': 600, 'width': 1300},
    
    figure = {
    'data': [go.Scatter(
            x=df.columns[1:], #dates
            y=df.ix[df.index[i]][1:], #position
            name = df['Title'][i])
              for i in range(len(df.index))],
              
    "layout": {
            "title": "Changes in the Positions of Individual Result"}
    })


#commented
# def generate_rankingTable(query, start_dateDir,end_dateDir ):
 
#     rankingResult = getResultDctFromData(start_dateDir, end_dateDir)
#     try:
#         rankingList = rankingResult[query]['ranking']
#         titles = [item[0] + "\n" + item[1][1] for item in rankingList]
#         changes = [item[1][0] for item in rankingList]
#         # url = [item[1][1] for item in rankingList]
            
#         return dcc.Graph(id = query + "-ranking-table", 
#         style = {'height': 600},
#         figure = {
#         'data': [ go.Table( type = 'table',
#         columnorder = [1,3],
#         columnwidth = [200, 30],
#         header=dict(values=['Title', 'Change'],
#                     line = dict(color='#7D7F80'),
#                     fill = dict(color='#a1c3d1'),
#                     align = ['left'] * 5),
                    
#         cells=dict(values=[titles, changes],
#                 line = dict(color='#7D7F80'),
#                 fill = dict(color='#EDFAFF'),
#                 align = ['left'] * 5))
#                 ]})
#     except:
#         return dcc.Graph(id = query + "-ranking-table")
#         print ("No data collection on selected date")

def generate_boxPlot(df, query):
    
    data = []
    for url in df.index:
        data.append(go.Box(
            y = df.ix[url][1:],
            name = df.ix[url][0],
            boxpoints = "all",
            marker = {'line': {'width':0}, 'symbol': 'octagon', 'size':'4'}
            ))
    
    return dcc.Graph(id = query + "-box-plot", 
    style = {'height': 400, 'width': 1200}, figure = {
    'data': data, 
    "layout": {"title": "The Range of Position for Each Result",
                'y-axis': {"title": "position in SERP page"}
                }
        }
    )

#-------------Turn URLs into hyperlinks----
def generate_hyperlinks(df):
    rows = []
    hyper_link_col_list = ['url']
    for i in range(len(df)):
        row = {}
        for col in df.columns:
            value = df.iloc[i][col]
            if col in hyper_link_col_list:
                row[col]=html.Td(html.A(href=value, children=value))
            else:
                row[col]=value
        rows.append(row)
    df = pd.DataFrame(rows)
    return df

#--------------DASH LAYOUT---------------
def generate_layout(query,connect):
    domain_df = getUniqueDomains(query)
    stories_df = run_query_withparms(getUniqueURLs(query),connect)
#    stories_df = generate_hyperlinks(stories_df)
    layout = html.Div([
    html.Div([
        html.Div(id='individual-page-content'),
        html.Br(),
        dcc.Link('Go back to home', href='/overview_app'),
    ]),
    html.Div([
        html.H2(id = 'page-title', children= query, className = "twelve columns"
        , style = {'fontFamily': 'Titillium Web', 'text-align': 'center'}),

        html.H5(id = 'page-stats', children= query, className = "twelve columns"
        , style = {'fontFamily': 'Titillium Web', 'text-align': 'center'})
        ], 
        className = "row"),
        
    html.Br(), html.Br(),
        
    html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt.strptime(datelist[0], "%Y-%m-%d-%I%p"),
       # max_date_allowed=dt.strptime(datelist[-1], "%Y-%m-%d-%I%p"),
        initial_visible_month= dt.today().date(),
        end_date=dt.today().date(),
        start_date_placeholder_text='MM Do, YY'
    ),
    html.Div(id='output-container-date-picker-range', className = "two columns")
    ], className = "row"),
    
    html.Br(),html.Br(),    
    
    html.Div([dcc.RadioItems( id = 'radio-items',
    options=[
        {'label': 'Box Plot', 'value': 'box'},
        {'label': 'Line Graph', 'value': 'line'}
    ],
    value=None,
    labelStyle={'display': 'inline-block'}
    )
    ], className = 'row'),
            
    #commented
    #  html.Div(id = 'change-in-ranking-graph', children = [
    #     html.Div([
    #         generate_boxPlot(df, query)
    #     ], className="nine columns"),
    # ], className="row", style = {'width': '100%'}),
    
    html.Br(), html.Br(),
    
    html.Div([
        html.Div(children = html.H6("The Position of Each Result in Selected Date")
        ,style = {'fontFamily': 'Titillium Web'}),  
        #generate_table(stories_df)
        ], className = "row"),
    dash_table.DataTable(
    id="domain-table",
    columns=[
        {'name': i, 'id': i, 'deletable': True} for i in sorted(domain_df.columns)
        if i!='id'
    ],
    page_current=0,
    page_size=5,
    page_action='custom',
    sort_action='custom',
    sort_mode='single',
    sort_by=[],
    editable=True,
    row_selectable="multi",
    filter_action="native",
    row_deletable=True,
    selected_rows=[],
    style_cell={
        'whiteSpace': 'no-wrap',
        'overflow': 'scroll',
        'textOverflow': 'ellipsis',
        'maxWidth': 200,
    },
    style_table={'overflowX': 'scroll'}
    
),
html.Div(id='datatable-row-ids-container'),

 dash_table.DataTable(
    id="-table",
    columns=[
        {'name': i, 'id': i, 'deletable': True} for i in sorted(stories_df.columns)
    ],
    page_current=0,
    page_size=20,
    page_action='custom',
    sort_action='custom',
    sort_mode='single',
    sort_by=[],
    
    style_cell={
        'whiteSpace': 'no-wrap',
        'overflow': 'scroll',
        'textOverflow': 'ellipsis',
        'maxWidth': 400,
    },
    style_table={'overflowX': 'scroll'}
    
),
    html.Br(), html.Br(),    

    #commented 
    # html.Div([  
    #     html.Div(children = 
    #     html.H6("Here are the results with the most total calculated change..."),
    #     style = {'fontFamily': 'Titillium Web'}),
    #     generate_rankingTable(query, os.path.join(path, datelist[0]), 
    #     os.path.join(path, datelist[-1]))], className = "row")

    
    ])
    return layout

# #---------------Interactive Callbacks--------------
# @app.callback(Output('change-in-ranking-graph', 'children'),
#               [Input('radio-items', 'value')])
# def update_graph_choice(choice):
#     if choice == 'line':
#         return [
#         html.Div([
#             generate_lineGraph(df, query), 
#         ], style = {'height':'800'}, className="nine columns"),
#     ]
# 
#     else:
#         return [
#         html.Div([
#             generate_boxPlot(df, query)
#         ], className="nine columns"),
#     ]

@app.callback(
    Output("-table", 'data'),
    [Input("-table", "page_current"),
     Input("-table", "page_size"),
     Input("-table", 'sort_by')])
def update_table(page_current, page_size, sort_by):
    if query in querylist:
            connect = sqlite3.connect('focus_database.db')
    else:
            connect = sqlite3.connect('dash_serp_database.db')
    stories_df = run_query_withparms(getUniqueURLs(query),connect)
   # stories_df = generate_hyperlinks(stories_df)
    if len(sort_by):
        dff = stories_df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )

    else:
        # No sort is applied
        dff = stories_df
    # print(dff.iloc[
    #     page_current*page_size:(page_current+ 1)*page_size
    # ].to_dict('records'))
    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

@app.callback(
    Output("domain-table", 'data'),
    [Input("domain-table", "page_current"),
     Input("domain-table", "page_size"),
     Input("domain-table", 'sort_by')])
def update_table(page_current, page_size, sort_by):
    if query in querylist:
        domain_df = getUniqueDomains2(query)
    else:
        domain_df = getUniqueDomains(query)
   # stories_df = generate_hyperlinks(stories_df)
    if len(sort_by):
        dff = domain_df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
        default_df = dff
        default_df['id']=default_df['domain']
        default_df.set_index('id', inplace=True, drop=False)

    else:
        # No sort is applied
        dff = domain_df
        default_df = dff
        default_df['id']=default_df['domain']
        default_df.set_index('id', inplace=True, drop=False)

    # print(dff.iloc[
    #     page_current*page_size:(page_current+ 1)*page_size
    # ].to_dict('records'))
    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

@app.callback(Output('output-container-date-picker-range', 'children'),
    [Input('my-date-picker-range', 'start_date'),
      Input('my-date-picker-range', 'end_date')])
      
def update_output(start_date, end_date):
    string_prefix = 'Please pick a time range for the data you want to see.\n '
    if start_date is not None:
        #print(start_date)
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = 'You have selected ' + 'start date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'end date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

@app.callback(
    Output('datatable-row-ids-container', 'children'),
    [Input('domain-table', 'derived_virtual_row_ids'),
     Input('domain-table', 'selected_row_ids'),
     Input('domain-table', 'active_cell')])
def update_graphs(row_ids, selected_row_ids, active_cell):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    default_df['id']=default_df['domain']
    selected_id_set = set(selected_row_ids or [])

    if row_ids is None:
        dff = default_df
        # pandas Series works enough like a list for this to be OK
        row_ids = default_df['id']
    else:
        dff = default_df.loc[row_ids]

    active_row_id = active_cell['row_id'] if active_cell else None

    colors = ['#FF69B4' if id == active_row_id
              else '#7FDBFF' if id in selected_id_set
              else '#0074D9'
              for id in row_ids]

    return [
        dcc.Graph(
            id=column + '--row-ids',
            figure={
                'data': [
                    {
                        'x': dff['domain'],
                        'y': dff[column],
                        'type': 'bar',
                        'marker': {'color': colors},
                    }
                ],
                'layout': {
                    'xaxis': {'automargin': True},
                    'yaxis': {
                        'automargin': True,
                        'title': {'text': column}
                    },
                    'height': 250,
                    'margin': {'t': 10, 'l': 10, 'r': 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ['pop', 'lifeExp', 'gdpPercap'] if column in dff
    ]

# @app.callback(
#     dash.dependencies.Output(query + '-table', 'figure'),
#     [dash.dependencies.Input('my-date-picker-range', 'start_date'),
#       dash.dependencies.Input('my-date-picker-range', 'end_date')])
#      
# def update_graph_table(start_date, end_date):
#     if start_date is not None and end_date is not None:
#         start_date = dt.strptime(start_date, '%Y-%m-%d')
#         end_date = dt.strptime(end_date, '%Y-%m-%d')
#         
#         dateListSelected = getDateList(start_date, end_date)
#         startDate = dateListSelected[0]
#         topNURL = getTopNURL(query, startDate,10)
#         if topNURL != None:
#             topNList = getPosition(dateListSelected, topNURL,query)
#             df = createDataFrameOverTime(topNList, dateListSelected)
#         figure = {
#         'data': [go.Table(
#             columnorder = range(len(df.columns)),
#             columnwidth = [250] + [80] * (len(df.columns)-1),
#             header = dict(values = list(df.columns),
#                     fill = dict(color='#C2D4FF')),
#             cells = dict(values = [df[col] for col in df.columns],
#             fill = dict(color='#F5F8FF'),
#             height = 40,
#             align = ["left"] + ["center"] * (len(df.columns)-1))
#             )]
#         }
#         return figure
# #commented
# @app.callback(Output(query + '-table', 'children'),
#     [Input('my-date-picker-range', 'start_date'),
#     Input('my-date-picker-range', 'end_date')])
      
# def update_graph_table(start_date, end_date):
#     print('reached')
#     if start_date is not None and end_date is not None:
#         start_date = dt.strptime(start_date, '%Y-%m-%d')
#         end_date = dt.strptime(end_date, '%Y-%m-%d')
#         print(end_date)
#         dateListSelected = pd.date_range(start=start_date, end=end_date)
#         startDate = dateListSelected[0]
#         # topNURL = getTopNURL(query, startDate,10)
#         # if topNURL != None:
#         #     topNList = getPosition(dateListSelected, topNURL,query)
#         #     df = createDataFrameOverTime(topNList, dateListSelected)
#         dateListSelected_str = [c.strftime('%Y-%m-%d') for c in dateListSelected]
#         print(dateListSelected_str)
#         print('reached')
#         stories_df = run_query_withparms(url_by_query)
#         stories_df = generate_hyperlinks(stories_df)
#         print(url_by_query)
#         return generate_table(stories_df)
#     else:
#         return generate_table(stories_df)
#commented
# @app.callback(
#     Output('change-in-ranking-graph', 'children'),
#     [Input('my-date-picker-range', 'start_date'),
#       Input('my-date-picker-range', 'end_date'),
#       Input('radio-items', 'value')])
      
# def update_graph_line_box(start_date, end_date, radio_choice):
#     if start_date is not None and end_date is not None:
#         start_date = dt.strptime(start_date, '%Y-%m-%d')
#         end_date = dt.strptime(end_date, '%Y-%m-%d')
        
#         dateListSelected = getDateList(start_date, end_date)
#         startDate = dateListSelected[0]
#         topNURL = getTopNURL(query, startDate,10)
#         if topNURL != None:
#             topNList = getPosition(dateListSelected, topNURL,query)
#             df = getAveragePosition(createDataFrameOverTime(topNList, dateListSelected))
            
        
#         if radio_choice == 'line':    
#             return [html.Div([
#                 generate_lineGraph(df, query), 
#             ], style = {'height':'800'}, className="nine columns")]
#         else:
#             return [html.Div([
#                 generate_boxPlot(df, query)
#             ], className="nine columns"),
#         ]
#     else:
#         generate_boxPlot(df, query)

# @app.callback(
#     Output(query + "-ranking-table", 'figure'),
#     [Input('my-date-picker-range', 'start_date'),
#       Input('my-date-picker-range', 'end_date')])
     
# def update_ranking_table(start_date, end_date):
#     if start_date is not None and end_date is not None:
#         # start_date = dt.strftime(start_date, '%d-%m-%Y')
#         # end_date = dt.strftime(end_date, '%d-%m-%Y')
        
#         start_dateDir = os.path.join(path, start_date, query)
#         end_dateDir = os.path.join(path, end_date, query)     
                
#         return generate_rankingTable(query, start_dateDir,end_dateDir )
 

# if __name__ == '__main__':
    # app.run_server(debug=True)
