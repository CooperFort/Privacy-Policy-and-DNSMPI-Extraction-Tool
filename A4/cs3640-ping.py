import socket
import time
import struct
import argparse
import dpkt  # Make sure dpkt is installed: pip install dpkt

# 1. Function to create ICMP socket with TTL and timeout
def make_icmp_socket(ttl, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        sock.settimeout(timeout)
        return sock
    except socket.error as e:
        print(f"[Error] Could not create socket: {e}")
        return None

# 2. Function to create and send ICMP Echo packet
def send_icmp_echo(sock, payload, id, seq, destination):
    icmp_packet = dpkt.icmp.ICMP.Echo(id=id, seq=seq, data=payload)
    icmp = dpkt.icmp.ICMP(type=8, code=0, data=icmp_packet)  # Type 8 is Echo Request
    packet = bytes(icmp)
    sock.sendto(packet, (destination, 1))

# 3. Function to receive ICMP response and calculate RTT
def recv_icmp_response(sock, start_time):
    try:
        data, _ = sock.recvfrom(1024)
        end_time = time.time()
        rtt = (end_time - start_time) * 1000  # RTT in milliseconds
        return rtt, True
    except socket.timeout:
        print("[Error] Request timed out.")
        return None, False

# Main function to handle pinging
def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="ICMP Ping program")
    parser.add_argument('-destination', type=str, required=True, help="Destination IP to ping")
    parser.add_argument('-n', type=int, default=4, help="Number of packets to send")
    parser.add_argument('-ttl', type=int, default=64, help="Time to Live for packets")
    args = parser.parse_args()

    # Initialize variables
    destination = args.destination
    n = args.n
    ttl = args.ttl
    timeout = 1  # 1 second timeout for replies

    # Attempt to create socket
    sock = make_icmp_socket(ttl, timeout)
    if not sock:
        return

    # Ping loop
    total_rtt = 0
    successful_pings = 0

    for seq in range(n):
        # Send ICMP packet
        send_icmp_echo(sock, b"Ping data", id=seq, seq=seq, destination=destination)
        start_time = time.time()

        # Receive ICMP response
        rtt, success = recv_icmp_response(sock, start_time)
        if success:
            total_rtt += rtt
            successful_pings += 1
            print(f"destination = {destination}; icmp_seq = {seq}; ttl = {ttl}; rtt = {rtt:.2f} ms")
        else:
            print(f"destination = {destination}; icmp_seq = {seq}; ttl = {ttl}; Request timed out")

    # Summary of results
    if successful_pings > 0:
        avg_rtt = total_rtt / successful_pings
        print(f"Average rtt: {avg_rtt:.2f} ms; {successful_pings}/{n} successful pings")
    else:
        print("[Error] No responses received")

    sock.close()

if __name__ == "__main__":
    main()
