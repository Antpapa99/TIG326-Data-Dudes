from flask import Flask, render_template
import dash
import dash_html_components as html
import dash_core_components as dcc
from Skills_Selector import select_skills
from Job_Selector import jobs

server = Flask(__name__)


@server.route('/')
def hello():
    return render_template("home.html")

app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/")

#Test lista av jobb här, vi kommer nog behöva köra en databas här
new_Jobs = jobs()
new_skills = select_skills()
new_list = new_skills

#Själva frontenden
app.layout = html.Div([
    html.H6(children="Hello world extremly early prototype:"),
    
    #Själva checklistan
    dcc.Dropdown(id='skills',
                 options = new_skills, #options är variabeln som deklarerar själva 
                    value=[], #value är variabeln som håller in alla valda val, mer om både options och value kommer in i callback
                    multi = True,
    ),
    html.Button('Match jobs', id='submit-button'), #Själva knappen till matchningen
    html.Div(id='job-matches'), #ids används som referenser  in koden och i callback funktionen
    ])
    
@app.callback( #En decorater som säger till Dash att associera funktionen nedan med en specifik output komponent och input komponent
    dash.dependencies.Output('job-matches', 'children'), #Själva output komponenten som upddateras när callback triggras
    [dash.dependencies.Input('submit-button', 'n_clicks')], #Själva input komponenten som triggras när man klickar på knappen
    [dash.dependencies.State('skills', 'value')] #Detta är komponenter som input behöver läsa in för att returnera ett värde som kommer att uppdatera "children" som är en del av job-matching
)

def match_jobs(n_clicks, selected_skills):
    print("test")
    if not selected_skills:
        return "no matches"
    matches = []
    for job in new_Jobs:
        required_skills = []
        required_skills = [skill['name'] for skill in job['skills']]
        seeker_skills = set(selected_skills)
        if set(seeker_skills).issubset(required_skills):
            matches.append(job['label'])
    if matches:
        return html.Ul([html.Li(match) for match in matches])
    else:
        return 'no Matches found'

if __name__ == '__main__':
    server.run(debug=True)
