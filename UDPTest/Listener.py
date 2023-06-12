import socket

host = "0.0.0.0"  # Listen on all available network interfaces
port = 8888  # Port to listen on

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

print(f"Listening for UDP messages on {host}:{port}")

while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode()
    print(f"Received message: {message} from {addr[0]}:{addr[1]}")

sock.close()