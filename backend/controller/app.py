from flask import Flask
import json

app = Flask(__name__)



@app.route('/')
def hello_world():
    print('test')
    return json.dumps({'msg': 'hi'})

@app.route('/test')
def test():
    print('test')
    return json.dumps({'msg': 'test'})


if __name__ == '__main__':
    app.run()
