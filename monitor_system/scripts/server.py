import socket
import psutil
import json
import time

def get_system_stats():
    # Coletar informações do sistema
    stats = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'uptime': time.time() - psutil.boot_time()
    }
    return stats

def start_monitoring_server(host='0.0.0.0', port=5001):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor de monitoramento iniciado em {host}:{port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão estabelecida com {client_address}")

        while True:
            try:
                stats = get_system_stats()
                # Converter o dicionário para JSON e enviar para o cliente
                client_socket.send(json.dumps(stats).encode())
                time.sleep(1)
            except (BrokenPipeError, ConnectionResetError):
                print(f"Conexão perdida com {client_address}")
                break

        client_socket.close()

if __name__ == "__main__":
    start_monitoring_server()
