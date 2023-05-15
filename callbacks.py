import dash
import plotly.graph_objs as go
import dash_html_components as html
from server import app
from layout import new_Jobs

#dropdown selector
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


#Graphs
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

#Matching mechanism
@app.callback(
    dash.dependencies.Output('job-matches', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('skills-dropdown', 'value'),
     dash.dependencies.State('selected-job', 'children')]
)
def match_jobs(n_clicks, selected_skills, selected_job):
    if not selected_skills:
        return "No matches"
    matches = []
    for job in new_Jobs:
        global seeker_skills
        required_skills = set(skill['name'] for skill in job['skills'])
        seeker_skills = set(selected_skills)
        if required_skills and seeker_skills.issubset(required_skills):
            # Check if the current job is the selected job
            button_style = {'background-color': 'green'} if job['label'] == selected_job else {}
            matches.append(html.Div([
                html.Button(job['label'], id={'type': 'job-link', 'index': job['label']}, style=button_style),
            ]))
    if matches:
        return matches
    else:
        return 'No Matches found'

#click on jobs callback


@app.callback(
    dash.dependencies.Output('job-skills', 'children'),
    [dash.dependencies.Input('jobs-dropdown', 'value'),
     dash.dependencies.Input('hidden-div', 'children')]
)
def display_job_skills(dropdown_value, clicked_job):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "No job selected"
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # If the trigger comes from the dropdown
        if trigger_id == 'jobs-dropdown':
            selected_job_label = dropdown_value
        else:  # trigger_id == 'hidden-div'
            selected_job_label = clicked_job
    if selected_job_label:
        job = next((job for job in new_Jobs if job['label'] == selected_job_label), None)
        if job:
            skills = job['skills']
            return html.Ul([
                html.Li(
                    f"{skill['name']} ({skill['count']})",
                    style={"font-weight": "bold", "color": "red"} if skill['name'] == "python" else {}
                )
                for skill in skills
            ])
    return "No job selected"

@app.callback(
    dash.dependencies.Output('hidden-div', 'children'),
    [dash.dependencies.Input({'type': 'job-link', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [dash.dependencies.State({'type': 'job-link', 'index': dash.dependencies.ALL}, 'id')]
)
def handle_job_click(n_clicks, ids):
    if not any(n_clicks):
        return dash.no_update
    # Get the label of the clicked job
    clicked_job_label = next(id['index'] for n_click, id in zip(n_clicks, ids) if n_click)
    return clicked_job_label