import socket

def send_udp_message(message, ip_address, port):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Send the UDP packet
    client_socket.sendto(message.encode(), (ip_address, port))
    
    # Close the socket
    client_socket.close()

# Usage example
message = "Hello, receiver!"
ip_address = "localhost"  # Replace with the receiver's IP address
port = 8888

send_udp_message(message, ip_address, port)
