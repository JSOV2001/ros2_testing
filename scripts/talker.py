#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        
        # Publicador que envía mensajes tipo String
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        
        # Temporizador que llama al callback cada 1 segundo  
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        # Crear el mensaje de tipo String
        msg = String()

        # Asignar el contenido del mensaje
        msg.data = 'Hello, ROS 2!'

        # Publicar el mensaje en el topic 'chatter'
        self.publisher_.publish(msg)  

        # Registrar el mensaje publicado en el log de la consola
        self.get_logger().info(f'Publishing: {msg.data}')  

def main(args=None):
    rclpy.init()
    # Crear una instancia del nodo Talker
    node = Talker()
    # Ejecutar el nodo y mantenerlo en funcionamiento
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()