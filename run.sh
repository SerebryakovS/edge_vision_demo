#!/bin/bash

echo "starting sensors"
./sensor.py 100000 &
sleep 0.1
echo "starting manipulator"
./manipulator.py &
sleep 0.1
echo "starting third_party_server"
./third_party_server.py &
sleep 0.1
echo "starting controller"
./controller.py &
sleep 0.1
