import argparse
import json
import iperf3

def run_client():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True, help="Client IP address")
    parser.add_argument('--port', type=int, default=5201, help="Client port")
    parser.add_argument('--server_ip', type=str, required=True, help="Server IP address")
    parser.add_argument('--test', type=str, choices=['tcp', 'udp'], required=True, help="Test type (tcp or udp)")
    parser.add_argument('--bottleneck_bw', type=int, required=True, help="Bottleneck Link bandwidth in Mbps")
    parser.add_argument('--other_bw', type=int, required=True, help="Other links bandwidth in Mbps")
    args = parser.parse_args()

    client = iperf3.Client()
    client.server_hostname = args.server_ip
    client.port = args.port
    client.protocol = args.test
    client.duration = 60

    # Run the client and gather results
    result = client.run()
    if result.error:
        print(f"Error: {result.error}")
        return

    # Default values for TCP (they will remain None if TCP is used)
    jitter_ms = None
    packet_loss = None

    if args.test == "tcp":
        # For TCP, gather the relevant metrics
        total_bytes_sent = result.sent_bytes
        total_bytes_received = result.received_bytes
        bits_per_second = result.sent_Mbps * 1e6
    elif args.test == "udp":
        # For UDP, gather relevant metrics
        bits_per_second = result.bps
        jitter_ms = result.jitter_ms
        packet_loss = result.lost_percent
        total_bytes_sent = None  # Not available for UDP
        total_bytes_received = None  # Not available for UDP

    output_data = {
        'total_bytes_sent': total_bytes_sent,
        'total_bytes_received': total_bytes_received,
        'protocol': args.test,
        'duration': client.duration,
        'server_ip': args.server_ip,
        'client_ip': args.ip,
        'bits_per_second': bits_per_second,
        'jitter': jitter_ms,
        'packet_loss': packet_loss
    }

    # Define file path based on parameters
    output_file_path = f"output-{args.test}-{args.bottleneck_bw}-{args.other_bw}.json"

    # Write the output data to JSON file
    try:
        print(f"Attempting to write to file: {output_file_path}")
        with open(output_file_path, 'w') as file:
            json.dump(output_data, file, indent=4)
        print(f"File written successfully: {output_file_path}")
    except Exception as e:
        print(f"An error occurred while writing the file: {e}")

if __name__ == "__main__":
    run_client()