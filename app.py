import dash

app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.css.append_css({'external_url': "https://fonts.googleapis.com/css?family=Dosis|Titillium+Web" })
if __name__ == '__main__':
    app.run_server(debug=True)