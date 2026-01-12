#!/usr/bin/env python3
import pytest
import rclpy
from std_msgs.msg import String
from talker import Talker

# ========== Testing. Fase 1: Organizar ==========
@pytest.fixture
def rclpy_init():
    # Abrir la comunicacion de ROS2
    rclpy.init()

@pytest.fixture
def pub_node():
    # Invoca publicador
    return Talker()

# ========== Testing. Fase 2: Actuar ==========
def test_talker_publish(rclpy_init, pub_node):
    try: 
        # ========== Testing. Fase 3: Afimar ==========

        # Verifica que cada nodo tiene el nombre esperado
        assert pub_node.get_name() == 'talker'
 
        # Verifica que el nodo tiene el atributo correcto
        assert hasattr(pub_node, 'publisher_')

        # Verifica que el nodo tiene el mismo topico y mensaje
        assert pub_node.publisher_.topic_name == '/chatter'
        assert pub_node.publisher_.msg_type == String
    finally:
        # Cerrar la comunicacion de ROS2
        rclpy.shutdown()
