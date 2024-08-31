import socket
import cv2
import struct
import pickle

def start_video_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        # Codificar o quadro em JPEG
        _, frame_encoded = cv2.imencode('.jpg', frame)
        data = pickle.dumps(frame_encoded)

        # Enviar o tamanho do quadro e o quadro em si
        message_size = struct.pack("Q", len(data))
        client_socket.sendall(message_size + data)

        cv2.imshow("Cliente Streaming", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    client_socket.close()
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    server_ip = '192.168.0.7'  # Substitua pelo IP do servidor
    server_port = 5002
    start_video_client(server_ip, server_port)
