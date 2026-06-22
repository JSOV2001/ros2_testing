#!/usr/bin/env python3
import pytest
import rclpy
from std_msgs.msg import String
from scripts.talker import Talker

# ========== Testing. Phase 1: Arrange ==========
@pytest.fixture
def rclpy_init():
    # Open ROS2 comunication
    rclpy.init()

@pytest.fixture
def node():
    # Call publisher
    return Talker()

# ========== Testing. Phase 2: Act ==========
def test_node(rclpy_init, node):
    try: 
        # ========== Testing. Phase 3: Assert ==========
        
        # Check if the node has the expected name
        assert node.get_name() == 'talker'
        
        # Check if the node has the correct atribute
        assert hasattr(node, 'publisher_')

        # Check if the node shares the correct topic and message
        assert node.publisher_.topic_name == '/chatter'
        assert node.publisher_.msg_type == String
    finally:
        # Close ROS2 communication
        rclpy.shutdown()