import os,tempfile
from time import sleep,time
from queue import Queue
from random import randrange
from threading import Thread


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

class sensors_pool(object):
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            sensor(self.tasks)
    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))
    def map(self, func, args_list):
        for args in args_list:
            self.add_task(func, args)
    def wait_completion(self):
        self.tasks.join()

if __name__ == "__main__":
    from get_config import get_config
    params = get_config();
    def run_sensor(freq):
        start_time = time();
        sleep(1);
        print(time()-start_time);
        
        #print("sleeping for (%d)sec" % d)
        #sleep(d)
    numb = int(params['SENSORS_NUMBER']);
    freq = [int(params['SENSOR_FREQUENCY']) for i in range(numb)]
    pool = sensors_pool(numb);
    pool.map(run_sensor,freq);
    pool.wait_completion()







        
