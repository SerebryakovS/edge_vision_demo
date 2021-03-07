#!/bin/bash

echo "starting sensors"
python3 sensor.py 100000 &
sleep 0.1
echo "starting manipulator"
python3 manipulator.py &
sleep 0.1
echo "starting third_party_server"
python3 third_party_server.py &
sleep 0.1
echo "starting controller"
python3 controller.py
