import configparser
import json
import datetime

from flask import Flask, request, Request
from pymongo import MongoClient, ASCENDING, DESCENDING

from json_encoder import JSONEncoder

config = configparser.ConfigParser()
config.read('config/db_conf.ini')

app = Flask(__name__)

client = MongoClient(
        host='{}:{}'.format(config['INSTANCE']['HOST'], config['INSTANCE']['PORT']),
        serverSelectionTimeoutMS=config['INSTANCE']['TIMEOUT'],
        username=config['MAIN']['DB_USER'],
        password=config['MAIN']['DB_PW'],
    )

@app.route('/')
def log():
    #print(client.server_info())
    request_data: Request = request.headers.environ.get('werkzeug.request')
    log = {
        'timestamp': datetime.datetime.now().timestamp(),
        'device': 'pc',
        'remote_access': request_data.remote_addr,
        'client_browser': request_data.user_agent.browser,
        'client_os': request_data.user_agent.platform,
        'log_msg': 'Testing'
    }

    log_db = client['log_db']
    access_log = log_db['access_log']
    access_log.insert_one(log)
    return app.response_class(
        response=json.dumps(log, cls=JSONEncoder),
        status=200,
        mimetype='application/json'
    )

@app.route('/latest')
def get_latest_access():
    log_db = client['log_db']
    access_log = log_db['access_log']
    res = access_log.find().sort([('_id', DESCENDING)])
    return app.response_class(
        response=json.dumps(list(res), cls=JSONEncoder),
        status=200,
        mimetype='application/json'
    )






if __name__ == '__main__':
    database_names = client.list_database_names()
    
    print('\ndatabases:', database_names)
    app.run()
