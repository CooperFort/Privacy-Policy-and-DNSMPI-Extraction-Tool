import socket
import dns.resolver
import ssl
import whois

def get_ipv4_address(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return str(result[0])
    except Exception as e:
        return f"Error: {str(e)}"

def get_ipv6_address(domain):
    try:
        result = dns.resolver.resolve(domain, 'AAAA')
        return str(result[0])
    except Exception as e:
        return f"Error: {str(e)}"

def get_tls_certificate(domain):
    try:
        cert = ssl.get_server_certificate((domain, 443))
        return cert
    except Exception as e:
        return f"Error: {str(e)}"

def get_hosting_as(domain):
    try:
        ip_address = get_ipv4_address(domain)
        if "Error" in ip_address:
            return ip_address
        w = whois.whois(ip_address)
        return w.asn
    except Exception as e:
        return f"Error: {str(e)}"

def get_organization(domain):
    try:
        cert = ssl.get_server_certificate((domain, 443))
        x509 = ssl.PEM_cert_to_DER_cert(cert)
        return ssl.DER_cert_to_X509(x509).get_subject().CN
    except Exception as e:
        return f"Error: {str(e)}"

def handle_client_connection(client_socket):
    request = client_socket.recv(1024).decode()
    command, domain = request.split("(", 1)
    domain = domain.strip(')')

    if command == "IPV4_ADDR":
        response = get_ipv4_address(domain)
    elif command == "IPV6_ADDR":
        response = get_ipv6_address(domain)
    elif command == "TLS_CERT":
        response = get_tls_certificate(domain)
    elif command == "HOSTING_AS":
        response = get_hosting_as(domain)
    elif command == "ORGANIZATION":
        response = get_organization(domain)
    else:
        response = "Unknown command."

    client_socket.sendall(response.encode())
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))
    server.listen(5)
    print("Listening on port 5555...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client_connection(client_socket)

if __name__ == "__main__":
    main()
