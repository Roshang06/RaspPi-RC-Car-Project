import socket

raspberrypi_IP = '192.168.68.128'  # Replace with your Raspberry Pi’s IP address
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello from laptop")
    data = s.recv(1024)

print(f"Received from server: {data.decode()}")