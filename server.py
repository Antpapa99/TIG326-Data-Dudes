from flask import Flask, render_template, url_for
import dash
import dash_bootstrap_components as dbc


#The backend for our basic home and about pages

server = Flask(__name__, static_folder='static/style')

@server.route('/', methods=['GET', 'POST'])
def home():
    image_path1 = url_for('static', filename='img/skillflair.PNG')
    image_path2 = url_for('static', filename='img/skillflair_frontpage.PNG')
    return render_template('home.html', image_path1=image_path1, image_path2=image_path2)

#the backend for our dash application
app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/",
                external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/custom.css'])

#the about page route
@server.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')