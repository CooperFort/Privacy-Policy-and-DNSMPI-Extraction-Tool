import socket
import ssl
import whois
import dns.resolver

def get_ipv4_address(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return f"IPv4 Address: {result[0].to_text()}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_ipv6_address(domain):
    try:
        result = dns.resolver.resolve(domain, 'AAAA')
        return f"IPv6 Address: {result[0].to_text()}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_tls_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return f"TLS Certificate: {cert}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_hosting_as(domain):
    try:
        # Resolve the IP address for the domain
        ip_address = dns.resolver.resolve(domain, 'A')[0].to_text()
        
        # Use the ipwhois library to perform the WHOIS lookup for AS information
        from ipwhois import IPWhois
        obj = IPWhois(ip_address)
        res = obj.lookup_rdap(asn_methods=["whois", "http"])
        
        # Extract AS information from the WHOIS data
        asn = res.get("asn")
        asn_description = res.get("asn_description")
        
        if asn and asn_description:
            return f"AS: {asn}, Description: {asn_description}"
        else:
            return "Error: AS information could not be determined."
    except dns.resolver.NXDOMAIN:
        return "Error: Domain could not be resolved."
    except ImportError:
        return "Error: ipwhois module is required. Install it with 'pip install ipwhois'."
    except Exception as e:
        return f"Error: {str(e)}"

def get_organization(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                # Check multiple fields for organization name
                org_name = None
                for subject in cert['subject']:
                    for item in subject:
                        if item[0] == 'organizationName':
                            org_name = item[1]
                            break
                        elif item[0] == 'commonName' and org_name is None:
                            org_name = item[1]
                
                if org_name:
                    return f"Organization: {org_name}"
                else:
                    return "Error: Organization or common name not found in certificate."
    except Exception as e:
        return f"Error: {str(e)}"

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    command, domain = request.split()
    
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
    
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5555))
    server_socket.listen(5)
    print("Server started and listening on 127.0.0.1:5555")
    
    while True:
        client_socket, _ = server_socket.accept()
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
