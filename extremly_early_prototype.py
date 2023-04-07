import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

#Test lista av jobb här, vi kommer nog behöva köra en databas här
Jobs = (
    {"title": "Software engineer", "skills": ["python", "c#", "git"]},
    {"title": "Unity Developer", "skills": ["c#", "git"]},
    {"title": "DevOps Engineer", "skills": ["python", "git", "kubernetes", "cloud", "linux"]},
    {"title": "Systems Engineer", "skills": ["systemvetenskap", "git", "ccna", "python"]},
    {"title": "Front-end Developer", "skills": ["javascript", "css", "html"]}
)


#En dictionary med skills som har två nycklar en för label och en annan för value
skills = {"label": 
          ["javascript", "css", "ccna", "html", "python", "c#", "git", "systemvetenskap", "kubernetes", "cloud", "linux",],
          "value": ["javascript", "css", "ccna", "html", "python", "c#", "git", "systemvetenskap", "kubernetes", "cloud", "linux",]}

#Gör om hela dictionary till flertal dictionaries 
new_list = [{"label": label, "value": value} for label, value in zip(skills["label"], skills["value"])]

#Själva frontenden
app.layout = html.Div([
    html.H6(children="Hello world extremly early prototype:"),
    
    #Själva checklistan
    dcc.Checklist(id='skills',
                 options = new_list, #options är variabeln som deklarerar själva 
                    value=[], #value är variabeln som håller in alla valda val, mer om både options och value kommer in i callback
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
        return ''
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
    app.run_server(debug=True)
