#!/usr/bin/python3
import os
import json
from flask import jsonify;
from flask import request;
from flask import make_response;
from flask import Flask, render_template,url_for
from get_config import get_config
flask_app = Flask(__name__);
#-------------------------------------------------
@flask_app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(flask_app.root_path,endpoint,filename);
            values['q'] = int(os.stat(file_path).st_mtime);
    return url_for(endpoint, **values);
#-------------------------------------------------
@flask_app.route('/')
def main_page():
    return render_template("index.html");
#-------------------------------------------------
@flask_app.route("/test_request",methods=['POST'])
def return_status():
    jsoned_data = json.loads(request.get_data().decode());
    print(jsoned_data);
    response_body = {'state':"normal_state"};
    return make_response(jsonify(response_body)), 200;
if __name__ == "__main__":
    params = get_config();
    print(params)
    flask_app.run(host='0.0.0.0',port=int(params['WEB_SERVISE_PORT']), debug=True);
    
    
    
