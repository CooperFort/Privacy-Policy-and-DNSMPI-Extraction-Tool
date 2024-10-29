import socket
import struct
import time
import argparse

def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    return sock

def send_icmp_request(sock, destination, ttl, packet_id, sequence):
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    packet = struct.pack("bbHHh", 8, 0, 0, packet_id, sequence)  # ICMP Echo Request
    sock.sendto(packet, (destination, 1))  # Send to destination

    print(f"Sent ICMP Echo Request: TTL={ttl}, ID={packet_id}, SEQ={sequence}, DEST={destination}")

def receive_icmp_response(sock, expected_id):
    try:
        packet, addr = sock.recvfrom(1024)
        icmp_header = packet[20:28]  # Get the ICMP header
        icmp_type, code, checksum, p_id, seq = struct.unpack("bbHHh", icmp_header)

        # Check if it's an Echo Reply (type 0) or Time Exceeded (type 11)
        if icmp_type in [0, 11]:
            print(f"Received ICMP packet from {addr[0]} (Type: {icmp_type}, ID: {p_id})")
            return True
        else:
            print(f"Received ICMP packet with different Type: {icmp_type} (expected ID: {expected_id})")
            return False

    except socket.timeout:
        print("Timeout waiting for response")
        return False
    except Exception as e:
        print(f"Error processing response: {e}")
        return False

def traceroute(destination, n_hops):
    sock = create_socket()
    sock.settimeout(5)  # Set a timeout of 5 seconds for receiving responses

    for ttl in range(1, n_hops + 1):
        send_icmp_request(sock, destination, ttl, ttl, ttl)
        time.sleep(1)  # Wait for a second before receiving

        # Retry receiving response up to 2 times for each hop
        response_received = False
        for _ in range(2):
            if receive_icmp_response(sock, ttl):
                print(f"Received response at hop {ttl}")
                response_received = True
                break
            else:
                print(f"destination = {destination}; hop {ttl} = timeout (retrying...)")

        if not response_received:
            print(f"destination = {destination}; hop {ttl} = final timeout")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traceroute implementation using ICMP")
    parser.add_argument("-destination", type=str, required=True, help="Destination IP address")
    parser.add_argument("-n_hops", type=int, required=True, help="Number of hops")
    args = parser.parse_args()

    print(f"Tracing route to {args.destination}")
    traceroute(args.destination, args.n_hops)
