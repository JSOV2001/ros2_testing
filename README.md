# ros2_testing
This repository contains unit tests on basic ROS2 nodes, topics, services, and actions.

Firstly, get to the tests folder within the ROS2 package

    cd ros2_ws/src/ros2_testing/tests/

Then, execute the desired test.

## Test for basic node.

    python -m pytest -s test_node.py

## Test for basic topic

    python -m pytest -s test_topic.py

## Test for basic services

    python -m pytest -s test_service.py

## Test for basic actions

    python -m pytest -s test_action.py

