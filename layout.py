import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from server import app
from Skills_Selector import select_skills
from Job_Selector import jobs

new_Jobs = jobs()
new_skills = select_skills()

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H3("Job Skills Matcher"), width={'size': 6, 'offset': 3}),
        className="mt-5"
    ),

    dbc.Row(
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
    dbc.Button('Match jobs', id='submit-button', className="mt-3"),
    dbc.Button('Match Skills', id='match-skills-button', className="mt-3"),  # Add this line
    html.Div(id='job-matches', className="my-3"),
    dcc.Graph(id='skills-barchart'),
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.Div(id='selected-job', style={'display': 'none'}),
    dcc.Store(id='job-link-styles', data={}),
], width={'size': 6, 'offset': 3}),
    )
], fluid=True)
