from flask import Flask, render_template
import dash
import dash_html_components as html
import dash_core_components as dcc
from Skills_Selector import select_skills

server = Flask(__name__)


@server.route('/')
def hello():
    return render_template("home.html")

app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/")

#Test lista av jobb här, vi kommer nog behöva köra en databas här
Jobs = (
    {"title": "Software engineer", "skills": ["python", "c#", "git"]},
    {"title": "Unity Developer", "skills": ["c#", "git"]},
    {"title": "DevOps Engineer", "skills": ["python", "git", "kubernetes", "cloud", "linux"]},
    {"title": "Systems Engineer", "skills": ["systemvetenskap", "git", "ccna", "python"]},
    {"title": "Front-end Developer", "skills": ["javascript", "css", "html"]},
    {"title": "Network Engineer", "skills": ["ccna"]},
    {"title": "Student", "skills": ["systemvetenskap"]},
    {"title": "Database Admin", "skills": ["sql"]},
)



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
    if not selected_skills: #Om inte väljer något får man inget tillbaka
        return "no matches"
    matches = [] #Själva listan som lagrar jobben när man väljer de olika skills
    for job in Jobs: #For loopen för att iterar genom jobben
        required_skills = set(job['skills']) #skills som jobb kräver
        seeker_skills = set(selected_skills) #skills som du väljher
        if required_skills.issubset(seeker_skills): #skills som du väljer som är lika med skills som jobb kräver
            matches.append(job['title']) #Alla jobb som du kan få med dina skills
    if matches:
        return html.Ul([html.Li(match) for match in matches]) #Returnera alla matchingar
    else:
        return 'no Matches found'

if __name__ == '__main__':
    server.run(debug=True)
