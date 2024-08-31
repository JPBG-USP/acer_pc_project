import socket
import json

def monitor_system(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    try:
        while True:
            # Receber os dados do servidor
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Converter JSON de volta para um dicionário
            stats = json.loads(data)
            print(f"Uso de CPU: {stats['cpu_percent']}%")
            print(f"Uso de Memória: {stats['memory_percent']}%")
            print(f"Uso de Disco: {stats['disk_usage']}%")
            print(f"Uptime: {stats['uptime'] // 3600} horas {stats['uptime'] // 60 % 60} minutos")
            print("=" * 40)
    except KeyboardInterrupt:
        print("Monitoramento interrompido.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    server_ip = '192.168.0.7'  # Substitua pelo IP do servidor
    server_port = 5001
    print(f"Cliente de monitoramento iniciado em {server_ip}:{server_port}")
    monitor_system(server_ip, server_port)
