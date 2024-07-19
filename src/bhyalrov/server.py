import socket
from threading import Thread

def handle_client(conn, addr):
    print(f"Connected to the server from: {addr[0]}:{addr[1]}")


def start_server():
    try:
        #return server socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        port = 5760
        server_ip = "127.0.0.1"
        
        #bind the server
        server.bind((server_ip, port))
        
        #server listens for connections
        server.listen(1)
        
        while True:
            print(f"Server is listening on: {server_ip}:{port}")
            
            #accept client connection request
            socket_client, addr = server.accept()
            print(f"The connection accepted from: {addr[0]}:{addr[1]}")
            
            handlerThread = Thread(target=handle_client, args=(socket_client, addr,))
            handlerThread.start()
            handlerThread.join()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()
        print("server is closed")
        
if __name__ == "__main__":
    start_server()