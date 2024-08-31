import socket
import cv2
import numpy as np

def start_image_server(host='0.0.0.0', port=5002):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor de imagens iniciado em {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão estabelecida com {client_address}")

        # Receber o tamanho da imagem
        img_size = int(client_socket.recv(16).decode())
        print(f"Tamanho da imagem: {img_size} bytes")

        # Receber a imagem
        data = b""
        while len(data) < img_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet

        # Converter os bytes recebidos em uma imagem
        np_data = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        # Exibir a imagem
        cv2.imshow('Imagem Recebida', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        client_socket.close()

if __name__ == "__main__":
    start_image_server()
