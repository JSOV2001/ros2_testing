#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import time

class TriggerClient(Node):
    def __init__(self):
        super().__init__("trigger_client")
        
        # Cliente que solicita mensajes tipo Trigger
        self.client = self.create_client(Trigger, "trigger_service")

        # Crear el mensaje de solictud de tipo Trigger
        self.request_msg_ = Trigger.Request()
        
        # Verificar si el servicio esta disponible 
        while not self.client.wait_for_service(5):
            print("Service not available. Waiting for it")
            time.sleep(1.0)
        print("Initializing service client")

def main():
    rclpy.init()
    client_node = TriggerClient() # Crear una instancia del nodo TriggerClient
    try:
        data = True
    except KeyboardInterrupt:
        client_node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()