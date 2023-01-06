import sys
from socket import *


def server(local_ip, local_port):
    serversocket = socket(AF_INET, SOCK_STREAM)
    try :
        serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serversocket.bind((local_ip, local_port))
        serversocket.listen(5)
        print(f"Starting server on: http://{local_ip}:{local_port}")

        while(1):
            (clientsocket, address) = serversocket.accept()

            rd = clientsocket.recv(5000).decode()
            pieces = rd.split("\n")
            if ( len(pieces) > 0 ) : print(pieces[0])

            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type: text/html; charset=utf-8\r\n"
            data += "\r\n"
            data += "<html><body>Hello World</body></html>\r\n\r\n"
            clientsocket.sendall(data.encode())
            clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt :
        print("\nShutting down...\n");
    except Exception as exc :
        print("Error:\n");
        print(exc)

    serversocket.close()

def main(args):
    local_ip = str(args[0])
    local_port = int(args[1])

    server(local_ip, local_port)

if __name__ == "__main__":
    main(sys.argv[1:])