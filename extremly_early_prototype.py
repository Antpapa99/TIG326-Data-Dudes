from flask import Flask, render_template
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from Skills_Selector import select_skills
from Job_Selector import jobs


server = Flask(__name__)


@server.route('/')
def hello():
    return render_template("home.html")


app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/",
                external_stylesheets=[dbc.themes.BOOTSTRAP])

new_Jobs = jobs()
new_skills = select_skills()
print(new_skills)

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H3("Job Skills Matcher"), width={'size': 6, 'offset': 3}),
        className="mt-5"
    ),

    dbc.Row(
        dbc.Col([
            dcc.Dropdown(id='jobs-dropdown',
                         options=[{'label': job['label'], 'value': job['label']} for job in new_Jobs],
                         placeholder="Select a job",
                         ),
            html.Div(id='job-skills', className="my-3"),
            dcc.Dropdown(id='skills',
                         options=new_skills,
                         value=[],
                         multi=True,
                         ),
            dbc.Button('Match jobs', id='submit-button', className="mt-3"),
            html.Div(id='job-matches', className="my-3"),
        ], width={'size': 6, 'offset': 3}),
    )
], fluid=True)


@app.callback(
    dash.dependencies.Output('job-skills', 'children'),
    [dash.dependencies.Input('jobs-dropdown', 'value')]
)
def display_job_skills(selected_job_label):
    if selected_job_label:
        job = next((job for job in new_Jobs if job['label'] == selected_job_label), None)
        if job:
            skills = job['skills']
            return html.Ul([html.Li(f"{skill['name']} ({skill['count']})") for skill in skills])
    return "No job selected"


@app.callback(
    dash.dependencies.Output('job-matches', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('skills', 'value')]
)
def match_jobs(n_clicks, selected_skills):
    if not selected_skills:
        return "no matches"
    matches = []
    for job in new_Jobs:
        required_skills = set(skill['name'] for skill in job['skills'])
        seeker_skills = set(selected_skills)
        if required_skills and required_skills.issubset(seeker_skills):
            matches.append(job['label'])
    if matches:
        return html.Ul([html.Li(match) for match in matches])
    else:
        return 'no Matches found'

if __name__ == '__main__':
    server.run(debug=True)
