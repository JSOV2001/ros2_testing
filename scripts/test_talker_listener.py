#!/usr/bin/env python3
import pytest
import rclpy
from std_msgs.msg import String
from talker import Talker
from listener import Listener

# ========== Testing. Fase 1: Organizar ==========
@pytest.fixture
def rclpy_init():
    # Abrir la comunicacion de ROS2
    rclpy.init()

@pytest.fixture
def pub_node():
    # Invoca publicador
    return Talker()

@pytest.fixture
def sub_node():
    # Invoca suscriptor
    return Listener()

# ========== Testing. Fase 2: Actuar ==========
def test_talker_listener(rclpy_init, pub_node, sub_node):
    try:
        # ========== Testing. Fase 3: Afimar ==========

        # Verifica que cada nodo tiene el nombre esperado
        assert pub_node.get_name() == 'talker'
        assert sub_node.get_name() == 'listener'
 
        # Verifica que cada nodo tiene el atributo correcto
        assert hasattr(pub_node, 'publisher_')
        assert hasattr(sub_node, 'subscription_')

        # Verifica que el publicador y el suscriptor comparten el mismo topico y mensaje
        assert pub_node.publisher_.topic_name == sub_node.subscription_.topic_name
        assert pub_node.publisher_.msg_type == sub_node.subscription_.msg_type

        # Verifica que el publicador tenga un suscriptor
        subscribers_amount = pub_node.publisher_.get_subscription_count()
        assert subscribers_amount == 1
    finally:
        # ========== Testing. Fase 4: Limpiar ==========
        
        # Cerrar la comunicacion de ROS2
        rclpy.shutdown()