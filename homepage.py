"""


Author: Alan Mackiewicz

Provided is the homepage I propose for the project. I thought it would be a good idea to take random comments on
the internet about the war and present them like a tweet that changes every once in a while. The hyperlinks do not work right now 
I wasnt sure how to make them work at the moment.


"""

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import random


file_path_comments = 'data/comments_data.csv'
comments_df = pd.read_csv(file_path_comments)

app = dash.Dash(__name__, suppress_callback_exceptions=True)


app.layout = html.Div([
    html.H1("Ukraine Russia Conflict Dashboard", style={'textAlign': 'center'}),
    
    # Navigation menu
    html.Div([
        dcc.Link('Home', href='/', style={'margin': '0 20px', 'textDecoration': 'none'}),
        dcc.Link('Section 1', href='/civilian_impact.py', style={'margin': '0 20px', 'textDecoration': 'none'}),
        dcc.Link('Section 2', href='/section-2', style={'margin': '0 20px', 'textDecoration': 'none'}),
       
    ], style={
        'textAlign': 'center',
        'margin': 'auto',
        'width': 'fit-content',
        'padding': '10px',
        'borderRadius': '15px',
        'display': 'flex',
        'justifyContent': 'center',
        'backgroundColor': '#f5f5f5',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }),
    
    


    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    
    # Comments section styled like Twitter Comment
    html.Div(id='comments-container', children=[], style={
        'overflow': 'auto',
        'maxHeight': '500px',
        'width': '600px',
        'margin': '20px auto',  
        'textAlign': 'left'
    }),
    dcc.Interval(id='interval-component', interval=8000, n_intervals=0)
])



# Callback to update comments
@app.callback(
    Output('comments-container', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_comments(_):
    random_index = random.randint(0, len(comments_df) - 1)
    comment = comments_df.iloc[random_index]['comment_body']
    
    # Twitter style card
    tweet_style_card = html.Div(
        style={
            'border': '1px solid #e1e8ed',
            'borderRadius': '15px',
            'padding': '10px 15px',
            'margin': '10px 0',
            'maxWidth': '500px',
            'backgroundColor': 'white',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        },
        children=[
            html.Div(
                style={'display': 'flex', 'paddingBottom': '10px'},
                children=[
                    html.Img(src='imgs/ctpLogo.png', style={'borderRadius': '50%', 'width': '40px', 'height': '40px'}),
                    html.Div(
                        style={'marginLeft': '10px'},
                        children=[
                            html.P('CoolUser', style={'margin': '0', 'fontWeight': 'bold'}),
                            html.P('@RussoUkraineWar', style={'margin': '0', 'color': '#657786'})
                        ]
                    )
                ]
            ),
            html.P(comment, style={'fontSize': '14px'}),
            html.Div(
                style={'display': 'flex', 'justifyContent': 'space-between', 'paddingTop': '10px', 'color': '#657786'},
                children=[
                    html.Span('11:00 AM - Month Day, Year', style={'fontSize': '12px'}),
                    html.Div(
                        style={'display': 'flex', 'gap': '20px'},
                        children=[
                            html.Span('Retweets'),
                            html.Span('Likes')
                        ]
                    )
                ]
            )
        ]
    )
    
    return tweet_style_card

if __name__ == '__main__':
    app.run_server(debug=True)



