import dash
import plotly.graph_objs as go
import dash_html_components as html
from server import app
from layout import new_Jobs

@app.callback(
    dash.dependencies.Output('jobs-dropdown', 'style'),
    dash.dependencies.Output('skills-dropdown', 'style'),
    [dash.dependencies.Input('search-dropdown', 'value')]
)
def toggle_dropdowns(search_type):
    if search_type == 'Jobs':
        return {'display': 'block'}, {'display': 'none'}
    elif search_type == 'Skills':
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}


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
    dash.dependencies.Output('skills-barchart', 'figure'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('jobs-dropdown', 'value')]
)
def update_graph(n_clicks, selected_job):
    if not selected_job:
        return go.Figure()  # return empty figure
    job = next((job for job in new_Jobs if job['label'] == selected_job), None)
    if job:
        skills = job['skills']
        names = [skill['name'] for skill in skills]
        counts = [skill['count'] for skill in skills]
        return {
            'data': [
                go.Bar(
                    x=names,
                    y=counts,
                    text=counts,
                    textposition='auto'
                )
            ],
            'layout': go.Layout(
                title='Skills Distribution',
                xaxis={'title': 'Skills'},
                yaxis={'title': 'Count'},
            )
        }
    return go.Figure()


@app.callback(
    dash.dependencies.Output('job-matches', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('skills-dropdown', 'value')]
)
def match_jobs(n_clicks, selected_skills):
    if not selected_skills:
        return "no matches"
    matches = []
    for job in new_Jobs:
        required_skills = set(skill['name'] for skill in job['skills'])
        seeker_skills = set(selected_skills)
        if required_skills and seeker_skills.issubset(required_skills):
            matches.append(job['label'])
    if matches:
        return html.Ul([html.Li(match) for match in matches])
    else:
        return 'no Matches found'
