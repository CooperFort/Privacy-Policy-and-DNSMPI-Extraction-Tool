import socket
import threading
import sys

def receive_messages(client_socket):
    while True:
        try:
            # Receive messages from the server
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n[Message Received]: {message}")
        except Exception as e:
            print(f"[Error] Failed to receive message: {str(e)}")
            break

def send_messages(client_socket):
    while True:
        try:
            # Prompt user to enter message
            message = input("> ")
            if message == "/quit":
                print("[Info] Disconnecting from the server...")
                client_socket.send(message.encode('utf-8'))
                break  # Exit the loop and disconnect
            elif not message.strip():
                print("[Error] Cannot send an empty message.")  # Injected flaw: does not prevent empty input
            else:
                client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"[Error] Failed to send message: {str(e)}")
            break

def connect_to_server(server_ip, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")

        # Start a thread to receive messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # Start a thread to send messages
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"[Error] Failed to connect to server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("[Error] Usage: python3 client.py <server_ip> <port>")
        sys.exit(1)
    
    server_ip = sys.argv[1]

    try:
        port = int(sys.argv[2])
        connect_to_server(server_ip, port)
    except ValueError:
        print("[Error] Invalid port number.")
        sys.exit(1)
