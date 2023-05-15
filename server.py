from flask import Flask, render_template, url_for
import dash
import dash_bootstrap_components as dbc

server = Flask(__name__, static_folder='static/style')

@server.route('/', methods=['GET', 'POST'])
def home():
    image_path = url_for('static', filename='img/skillflair.PNG')
    return render_template('home.html', image_path=image_path)

app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/",
                external_stylesheets=[dbc.themes.BOOTSTRAP])
