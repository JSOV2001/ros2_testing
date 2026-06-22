#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        
        # Suscriptor que recibe mensajes tipo String
        self.subscription_ = self.create_subscription(String, 'chatter', self.listener_callback, 10)
        
        # Crear el mensaje de tipo String
        self.received_msg = None
    
    def listener_callback(self, msg):
        # Asignar el contenido del mensaje
        self.received_msg = msg.data

        # Registrar el mensaje recibido en el log de la consola
        self.get_logger().info(f'Received: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    # Crear una instancia del nodo Talker
    node = Listener()
    # Ejecutar el nodo y mantenerlo en funcionamiento
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()