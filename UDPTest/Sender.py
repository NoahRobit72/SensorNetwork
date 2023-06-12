import socket

target_ip = "192.168.12.32"  # Replace with the recipient's IP address
target_port = 9999  # Replace with the recipient's port number

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Enter a message: ")
    sock.sendto(message.encode(), (target_ip, target_port))

sock.close()