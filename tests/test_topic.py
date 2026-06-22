#!/usr/bin/env python3
import pytest
import rclpy
from std_msgs.msg import String
from scripts.talker import Talker
from scripts.listener import Listener

# ========== Testing. Phase 1: Arrange ==========
@pytest.fixture
def rclpy_init():
    # Open ROS2 comunication
    rclpy.init()

@pytest.fixture
def pub_node():
    # Call publisher
    return Talker()

@pytest.fixture
def sub_node():
    # Call subscriber
    return Listener()

# ========== Testing. Phase 2: Act ==========
def test_talker_listener(rclpy_init, pub_node, sub_node):
    try:
        # ========== Testing. Phase 3: Assert ==========
        
        # Check if node has the expected name
        assert pub_node.get_name() == 'talker'
        assert sub_node.get_name() == 'listener'
        
        # Check if each node has the correct atribute
        assert hasattr(pub_node, 'publisher_')
        assert hasattr(sub_node, 'subscription_')
        
        # Check if the publisher and subscriber share the same topic and message
        assert pub_node.publisher_.topic_name == sub_node.subscription_.topic_name
        assert pub_node.publisher_.msg_type == sub_node.subscription_.msg_type

        # Check if the publisher has a subscriber
        subscribers_amount = pub_node.publisher_.get_subscription_count()
        assert subscribers_amount == 1
    finally:
        # Close ROS2 communication
        rclpy.shutdown()
