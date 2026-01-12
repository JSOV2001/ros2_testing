#!/usr/bin/env python3
import pytest
import rclpy
from trigger_server import TriggerServer
from trigger_client import TriggerClient
from rclpy.executors import SingleThreadedExecutor
import threading

# ========== Testing. Fase 1: Organizar ==========
@pytest.fixture
def rclpy_init():
    # Abrir la comunicacion de ROS2
    rclpy.init()

def spin_executor(executor):
    executor.spin()

@pytest.fixture
def server():
    # Invocar servidor para el servicio Trigger
    server_node = TriggerServer()

    # Inicializar un hilo paralelo para ejecutar servidor
    server_executor = SingleThreadedExecutor()
    server_executor.add_node(server_node)
    server_thread = threading.Thread(target= spin_executor, args=(server_executor,))
    return server_node, server_thread

def test_service_response(rclpy_init, server):
    try:
        # ========== Testing. Fase 2: Actuar ==========

        # Ejecutar servidor del servicio Trigger en un hilo paralelo
        server_node, server_thread = server
        server_thread.start()

        # Invocar cliente del servicio Trigger
        client_node = TriggerClient()

        # Realizar la solicitud al servicio
        response_future = client_node.client.call_async(client_node.request_msg_)
        rclpy.spin_until_future_complete(client_node, response_future, timeout_sec= 2)
        response_msg = response_future.result()

        # ========== Testing. Fase 3: Afimar ==========

        # Verificar que cada nodo tiene el nombre esperado
        assert client_node.get_name() == 'trigger_client'
        assert server_node.get_name() == 'trigger_server'

        # Verificar que cada nodo tiene el nombre esperado
        assert hasattr(client_node, 'client')
        assert hasattr(server_node, 'server')

        # Verificar que ambos nodos comparten el mismo servicio y mensaje
        assert server_node.server.srv_name == client_node.client.srv_name
        assert server_node.server.srv_type == client_node.client.srv_type

        # Verificar la respuesta del cliente
        assert response_msg.success
        assert response_msg.message == 'Service executed successfully'
    finally:
        # Cerrar la comunicacion de ROS2
        rclpy.shutdown()
