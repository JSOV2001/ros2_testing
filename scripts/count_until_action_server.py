#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from ros2_basics_interfaces.action import CountUntil
from rclpy.action.server import ServerGoalHandle, GoalResponse, CancelResponse
import time

class CountUntilServer(Node):
    def __init__(self):
        super().__init__('count_until_server')
        
        # Convert node into a server with a specific type and name
        self.count_until_server = ActionServer(
            node = self,
            action_type = CountUntil,
            action_name = "/count_until",
            execute_callback = self.execute_accepted_goal,
            goal_callback= self.set_goal_status,
            cancel_callback= self.cancel_goal
        )
        print("Initializing action server")
    
    def set_goal_status(self, goal_request):
        # Get goal
        target_number = goal_request.target_number
        period = goal_request.period

        # Define if goal is acceptable or not
        if target_number > 5 or target_number < 0:
            return GoalResponse.REJECT
        elif period > 1.0 or period <= 0.0:
            return GoalResponse.REJECT
        else:
            return GoalResponse.ACCEPT
    
    def cancel_goal(self, goal_handle):
        print("Canceling goal")
        return CancelResponse.ACCEPT
    
    # Define protoccol for executing accepted-only goals,
    # and getting result and feedback
    def execute_accepted_goal(self, goal_handle: ServerGoalHandle):
        # Get goal
        target_number = goal_handle.request.target_number
        period = goal_handle.request.period

        # Declare feedback and result
        feedback_msg = CountUntil.Feedback()
        result_msg = CountUntil.Result()
        
        # Process goal
        counter = 0
        print(f"Server executing goal:")
        for i in range(target_number):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return result_msg

            counter += 1
            
            # Publish feedback meanwhile
            feedback_msg.current_number = counter
            goal_handle.publish_feedback(feedback_msg)
            print(f"Server's Current Number #{i}: {counter}")
            time.sleep(period)
        
        # As the goal processing is done
        # Send goal's status to the client
        goal_handle.succeed()

        # Initialize and return result
        result_msg.reached_number = counter
        print("Goal succeeded on Server's side")
        return result_msg

def main():
    rclpy.init()
    count_until_server_node = CountUntilServer()
    try:
        rclpy.spin(count_until_server_node)
    except KeyboardInterrupt:
        count_until_server_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
