#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class TriggerServer(Node):
    def __init__(self):
        super().__init__('trigger_server')

        # Servidor que procesa mensajes tipo Trigger
        self.server = self.create_service(Trigger, 'trigger_service', self.trigger_callback)

    def trigger_callback(self, request, response):
        # Asignar el contenido del mensaje
        response.success = True
        response.message = 'Service executed successfully'
        return response

def main(args=None):
    rclpy.init(args=args)
    node = TriggerServer() # Crear una instancia del nodo TriggerServer
    rclpy.spin(node) # Ejecutar el nodo y mantenerlo en funcionamiento
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()