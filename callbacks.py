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
    [dash.dependencies.Input('jobs-dropdown', 'value')],
    [dash.dependencies.State('job-skills', 'children')]
)
def display_job_skills(selected_job_label, current_children):
    if selected_job_label:
        job = next((job for job in new_Jobs if job['label'] == selected_job_label), None)
        if job:
            skills = job['skills']
            if len(skills) > 10:
                visible_skills = skills[:10]  # Display the first 10 skills initially
                hidden_skills = skills[10:]  # Skills to be hidden initially

                if current_children:
                    # Remove existing show more button if it exists
                    children = [child for child in current_children if not isinstance(child, html.Button)]
                else:
                    children = []

                children.extend([
                    html.Ul([html.Li(f"{skill['name']} ({skill['count']})") for skill in visible_skills]),
                    html.Ul(
                        id='hidden-skills',
                        children=[html.Li(f"{skill['name']} ({skill['count']})") for skill in hidden_skills],
                        style={'display': 'none'}
                    )
                ])

                if len(skills) > 10:
                    children.append(html.Button(
                        'Show More',
                        id='show-more-button',
                        n_clicks=0,
                        style={'display': 'block', 'margin-top': '10px'}
                    ))

                return children
            else:
                return html.Ul([html.Li(f"{skill['name']} ({skill['count']})") for skill in skills])

    # Clear the children if no job is selected
    return []




@app.callback(
    dash.dependencies.Output('hidden-skills', 'style'),
    dash.dependencies.Output('show-more-button', 'children'),
    dash.dependencies.Output('show-more-button', 'style'),
    [dash.dependencies.Input('show-more-button', 'n_clicks')],
    [dash.dependencies.State('hidden-skills', 'style')]
)
def show_hidden_skills(n_clicks, hidden_skills_style):
    if n_clicks % 2 == 1:
        return {'display': 'block'}, 'Show Less', {'display': 'block', 'margin-top': '10px'}
    else:
        return {'display': 'none'}, 'Show More', {'display': 'block', 'margin-top': '10px'}

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

@app.callback(
    dash.dependencies.Output('skills-barchart', 'figure'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('jobs-dropdown', 'value')]
    )
def update_graph(n_clicks, selected_job):
    if not selected_job:
        return go.Figure() # return empty figure
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