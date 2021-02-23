from flask import Flask
import json

app = Flask(__name__)



@app.route('/')
def hello_world():
    return json.dumps({'msg': 'hi'})


if __name__ == '__main__':
    app.run()
