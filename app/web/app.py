from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Upload E-Pub to RaspReader'

@app.route('/upload')
def upload():
    return 'Upload...'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')