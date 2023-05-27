# import socket module
from socket import *
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
serverPort = 80
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

def response_status(code):
    if code == 200:
        return "HTTP/1.1 200 OK"
    elif code == 404:
        return "HTTP/1.1 404 Not Found"

while True:
    print("ready to serve...")
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\nContent-Type: text/html\r\n\r\n".encode())
        print("Response:", response_status(200))
        print("File Data: \n\n", outputdata, "\n")

         # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        # Send a 404 Not Found HTTP response message to the client
        print("Response:", response_status(404))
        connectionSocket.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())

        # Close the client connection socket
        connectionSocket.close()
serverSocket.close()
sys.exit()
