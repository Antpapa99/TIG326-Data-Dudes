import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import math
from server import app
from Skills_Selector import select_skills
from Job_Selector import jobs

new_Jobs = jobs()
new_skills = select_skills()

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            [
                html.Img(src="assets\img\skillflair.PNG", height="150px"),
            ],
            width=12,
        ),
    ),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='search-dropdown',
                         options=[{'label': 'Jobs', 'value': 'Jobs'}, {'label': 'Skills', 'value': 'Skills'}],
                         placeholder="Search by jobs or skills",
                         ),
            dcc.Dropdown(id='jobs-dropdown',
                         options=[{'label': job['label'], 'value': job['label']} for job in new_Jobs],
                         placeholder="Select a job",
                         style={'display': 'none'}),
            dcc.Dropdown(id='skills-dropdown',
                         options=new_skills,
                         value=[],
                         multi=True,
                         style={'display': 'none'}),
            html.Div(id='job-skills', className="my-3"),
            html.Div(id='hidden-skills', className="my-3"),
            dbc.Button('Match Skills', id='match-skills-button', className="mt-3 mb-3 dynamic-job-button"),
            dbc.Button('Exact Match Skills', id='exact-match-skills-button', className="mt-3 mb-3 dynamic-job-button"),
            html.Div(id='job-matches', className="my-3"),
            html.Div(id='hidden-div', style={'display': 'none'}),
            html.Div(id='selected-job', style={'display': 'none'}),
            html.Div(id='clicked-job', style={'display': 'none'}),
            dcc.Store(id='job-link-styles', data={}),
            dcc.Store(id='last-button-pressed', data=''),
            dcc.Store(id='selected-job-store', storage_type='session'),
            dcc.Store(id='clicked-button-store', data=None),
            dcc.Store(id='clicked-button-id', storage_type='memory'),
            dbc.Pagination(id='pagination', max_value=1, size='lg', className='mt-3 mb-3'),
            html.A(
            'Go to Flask homepage',
            href='/',
            className='fancy-link'  # Apply the CSS class to the hyperlink
        ),
        ], width=6, className="mx-auto"),
        dbc.Col([
            dcc.Graph(id='skills-barchart'),
        ], width=6, className="mx-auto"),
    ])
], fluid=True, className='py-5', style={'backgroundColor': '#ffffff'})
