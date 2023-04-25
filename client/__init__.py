from flask import Flask
from client.store.store import Store

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key'
store = Store()