import socket
import sys

def send_request(intel_server_addr, intel_server_port, domain, service):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((intel_server_addr, int(intel_server_port)))
        
        # Send command to server
        command = f"{service} {domain}"
        client_socket.send(command.encode('utf-8'))
        
        # Receive response from server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Response from server: {response}")
        
        client_socket.close()
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 cs3640-intelclient.py <intel_server_addr> <intel_server_port> <domain> <service>")
        sys.exit(1)

    intel_server_addr = sys.argv[1]
    intel_server_port = sys.argv[2]
    domain = sys.argv[3]
    service = sys.argv[4]
    
    send_request(intel_server_addr, intel_server_port, domain, service)
