# locust-grpc-advanced.py
"""
Teste de Carga Avançado para gRPC com múltiplos cenários
"""

import grpc
import time
import random
from locust import User, task, events, between
from locust_global_time import StepLoadShape

try:
    import music_service_pb2
    import music_service_pb2_grpc
except ImportError:
    print("ERRO: Execute: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. music_service.proto")
    exit(1)


class GrpcClient:
    """Cliente gRPC otimizado com pool de conexões"""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._channel = None
        self._stub = None
        self.connect()
    
    def connect(self):
        # Configurações otimizadas para testes de carga
        options = [
            ('grpc.max_send_message_length', 10 * 1024 * 1024),
            ('grpc.max_receive_message_length', 10 * 1024 * 1024),
            ('grpc.keepalive_time_ms', 10000),
            ('grpc.keepalive_timeout_ms', 5000),
        ]
        self._channel = grpc.insecure_channel(
            f'{self.host}:{self.port}',
            options=options
        )
        self._stub = music_service_pb2_grpc.MusicServiceStub(self._channel)
    
    def close(self):
        if self._channel:
            self._channel.close()
    
    def _make_request(self, method_name, request, metadata=None):
        start_time = time.time()
        response = None
        exception = None
        
        try:
            method = getattr(self._stub, method_name)
            response = method(request, metadata=metadata, timeout=10)
        except grpc.RpcError as e:
            exception = e
        finally:
            total_time = int((time.time() - start_time) * 1000)
            
            if exception:
                events.request.fire(
                    request_type="grpc",
                    name=method_name,
                    response_time=total_time,
                    response_length=0,
                    exception=exception,
                    context={}
                )
            else:
                response_length = len(response.SerializeToString()) if response else 0
                events.request.fire(
                    request_type="grpc",
                    name=method_name,
                    response_time=total_time,
                    response_length=response_length,
                    exception=None,
                    context={}
                )
        
        return response
    
    def list_users(self):
        request = music_service_pb2.Empty()
        return self._make_request('ListUsers', request)
    
    def list_songs(self):
        request = music_service_pb2.Empty()
        return self._make_request('ListSongs', request)
    
    def list_user_playlists(self, user_id):
        request = music_service_pb2.UserId(id=user_id)
        return self._make_request('ListUserPlaylists', request)


class GrpcUser(User):
    abstract = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if ':' in self.host:
            host, port = self.host.rsplit(':', 1)
        else:
            host = self.host
            port = '50051'
        
        self.client = GrpcClient(host, port)
    
    def on_stop(self):
        self.client.close()


class LightUser(GrpcUser):
    """Usuário leve - apenas consultas simples"""
    weight = 3
    wait_time = between(1, 3)
    
    @task
    def browse(self):
        self.client.list_users()
        self.client.list_songs()


class HeavyUser(GrpcUser):
    """Usuário pesado - consultas complexas e múltiplas"""
    weight = 1
    wait_time = between(0.5, 1.5)
    
    @task
    def intensive_browse(self):
        # Busca múltiplos recursos
        self.client.list_users()
        self.client.list_songs()
        
        # Busca playlists de usuários aleatórios
        for user_id in [1, 2]:
            self.client.list_user_playlists(user_id)


## StepLoadShape agora é importado de locust-global-time.py


# Suprimir logs verbosos do gRPC
import logging
logging.getLogger('grpc').setLevel(logging.ERROR)


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     Teste de Carga gRPC AVANÇADO - Múltiplos Cenários    ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Este script inclui:
    - Usuários leves (70%) e pesados (30%)
    - Formato de carga em degraus (StepLoadShape)
    - Conexões otimizadas com keepalive
    
    Para executar:
       locust -f locust-grpc-advanced.py --host=localhost:50051
    """)
