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

@app.callback(
    dash.dependencies.Output('match-skills-button', 'style'),
    [dash.dependencies.Input('skills-dropdown', 'style')]
)
def toggle_match_skills_button(skills_dropdown_style):
    if skills_dropdown_style['display'] == 'block':
        return {'display': 'block'}  # If skills dropdown is visible, show the button
    else:
        return {'display': 'none'}  # If skills dropdown is not visible, hide the button

#Graphs
@app.callback(
    dash.dependencies.Output('skills-barchart', 'figure'),
    [dash.dependencies.Input('jobs-dropdown', 'value')]
)
def update_graph(selected_job):
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

@app.callback(
    dash.dependencies.Output('job-matches', 'children'),
    [dash.dependencies.Input('skills-dropdown', 'value'),
     dash.dependencies.Input('match-skills-button', 'n_clicks'),
     dash.dependencies.Input('job-link-styles', 'data')]
)
def match_jobs(selected_skills, n_clicks, styles):
    if not n_clicks or not selected_skills:
        return "No matches"
    matches = []
    for job in new_Jobs:
        required_skills = set(skill['name'] for skill in job['skills'])
        seeker_skills = set(selected_skills)
        if required_skills and (seeker_skills & required_skills): 
            button_style = styles.get(job['label'], {})
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
     dash.dependencies.Input('hidden-div', 'children'),
     dash.dependencies.Input('job-link-styles', 'data')],  # Add this line
    [dash.dependencies.State('skills-dropdown', 'value')]
)
def display_job_skills(dropdown_value, clicked_job, styles, selected_skills):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "No job selected"
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # If the trigger comes from the dropdown
        if trigger_id == 'jobs-dropdown':
            selected_job_label = dropdown_value
        elif trigger_id == 'job-link-styles':  # Add this condition
            selected_job_label = next(
                job for job, style in styles.items() if style.get('background-color') == 'green'
            )
        else:  # trigger_id == 'hidden-div'
            selected_job_label = clicked_job
    if selected_job_label:
        job = next((job for job in new_Jobs if job['label'] == selected_job_label), None)
        if job:
            skills = job['skills']
            # Added logic for show more/show less functionality
            if len(skills) > 10:
                visible_skills = skills[:10]  # Display the first 10 skills initially
                hidden_skills = skills[10:]  # Skills to be hidden initially

                children = []
                children.extend([
                    html.Ul([html.Li(
                        f"{skill['name']} ({skill['count']})",
                        style={"font-weight": "bold", "color": "red"} if skill['name'] in selected_skills else {}
                    ) for skill in visible_skills]),
                    html.Ul(
                        id='hidden-skills',
                        children=[html.Li(
                            f"{skill['name']} ({skill['count']})",
                            style={"font-weight": "bold", "color": "red"} if skill['name'] in selected_skills else {}
                        ) for skill in hidden_skills],
                        style={'display': 'none'}
                    )
                ])
                children.append(html.Button(
                    'Show More',
                    id='show-more-button',
                    n_clicks=0,
                    style={'display': 'block', 'margin-top': '10px'}
                ))
                return children
            else:
                return html.Ul([html.Li(
                    f"{skill['name']} ({skill['count']})",
                    style={"font-weight": "bold", "color": "red"} if skill['name'] in selected_skills else {}
                ) for skill in skills])
    return "No job selected"


def highlight_selected_job(dropdown_value, clicked_job, ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [{} for _ in ids]
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # If the trigger comes from the dropdown
        if trigger_id == 'jobs-dropdown':
            selected_job_label = dropdown_value
        else:  # trigger_id == 'hidden-div'
            selected_job_label = clicked_job

    return [{'background-color': 'green'} if id['index'] == selected_job_label else {} for id in ids]

@app.callback(
    dash.dependencies.Output('job-link-styles', 'data'),
    [dash.dependencies.Input({'type': 'job-link', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [dash.dependencies.State({'type': 'job-link', 'index': dash.dependencies.ALL}, 'id'),
     dash.dependencies.State('job-link-styles', 'data')]
)
def handle_job_click(n_clicks, ids, styles):
    if not any(n_clicks):
        return styles  # No buttons have been clicked yet, return current styles
    # Get the label of the clicked job
    clicked_job_label = next(id['index'] for n_click, id in zip(n_clicks, ids) if n_click)
    # Reset all styles and set the style of the clicked job to green
    new_styles = {id['index']: {} for id in ids}  # reset styles
    new_styles[clicked_job_label] = {'background-color': 'green'}  # highlight clicked job
    return new_styles


@app.callback(
    [dash.dependencies.Output({'type': 'job-link', 'index': dash.dependencies.ALL}, 'style')],
    [dash.dependencies.Input('job-link-styles', 'data')],
    [dash.dependencies.State({'type': 'job-link', 'index': dash.dependencies.ALL}, 'id')]
)

def update_job_link_styles(styles, ids):
    return [styles.get(id['index'], {}) for id in ids]


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
