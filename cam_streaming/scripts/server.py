import socket
import cv2
import struct
import pickle

def start_video_server(host='0.0.0.0', port=5002):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor de vídeo iniciado em {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Conexão estabelecida com {client_address}")

    cap = cv2.VideoCapture(0)  # Captura de vídeo da webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Codificar o quadro em formato JPEG
        _, frame_encoded = cv2.imencode('.jpg', frame)
        data = pickle.dumps(frame_encoded)

        # Enviar o tamanho do quadro e o quadro
        message_size = struct.pack("Q", len(data))
        client_socket.sendall(message_size + data)

    client_socket.close()
    cap.release()

if __name__ == "__main__":
    start_video_server()
