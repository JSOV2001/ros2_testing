#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from ros2_basics_interfaces.action import CountUntil
from rclpy.action.client import ClientGoalHandle

class CountUntilClient(Node):
    def __init__(self):
        super().__init__('count_until_client')

        # Convert node into a client that matches action's type and name
        self.count_until_client = ActionClient(self, CountUntil, "/count_until")
        print("Initializing action client")
    
    # Define protoccol for sending goal
    def send_goal(self, target_number, period):
        # Wait for the server
        self.count_until_client.wait_for_server()

        # Initialize the goal
        goal_msg = CountUntil.Goal()
        goal_msg.target_number = target_number
        goal_msg.period = period
        
        # Send the goal
        # self.count_until_client.send_goal_async(goal_msg, self.get_feedback).add_done_callback(self.get_goal_status)
        
        # Create a future possible response using an asynchronous call,
        # with no risk of blocking other ROS and non-ROS processes
        self.goal_sender_future = self.count_until_client.send_goal_async(goal_msg, self.get_feedback)
        self.goal_sender_future.add_done_callback(self.get_goal_status)    
    
    # Define protoccol for getting the goal status from the server
    def get_goal_status(self, status_future_msg):
        self.goal_handle: ClientGoalHandle = status_future_msg.result()
        if self.goal_handle.accepted:
            # self.goal_handle.get_result_async().add_done_callback(self.get_goal_result)
            self.result_getter_future = self.goal_handle.get_result_async()
            self.result_getter_future.add_done_callback(self.get_goal_result)
    
    # Define protoccol for getting the result from the server
    def get_goal_result(self, result_future_msg):
        result_msg = result_future_msg.result().result
        print(f"Result: {result_msg.reached_number}")
    
    # Define protoccol for getting feedback from the server
    def get_feedback(self, feedback_msg):
        feedback_msg = feedback_msg.feedback
        print(f"Feedback: {feedback_msg.current_number}")

def main():
    rclpy.init()
    count_until_client_node = CountUntilClient()
    target_number = 5
    period = 1.0
    try:
        print(f"Go up to {target_number} every {period} seconds")
        count_until_client_node.send_goal(target_number, period)
        rclpy.spin(count_until_client_node)
    except KeyboardInterrupt:
        count_until_client_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()