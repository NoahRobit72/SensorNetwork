import socket

target_ip = "0.0.0.0"  # Replace with the recipient's IP address
target_port = 8888  # Replace with the recipient's port number

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Enter a message: ")
    sock.sendto(message.encode(), (target_ip, target_port))

sock.close()