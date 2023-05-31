import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import math
from server import app
from layout import new_Jobs

#dropdown selector
@app.callback(
    dash.dependencies.Output('jobs-dropdown', 'style'),
    dash.dependencies.Output('skills-dropdown', 'style'),
    [dash.dependencies.Input('search-dropdown', 'value')]
)

#This actually toggles the dropdowns
def toggle_dropdowns(search_type):
    if search_type == 'Jobs':
        return {'display': 'block'}, {'display': 'none'}
    elif search_type == 'Skills':
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}

#Makes sure that the match skills button doesn't appear when on jobs dropdown
@app.callback(
    dash.dependencies.Output('match-skills-button', 'style'), 
    [dash.dependencies.Input('skills-dropdown', 'style')]
)
def toggle_match_skills_button(skills_dropdown_style):
    if skills_dropdown_style['display'] == 'block':
        return {'display': 'block'}  # If skills dropdown is visible, show the button
    else:
        return {'display': 'none'}  # If skills dropdown is not visible, hide the button


#Kind of clears the selected job when you switch to select skills 
@app.callback(
    dash.dependencies.Output('job-matches', 'style'),
    [dash.dependencies.Input('search-dropdown', 'value')]
)
def toggle_job_matches(search_type):
    if search_type == 'Jobs':
        return {'display': 'none'}
    elif search_type == 'Skills':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


#Same as the match skills one
@app.callback(
    dash.dependencies.Output('exact-match-skills-button', 'style'), 
    [dash.dependencies.Input('skills-dropdown', 'style')]
)
def toggle_exact_match_skills_button(skills_dropdown_style):
    if skills_dropdown_style['display'] == 'block':
        return {'display': 'block'}  # If skills dropdown is visible, show the button
    else:
        return {'display': 'none'}  # If skills dropdown is not visible, hide the button

#Our Graph to show the skill percentages associated with each job role
@app.callback(
    dash.dependencies.Output('skills-barchart', 'figure'),
    [dash.dependencies.Input('jobs-dropdown', 'value')]
)
def update_graph(selected_job):
    if not selected_job:
        return go.Figure()  # return empty figure

    job = next((job for job in new_Jobs if job['label'] == selected_job), None)
    if job:
        skills = job['skills']
        names = [skill['name'] for skill in skills]
        counts = [(str(round((skill['average']) * 100)) + "%") for skill in skills]

        # Update the marker color to green (#086971)
        bar_color = '#086971'

        title = 'Skills Distribution For ' + job['label']
        subtitle = 'Number of Job Ads: ' + str(job["count"])

        return {
            'data': [
                go.Bar(
                    x=names,
                    y=counts,
                    text=counts,
                    textposition='auto',
                    marker={'color': bar_color}  # Set the bar color
                )
            ],
            'layout': go.Layout(
                title={
                    'text': '<b>' + title + '</b><br>' + subtitle,
                    'y': 0.9,  # Adjust the vertical position of the title
                    'x': 0.5,  # Center the title horizontally
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                xaxis={'title': 'Skills'},
                yaxis={'title': 'Presence in job ads(%)'},
            )
        }

    return go.Figure()


#Our big function that matches selected skills with jobs as well code that makes sure it nice to look at it

@app.callback(
    [dash.dependencies.Output('job-matches', 'children'),
     dash.dependencies.Output('pagination', 'max_value'),
     dash.dependencies.Output('pagination', 'hidden')],
    [dash.dependencies.Input('skills-dropdown', 'value'),
     dash.dependencies.Input('last-button-pressed', 'data'),
     dash.dependencies.Input('job-link-styles', 'data'),
     dash.dependencies.Input('pagination', 'active_page')],
)
def match_jobs(selected_skills, last_button_pressed, styles, active_page):
    if not selected_skills or not last_button_pressed:
        return "", 1, True

    job_matches = []  # a list to store tuples (match count, job label, job button)

    for job in new_Jobs:
        required_skills = set(skill['name'] for skill in job['skills'])
        seeker_skills = set(selected_skills)
        if required_skills:
            match_count = len(seeker_skills & required_skills) # calculating number of matching skills
            button_style = styles.get(job['label'], {})
            if last_button_pressed == 'exact-match-skills-button':
                if required_skills.issuperset(seeker_skills): 
                    job_button = html.Button(job['label'], id={'type': 'job-link', 'index': job['label']}, className='fancy-button', style=button_style)
                    job_matches.append((match_count, job['label'], job_button))
            else:  # The match skills button was pressed last or is the only one pressed
                if required_skills & seeker_skills: 
                    job_button = html.Button(job['label'], id={'type': 'job-link', 'index': job['label']}, className='fancy-button', style=button_style)
                    job_matches.append((match_count, job['label'], job_button))

    # sort the job matches by match count (highest first)
    job_matches.sort(key=lambda x: x[0], reverse=True)

    if job_matches:
        matches = [job[2] for job in job_matches]  # retrieve job buttons from the sorted list

        items_per_page = 15
        pages = math.ceil(len(matches) / items_per_page)
        active_page = active_page or 1
        start = (active_page - 1) * items_per_page
        end = start + items_per_page

        return matches[start:end], pages, False
    else:
        return '', 1, True



# Basically a function that shows skills associated with each job
@app.callback(
    dash.dependencies.Output('job-skills', 'children'),
    [dash.dependencies.Input('search-dropdown', 'value'),
     dash.dependencies.Input('jobs-dropdown', 'value'),
     dash.dependencies.Input('selected-job-store', 'data')],
    [dash.dependencies.State('skills-dropdown', 'value')]
)
def display_job_skills(search_type, dropdown_value, selected_job_store, selected_skills):
    # If the search type is 'Skills', return "No job selected"
    #if search_type == 'Skills':
        #return [] # clear the skill list

    ctx = dash.callback_context
    if not ctx.triggered:
        return ""
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # If the trigger comes from the dropdown
        if trigger_id == 'jobs-dropdown':
            selected_job_label = dropdown_value
        elif trigger_id == 'selected-job-store':  # the job link button was clicked
            selected_job_label = selected_job_store
        else:  # No job selected
            return ""

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
                            f"{skill['name']}",
                            style={"font-weight": "bold", "color": "green"} if skill['name'] in selected_skills else {}
                        ) for skill in visible_skills]),
                        html.Ul(
                            id='hidden-skills',
                            children=[html.Li(
                                f"{skill['name']}",
                                style={"font-weight": "bold", "color": "green"} if skill['name'] in selected_skills else {}
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
                        f"{skill['name']}",
                        style={"font-weight": "bold", "color": "green"} if skill['name'] in selected_skills else {}
                    ) for skill in skills])
        return ""


#A function that handles the interaction with job buttons i.e the jobs that are shown when you select and match skills
@app.callback(
    dash.dependencies.Output('job-link-styles', 'data'),
    dash.dependencies.Output('selected-job-store', 'data'),
    [dash.dependencies.Input({'type': 'job-link', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [dash.dependencies.State({'type': 'job-link', 'index': dash.dependencies.ALL}, 'id'),
     dash.dependencies.State('job-link-styles', 'data')]
)
def handle_job_click(n_clicks, ids, styles):
    if not any(n_clicks):
        return styles, dash.no_update  # No buttons have been clicked yet, return current styles
    # Get the label of the clicked job
    clicked_job_label = next(id['index'] for n_click, id in zip(n_clicks, ids) if n_click)
    # Reset all styles and set the style of the clicked job to green
    new_styles = {id['index']: {} for id in ids}  # reset styles
    new_styles[clicked_job_label] = {'background-color': 'green'}  # highlight clicked job
    return new_styles, clicked_job_label

#
@app.callback(
    [dash.dependencies.Output({'type': 'job-link', 'index': dash.dependencies.ALL}, 'style')],
    [dash.dependencies.Input('job-link-styles', 'data')],
    [dash.dependencies.State({'type': 'job-link', 'index': dash.dependencies.ALL}, 'id')]
)

def update_job_link_styles(styles, ids):
    return [styles.get(id['index'], {}) for id in ids]

#Adds a show more or show less button for skills and makes it work
@app.callback(
    dash.dependencies.Output('hidden-skills', 'style'),
    dash.dependencies.Output('show-more-button', 'children'),
    dash.dependencies.Output('show-more-button', 'style'),
    [dash.dependencies.Input('show-more-button', 'n_clicks')],
    [dash.dependencies.State('hidden-skills', 'style')]
)
def show_hidden_skills(n_clicks, hidden_skills_style):
    if n_clicks % 2 == 1:
        return {'display': 'block'}, 'Show Less', {'display': 'block', 'margin-top': '10px', 'background-color': '#086971', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'text-align': 'center', 'text-decoration': 'none', 'display': 'inline-block', 'font-size': '16px', 'margin': '4px 2px', 'cursor': 'pointer', 'border-radius': '12px'}
    else:
        return {'display': 'none'}, 'Show More', {'display': 'block', 'margin-top': '10px', 'background-color': '#086971', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'text-align': 'center', 'text-decoration': 'none', 'display': 'inline-block', 'font-size': '16px', 'margin': '4px 2px', 'cursor': 'pointer', 'border-radius': '12px'}

#

@app.callback(
    dash.dependencies.Output('last-button-pressed', 'data'),
    [dash.dependencies.Input('match-skills-button', 'n_clicks'),
     dash.dependencies.Input('exact-match-skills-button', 'n_clicks')]
)
def update_last_button_pressed(match_n_clicks, exact_n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ''
    else:
        button_id = ctx.triggered[-1]['prop_id'].split('.')[0]
        return button_id
    
@app.callback(
    dash.dependencies.Output('selected-job', 'children'),
    [dash.dependencies.Input('jobs-dropdown', 'value')]
)
def update_selected_job(dropdown_value):
    return dropdown_value

@app.callback(
    dash.dependencies.Output('clicked-job', 'children'),
    [dash.dependencies.Input({'type': 'job-link', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [dash.dependencies.State({'type': 'job-link', 'index': dash.dependencies.ALL}, 'id')]
)
@app.callback(
    dash.dependencies.Output('jobs-dropdown', 'value'),
    [dash.dependencies.Input({'type': 'job-link', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [dash.dependencies.State({'type': 'job-link', 'index': dash.dependencies.ALL}, 'id')]
)
def update_jobs_dropdown_from_link(n_clicks, ids):
    if not any(n_clicks):
        return dash.no_update  # No buttons have been clicked yet, don't update
    # Get the label of the clicked job
    clicked_job_label = next(id['index'] for n_click, id in zip(n_clicks, ids) if n_click)
    return clicked_job_label

@app.callback(
    dash.dependencies.Output('clicked-button-store', 'data'),
    [dash.dependencies.Input({'type': 'job-link', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [dash.dependencies.State({'type': 'job-link', 'index': dash.dependencies.ALL}, 'id')]
)
def store_clicked_button(n_clicks, ids):
    if not any(n_clicks):
        return dash.no_update  # No buttons have been clicked yet, return current styles
    # Get the label of the clicked job
    clicked_button_id = next(id['index'] for n_click, id in zip(n_clicks, ids) if n_click)
    return clicked_button_id

@app.callback(
    [dash.dependencies.Output({'type': 'job-link', 'index': dash.dependencies.ALL}, 'className')],
    [dash.dependencies.Input('clicked-button-store', 'data')],
    [dash.dependencies.State({'type': 'job-link', 'index': dash.dependencies.ALL}, 'id')]
)
def update_button_styles(clicked_button_id, ids):
    return ['fancy-button-clicked' if id['index'] == clicked_button_id else 'fancy-button' for id in ids]

