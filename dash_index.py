import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_front_page
import app
from app import app
import dash_page_app
from dash_page_app import generate_layout



# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children = dash_front_page.layout)
])



@app.callback(Output('page-title','children'),
              [Input('url', 'pathname')])
def change_subject(pathname):
    if pathname != None and pathname.startswith('/apps/page_app/'):
        string = pathname.split('/')[-1]
        string = ' '.join(string.split('%20'))
        return string

# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname != None and pathname.startswith('/apps/page_app/'):
        string = pathname.split('/')[-1]
        string = ' '.join(string.split('%20'))
        dash_page_app.query = string
        return generate_layout(string)
        
    else:
        return dash_front_page.layout
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)