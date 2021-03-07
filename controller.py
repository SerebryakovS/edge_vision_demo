#!/usr/bin/python3

import json;
import time;
import socket;
import asyncio;
import aiofiles;
import requests;
import threading;
from json import loads,dumps
from queue import Queue
from get_config import get_config
params = get_config();
sensors_num = int(params['SENSORS_NUMBER']);
q_curr = Queue(sensors_num);


async def read_sensor_data(sensors_path, sensor_index, _queue):
    async with aiofiles.open(sensors_path+"/sensor_"+str(sensor_index),'rb') as afp:
        sensor_data = await afp.readline();
        _queue.put(sensor_data);

async def read_all_sensors():
    tasks = [];
    for index in range(int(params['SENSORS_NUMBER'])):
        task = asyncio.create_task(read_sensor_data(params['SENSORS_FOLDER'],index,q_curr));
        tasks.append(task);
    await asyncio.gather(*tasks);

def analyze_dataset(recvd_que):
    num_sensors = int(params['SENSORS_NUMBER']);
    input_dict = dict((str(key),"") for key in range(num_sensors));
    time.sleep(1);
    counter = num_sensors;
    while True:
        if not q_curr.empty():
            curr_val = json.loads(q_curr.get());
            if input_dict[curr_val['sens_num']] == "":
                input_dict[curr_val['sens_num']] = curr_val['payload'];
                counter-=1;
            if counter ==0:
                break;
        else:
            time.sleep(0.1);
            pass;
    summa = 0;
    for key in input_dict:
        summa+=int(input_dict[key]);
    status = "down" if summa/num_sensors < 500 else "up";
    time_of_decision = time.strftime("%Y-%m-%d-%H.%M.%S",time.localtime());
    time.sleep(int(params['DECISION_TIME']));
    return time_of_decision,status;

def run_sensors_reader():
    while True:
        asyncio.run(read_all_sensors());
    
if __name__ == "__main__":
    sensors_thread = threading.Thread(target=run_sensors_reader,args=());
    sensors_thread.start()
    while True:
        time_of_decision,status = analyze_dataset(q_curr);
        message = json.dumps({"datetime": time.strftime("%Y-%m-%d-%H.%M.%S",time.localtime()),
                              "status": status,
                              "time_of_decision": time_of_decision});
        #---------------------------------------------------------------------send_to_manipulator
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as manipulator:
                manipulator.connect((params['MANIPULATOR_HOST'], int(params['MANIPULATOR_PORT'])))
                manipulator.send(message.encode());
        except Exception as ex:
            print("connect to manipulator: "+str(ex));
        #---------------------------------------------------------------------send_to_third_party_server
        try:
            requests.post("http://%s:%s/set_status"%(params['MANIPULATOR_HOST'],
                                                     params['WEB_SERVISE_PORT']),data=message);
        except Exception as ex:
            print("connect to third_party_server: "+str(ex));
    
