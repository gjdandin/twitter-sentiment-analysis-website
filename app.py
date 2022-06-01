from flask import Flask, render_template, request, url_for
from routes import configure_routes
import main

app = Flask(__name__, template_folder="templates")
configure_routes(app)

if __name__ == '__main__':
    app.run()
