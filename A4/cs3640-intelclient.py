import socket
import sys

def main(intel_server_addr, intel_server_port, domain, service):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((intel_server_addr, intel_server_port))

    command = f"{service}({domain})"
    client.sendall(command.encode())

    response = client.recv(4096).decode()
    print(f"Response from server: {response}")

    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python cs3640-intelclient.py <intel_server_addr> <intel_server_port> <domain> <service>")
        sys.exit(1)

    intel_server_addr = sys.argv[1]
    intel_server_port = int(sys.argv[2])
    domain = sys.argv[3]
    service = sys.argv[4]

    main(intel_server_addr, intel_server_port, domain, service)
