import socket

def receive_udp_message(port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the specified port
    server_socket.bind(("localhost", port))
    
    # Receive the UDP packet
    message, address = server_socket.recvfrom(1024)
    
    # Print the received message
    print("Received message:", message.decode())
    
    # Close the socket
    server_socket.close()

# Usage example
port = 8888

receive_udp_message(port)
