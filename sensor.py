#!/usr/bin/python3
import os
import sys
import json
import time
import random
from queue import Queue
from random import randrange
from threading import Thread
#--------------------------------------------------------------
class sensor(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs);
            except Exception as ex:
                print(ex)
            finally:
                self.tasks.task_done()
#--------------------------------------------------------------
class sensors_pool(object):
    def __init__(self, num_threads,sensors_folder,fifo_prefix):
        self.tasks = Queue(num_threads);
        self.sensors_folder = sensors_folder;
        fifos_arr = list();
        for i in range(num_threads):
            fifos_arr.append(
                os.path.join(self.sensors_folder,fifo_prefix+str(i)));
            try:
                curr_fifo = fifos_arr[-1];
                print("creating FIFO: %s"%curr_fifo);
                os.mkfifo(curr_fifo);
            except Exception as ex:
                print("Failed to create FIFO: %s"%ex);
        for _ in range(num_threads):
            sensor(self.tasks)
    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))
    def map(self, func, args_list1, args_list2, args_list3):
        for arg_index in range(len(args_list1)):
            self.add_task(func, args_list1[arg_index],
                                args_list2[arg_index],
                                args_list3[arg_index])
    def wait_completion(self):
        self.tasks.join();
        os.system("rm -rf %s/*"%self.sensors_folder);
#--------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage : %s seconds_to_work"%sys.argv[0]);
        exit(-1);
    from get_config import get_config
    params = get_config();
    def run_sensor(freq, filename, seconds_to_work):
        sensor_id = filename.split("_")[1];
        sensor_IO = open(filename,'w');
        start_time = time.time();
        waiting_time = 0;
        while seconds_to_work - (time.time()-start_time) >= 0:
            time.sleep(1.0/freq);
            message = json.dumps({"sens_num": sensor_id,
                                  "datetime": time.localtime(),
                                  "payload" : random.randint(1,1000)})
            sensor_IO.write(message+"\n");
        sensor_IO.close();
        os.remove(filename); 
    nb_sensors = int(params['SENSORS_NUMBER']);
    sensors_folder = params['SENSORS_FOLDER'];
    try:
        os.mkdir(sensors_folder);
    except: pass;
    fifo_prefix = "sensor_";
    filename = [sensors_folder+"/"+fifo_prefix+str(i) for i in range(nb_sensors)];
    freq = [int(params['SENSOR_FREQUENCY']) for i in range(nb_sensors)];
    secs = [int(sys.argv[1]) for i in range(nb_sensors)];
    pool = sensors_pool(nb_sensors,sensors_folder,fifo_prefix);
    pool.map(run_sensor,freq,filename,secs);
    pool.wait_completion()
#--------------------------------------------------------------




        
