import socket
import threading
import sys

# List to keep track of connected clients
clients = []

def handle_client(client_socket, client_address):
    try:
        print(f"[Info] Client {client_address} connected.")
        clients.append(client_socket)

        while True:
            try:
                # Receive message from the client
                message = client_socket.recv(1024).decode('utf-8')

                if not message:
                    break  # Client has disconnected
                if message == "/quit":
                    break  # Client sent /quit to disconnect

                print(f"[Received] {client_address}: {message}")

                # Broadcast the message to all other clients except the sender
                broadcast_message(f"{client_address} says: {message}", client_socket)
            except Exception as e:
                print(f"[Error] Issue with client {client_address}: {str(e)}")
                break
    finally:
        # Clean up: Remove the client and close the connection
        print(f"[Info] Client {client_address} disconnected.")
        clients.remove(client_socket)
        client_socket.close()

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                # Injected flaw: check if client is still connected before broadcasting
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"[Error] Failed to send message to a client: {str(e)}")
                client.close()
                clients.remove(client)

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_socket.bind(('localhost', port))
        server_socket.listen(5)  # Inject flaw: limit backlog to 5 clients
        print(f"Server started on port {port}. Listening for connections...")

        while True:
            try:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()
            except Exception as e:
                print(f"[Error] Error accepting client: {str(e)}")
    except Exception as e:
        print(f"[Error] Failed to start server: {str(e)}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[Error] Usage: python3 server.py <port>")
        sys.exit(1)
    
    try:
        port = int(sys.argv[1])
        start_server(port)
    except ValueError:
        print("[Error] Invalid port number.")
        sys.exit(1)
