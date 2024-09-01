import socket
import cv2
import struct
import pickle
import numpy as np

def start_video_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        try:
            # Certifique-se de que recebemos o tamanho completo da mensagem
            while len(data) < payload_size:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet

            if len(data) < payload_size:
                print("Conexão fechada pelo servidor.")
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            # Receber o quadro completo
            while len(data) < msg_size:
                data += client_socket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            cv2.imshow("Cliente Streaming", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"Erro durante o streaming: {e}")
            break

    client_socket.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    server_ip = '192.168.0.7'  # Substitua pelo IP do servidor
    server_port = 5002
    start_video_client(server_ip, server_port)
