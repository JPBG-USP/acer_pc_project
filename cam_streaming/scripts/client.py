import socket
import cv2

def send_image(server_ip, server_port, image_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Ler a imagem usando OpenCV
    img = cv2.imread(image_path)

    # Codificar a imagem em formato JPEG
    _, img_encoded = cv2.imencode('.jpg', img)

    # Converter para bytes
    data = img_encoded.tobytes()

    # Enviar o tamanho da imagem
    client_socket.send(str(len(data)).encode().ljust(16))

    # Enviar a imagem
    client_socket.sendall(data)
    print(f"Imagem '{image_path}' enviada com sucesso.")

    client_socket.close()

if __name__ == "__main__":
    server_ip = '192.168.0.7'  # Substitua pelo IP do servidor
    server_port = 5002
    image_path = 'caminho/para/sua/imagem.jpg'  # Substitua pelo caminho da imagem
    send_image(server_ip, server_port, image_path)
