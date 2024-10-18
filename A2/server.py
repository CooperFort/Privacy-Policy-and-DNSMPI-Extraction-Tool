import socket
import threading
import sys
import os

# List to keep track of connected clients
clients = []
output_file = "server_output.txt"

# Write initial info to the output file (HawkID and Name)
def initialize_output():
    with open(output_file, "w") as f:
        f.write("HawkID: bschlachtenhaufen\n")
        f.write("Name: Benjamin Schlachtenhaufen\n\n")
        f.write("Server Logs:\n")

def log_to_file(message):
    with open(output_file, "a") as f:
        f.write(message + "\n")

def handle_client(client_socket, client_address):
    try:
        log_to_file(f"[Info] Client {client_address} connected.")
        clients.append(client_socket)

        while True:
            try:
                # Receive message from the client
                message = client_socket.recv(1024).decode('utf-8')

                if not message:
                    break  # Client has disconnected
                if message == "/quit":
                    break  # Client sent /quit to disconnect

                log_to_file(f"[Received] {client_address}: {message}")
                print(f"[Received] {client_address}: {message}")

                # Broadcast the message to all other clients except the sender
                broadcast_message(f"{client_address} says: {message}", client_socket)
            except Exception as e:
                error_msg = f"[Error] Issue with client {client_address}: {str(e)}"
                log_to_file(error_msg)
                print(error_msg)
                break
    finally:
        # Clean up: Remove the client and close the connection
        log_to_file(f"[Info] Client {client_address} disconnected.")
        print(f"[Info] Client {client_address} disconnected.")
        clients.remove(client_socket)
        client_socket.close()

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                error_msg = f"[Error] Failed to send message to a client: {str(e)}"
                log_to_file(error_msg)
                print(error_msg)
                client.close()
                clients.remove(client)

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_socket.bind(('localhost', port))
        server_socket.listen(5)
        print(f"Server started on port {port}. Listening for connections...")
        log_to_file(f"Server started on port {port}. Listening for connections...")

        while True:
            try:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()
            except Exception as e:
                error_msg = f"[Error] Error accepting client: {str(e)}"
                log_to_file(error_msg)
                print(error_msg)
    except Exception as e:
        error_msg = f"[Error] Failed to start server: {str(e)}"
        log_to_file(error_msg)
        print(error_msg)
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[Error] Usage: python3 server.py <port>")
        sys.exit(1)
    
    try:
        port = int(sys.argv[1])
        initialize_output()
        start_server(port)
    except ValueError:
        print("[Error] Invalid port number.")
        sys.exit(1)
