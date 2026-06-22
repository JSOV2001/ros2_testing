#!/usr/bin/env python3
import pytest
import rclpy
from scripts.trigger_server import TriggerServer
from scripts.trigger_client import TriggerClient
from rclpy.executors import SingleThreadedExecutor
import threading

# ========== Testing. Phase 1: Arrange ==========
@pytest.fixture
def rclpy_init():
    # Open ROS2 communication
    rclpy.init()

def spin_executor(executor):
    executor.spin()

@pytest.fixture
def server():
    # Call server from Trigger service
    server_node = TriggerServer()
    
    # Initialize a parallel thread to execute server
    server_executor = SingleThreadedExecutor()
    server_executor.add_node(server_node)
    server_thread = threading.Thread(target= spin_executor, args=(server_executor,))
    return server_node, server_thread, server_executor

def test_service(rclpy_init, server):
    try:
        # ========== Testing. Phase 2: Act ==========

        # Execute Trigger server in a parallel thread
        server_node, server_thread, server_executor = server
        server_thread.start()

        # Call client from Trigger service
        client_node = TriggerClient()

        # Request response from server
        response_future = client_node.client.call_async(client_node.request_msg_)
        rclpy.spin_until_future_complete(client_node, response_future, timeout_sec= 2)
        response_msg = response_future.result()

        # ========== Testing. Phase 3: Assert ==========

        # Check if each node has the expected name
        assert client_node.get_name() == 'trigger_client'
        assert server_node.get_name() == 'trigger_server'

        # Check if the node has the correct atribute
        assert hasattr(client_node, 'client')
        assert hasattr(server_node, 'server')

        # Check if the node shares the correct service and message
        assert server_node.server.srv_name == client_node.client.srv_name
        assert server_node.server.srv_type == client_node.client.srv_type
        
        # Check if the client provide the correct response
        assert response_msg.success
        assert response_msg.message == 'Service executed successfully'
    finally:
    # Close ROS2 communication
        server_node.destroy_node()
        client_node.destroy_node()
        server_executor.shutdown()
        rclpy.shutdown()
