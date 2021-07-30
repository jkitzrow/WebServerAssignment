from socket import *
import sys

# Prepare Socket
port = 80
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', port))
serverSocket.listen(1)


try:
    while True:
        # Establish connection
        print("Ready to serve...")
        connectionSocket, addr = serverSocket.accept()

        print("Recieved Request")

        try:
            message = connectionSocket.recv(1024).decode()

            # Extract file name and open it
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()

            # Send one HTTP header line into socket
            response = "HTTP/1.1 200 OK\n\n"
            connectionSocket.send(response.encode())

            # Send the content of the requested file
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            
            # End HTML message and close connection
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        
        except IOError:
            #Send response message for file not found
            error = "HTTP/1.1 404 NOT FOUND\n\n<h1> Error 404 </h1>File Not Found"
            connectionSocket.send(error.encode())
            connectionSocket.send("\r\n".encode())
            # Close client
            connectionSocket.close()
        
except KeyboardInterrupt:
    pass

print("Keyboard Interrupt")
serverSocket.close()
sys.exit()