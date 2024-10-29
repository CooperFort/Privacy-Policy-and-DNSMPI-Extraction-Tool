import sys
import time
import socket
import dpkt

def checksum(data):
    """Calculates the checksum of the provided data."""
    total = 0
    count = 0
    while count < len(data):
        total += (data[count] << 8) + (data[count + 1] if count + 1 < len(data) else 0)
        total &= 0xFFFFFFFF  # Keep total to 32 bits
        count += 2
    total = (total >> 16) + (total & 0xFFFF)  # Fold 32 bits to 16 bits
    total += (total >> 16)  # Fold again to get 16 bits
    return ~total & 0xFFFF  # Return the 16-bit checksum

def make_icmp_socket(ttl, timeout):
    """Creates a raw ICMP socket with the specified TTL and timeout."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    sock.settimeout(timeout)
    return sock

def send_icmp_echo(sock, payload, packet_id, seq, destination):
    """Sends an ICMP Echo request."""
    icmp = dpkt.icmp.ICMP(type=dpkt.icmp.ICMP_ECHO, code=0)  # ICMP Echo request
    icmp.id = packet_id
    icmp.seq = seq
    icmp.data = payload

    # Prepare the ICMP packet
    packet = bytes(icmp)
    icmp.cksum = checksum(packet)  # Calculate checksum
    packet = bytes(icmp)  # Repack ICMP with checksum

    # Send the packet
    try:
        sock.sendto(packet, (destination, 1))  # Port 1 is used for ICMP
        print(f"Sent ICMP Echo Request: TTL={ttl}, ID={packet_id}, SEQ={seq}, DEST={destination}")
    except Exception as e:
        print(f"Failed to send ICMP Echo Request: {e}")

def recv_icmp_response(sock, packet_id):
    """Receives an ICMP response."""
    start_time = time.time()  # Record the start time
    try:
        data, addr = sock.recvfrom(1024)  # Receive data from the socket
        ip = dpkt.ip.IP(data)  # Unpack the IP packet
        icmp = dpkt.icmp.ICMP(ip.data)  # Extract ICMP from the IP packet
        
        # Check if we have a valid ICMP response
        if isinstance(icmp, dpkt.icmp.ICMP) and hasattr(icmp, 'type'):
            rtt = (time.time() - start_time) * 1000  # Calculate RTT in ms
            print(f"Received ICMP Response: Type={icmp.type}, Code={icmp.code}, ID={icmp.id}, SEQ={icmp.seq}")

            # Check if the response is an Echo Reply
            if icmp.type == dpkt.icmp.ICMP_ECHOREPLY and icmp.seq == packet_id:
                return addr, rtt  # Return the address and RTT
            elif icmp.type == dpkt.icmp.ICMP_TIMEXCEED:
                return addr, rtt  # Handle time exceeded response
    except socket.timeout:
        return None, None  # Timeout occurred
    except Exception as e:
        print(f"Error receiving ICMP response: {e}")

    return None, None  # Return None if no valid response

def main():
    # Parse command-line arguments
    if len(sys.argv) != 5 or sys.argv[1] != '-destination' or sys.argv[3] != '-n_hops':
        print("Usage: python3 cs3640-traceroute.py -destination <ip> -n_hops <number>")
        sys.exit(1)

    destination = sys.argv[2]
    max_hops = int(sys.argv[4])  # Get the number of hops from arguments

    print(f"Tracing route to {destination}")

    for ttl in range(1, max_hops + 1):
        # Create the socket
        sock = make_icmp_socket(ttl, timeout=2)

        # Prepare payload and packet ID
        payload = b'Ping'
        packet_id = ttl  # Use TTL as packet ID for simplicity

        # Send ICMP Echo
        send_icmp_echo(sock, payload, packet_id, ttl, destination)

        # Receive response
        addr, rtt = recv_icmp_response(sock, packet_id)

        if addr:
            print(f"destination = {destination}; hop {ttl} = {addr[0]}; rtt = {rtt:.2f} ms")
        else:
            print(f"destination = {destination}; hop {ttl} = timeout")

        sock.close()

if __name__ == "__main__":
    main()
