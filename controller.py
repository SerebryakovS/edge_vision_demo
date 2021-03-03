
import time;
import socket;
import requests;
from json import loads,dumps
from get_config import get_config
params = get_config();
#while [[ 1 ]]:
    #start_time = time.time();
data_template = dumps({"datetime":time.strftime("%Y-%m-%d-%H.%M.%S",time.localtime()),
                       "status":,# up or down
                       "time_of_decision":});
response = loads(requests.post("http://127.0.0.1:%s/test_request"%(params['WEB_SERVISE_PORT']),data=data).text);



print(response)


