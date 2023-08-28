import socket

server = socket.socket()
server.bind(("0.0.0.0", 2900))

server.listen()

while True:
	client, addr = server.accept()
	print("Connection from", addr)
	client.send("Welcome to lazy-investor!\n".encode())
	client.close()
