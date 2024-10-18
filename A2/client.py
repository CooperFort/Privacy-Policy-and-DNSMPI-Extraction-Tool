import socket
import threading
import sys
import os

output_file = "client_output.txt"

# Write initial info to the output file (HawkID and Name)
def initialize_output():
    with open(output_file, "w") as f:
        f.write("HawkID: bschlachtenhaufen\n")
        f.write("Name: Benjamin Schlachtenhaufen\n\n")
        f.write("Client Logs:\n")

def log_to_file(message):
    with open(output_file, "a") as f:
        f.write(message + "\n")

def receive_messages(client_socket):
    while True:
        try:
            # Receive messages from the server
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n[Message Received]: {message}")
            log_to_file(f"[Message Received]: {message}")
        except Exception as e:
            error_msg = f"[Error] Failed to receive message: {str(e)}"
            log_to_file(error_msg)
            print(error_msg)
            break

def send_messages(client_socket):
    while True:
        try:
            # Prompt user to enter message
            message = input("> ")
            if message == "/quit":
                print("[Info] Disconnecting from the server...")
                client_socket.send(message.encode('utf-8'))
                log_to_file("[Info] Client sent /quit command.")
                break  # Exit the loop and disconnect
            elif not message.strip():
                print("[Error] Cannot send an empty message.")
            else:
                client_socket.send(message.encode('utf-8'))
                log_to_file(f"[Message Sent]: {message}")
        except Exception as e:
            error_msg = f"[Error] Failed to send message: {str(e)}"
            log_to_file(error_msg)
            print(error_msg)
            break

def connect_to_server(server_ip, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")
        log_to_file(f"Connected to server at {server_ip}:{port}")

        # Start a thread to receive messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # Start a thread to send messages
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except Exception as e:
        error_msg = f"[Error] Failed to connect to server: {str(e)}"
        log_to_file(error_msg)
        print(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("[Error] Usage: python3 client.py <server_ip> <port>")
        sys.exit(1)
    
    server_ip = sys.argv[1]

    try:
        port = int(sys.argv[2])
        initialize_output()
        connect_to_server(server_ip, port)
    except ValueError:
        print("[Error] Invalid port number.")
        sys.exit(1)
