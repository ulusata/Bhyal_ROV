import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8000
    
    try:
        client.connect((server_ip, server_port))
        print(f"Connected to the server: {server_ip}:{server_port}")
        
        while True:
            msg = input("Enter message: ").encode("utf-8")[:1024]
            
            client.send(msg)
            
            response = client.recv(1024).decode("utf-8")
            
            
            if response.lower() == "closed":
                break
            
            print(f"From server: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()