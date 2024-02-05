import socket

# Create a TCP/IP socket
server_address = ('', 80)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Accept a connection
    connection, client_address = sock.accept()
    
    try:
        # Receive data from ESP32
        data = b''
        while True:
            chunk = connection.recv(1024)
            if not chunk:
                break
            data += chunk
            
        # Print accelerometer data
        print(data.decode())
        
    finally:
        # Close the connection
        connection.close()

# Clean up the socket
sock.close()
