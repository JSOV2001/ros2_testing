#!/usr/bin/env python3
import pytest
import rclpy
from scripts.count_until_action_server import CountUntilServer
from scripts.count_until_action_client import CountUntilClient
from ros2_basics_interfaces.action import CountUntil
from rclpy.executors import SingleThreadedExecutor
import threading
from rclpy.action.client import ClientGoalHandle

def get_feedback(feedback_msg):
    # Get feedback from the goal
    feedback_msg = feedback_msg.feedback
    print(f"Client's Feedback: {feedback_msg.current_number}")

def get_goal_result(result_future_msg):
    # Get result from the goal
    result_msg = result_future_msg.result().result
    assert goal_msg.target_number == result_msg.reached_number
    print(f"Client's Result: {result_msg.reached_number}")

    # Close ROS2 communication
    server_node.destroy_node()
    client_node.destroy_node()
    server_executor.shutdown()
    client_executor.shutdown()
    rclpy.shutdown()
   
def get_goal_status(status_future_msg):
        # ========== Testing. Phase 3: Assert ==========
        # Assert whether goal was accepted or not
        goal_handle: ClientGoalHandle = status_future_msg.result()
        if goal_handle.accepted:
            assert goal_handle.accepted
            result_getter_future = goal_handle.get_result_async()
            result_getter_future.add_done_callback(get_goal_result)
        else:
            assert not goal_handle.accepted
            print("Not valid goal")

""" def timer_cancel_callback(goal_handle):
    cancel_future = goal_handle.cancel_goal_async()
    cancel_future.add_done_callback(cancel_done)

def cancel_done(self, future):
    cancel_response = future.result()
    
    if len(cancel_response.goals_canceling) > 0:
        self.get_logger().info('Goal successfully canceled')
    else:
        self.get_logger().info('Goal failed to cancel')
    
    server_node.destroy_node()
    client_node.destroy_node()
    server_executor.shutdown()
    client_executor.shutdown()
    rclpy.shutdown() """

# ========== Testing. Phase 1: Arrange ==========
@pytest.fixture
def rclpy_init():
    # Open ROS2 communication
    rclpy.init()

def spin_executor(executor):
    executor.spin()

@pytest.fixture
def action_service():
    # Call server from CountUntil service
    server_node = CountUntilServer()

    # Initialize a parallel thread to execute server
    server_executor = SingleThreadedExecutor()
    server_executor.add_node(server_node)
    server_thread = threading.Thread(target= spin_executor, args=(server_executor,))

    # Execute server in a parallel thread
    server_thread.start()

    # Call client from CountUntil service
    client_node = CountUntilClient()

    # Initialize a parallel thread to execute client
    client_executor = SingleThreadedExecutor()
    client_executor.add_node(client_node)
    client_thread = threading.Thread(target= spin_executor, args=(client_executor,))

    # Execute client in a parallel thread
    client_thread.start()

    return server_node, server_executor, client_node, client_executor

def test_action(rclpy_init, action_service):
    global is_finished
    is_finished = False

    global server_node, server_executor, client_node, client_executor
    server_node, server_executor, client_node, client_executor = action_service

    # ========== Testing. Phase 2: Act ==========

    # Wait for an available server, and
    # assert if action service is available
    is_server_ready = client_node.count_until_client.wait_for_server(timeout_sec= 2)
    assert is_server_ready
    print(f"Server-Client is ready")

    # Initiaize goal
    global goal_msg
    goal_msg = CountUntil.Goal()
    goal_msg.target_number = 5
    goal_msg.period = 1.0
    
    # Request response from server
    print(f"Sending goal to Server: {goal_msg.target_number}, {goal_msg.period}")
    goal_sender_future = client_node.count_until_client.send_goal_async(goal_msg, get_feedback)
    goal_sender_future.add_done_callback(get_goal_status)
