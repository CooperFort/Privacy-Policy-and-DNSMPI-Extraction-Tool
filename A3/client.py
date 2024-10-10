import argparse
from iperf3 import Client
import os
import json

def run_client():
    # Set up argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True, help='Client IP address')
    parser.add_argument('--port', type=int, default=5201, help='Client port')
    parser.add_argument('--server_ip', type=str, required=True, help='Server IP address')
    parser.add_argument('--test', type=str, choices=['tcp', 'udp'], required=True, help='Test type (tcp or udp)')
    parser.add_argument('--bottleneck_bw', type=int, required=True, help='Bottleneck link bandwidth in Mbps')
    parser.add_argument('--other_bw', type=int, required=True, help='Other links bandwidth in Mbps')
    args = parser.parse_args()

    # Initialize client with parsed arguments
    client = Client()
    client.server_hostname = args.server_ip
    client.port = args.port
    client.protocol = args.test
    client.duration = 60  # Set duration to 60 seconds as per assignment

    # Run the client and collect results
    result = client.run()
    if result.error:
        print(f"Error: {result.error}")
    else:
        # Extract total bytes sent and received
        total_bytes_sent = result.sent_bytes
        total_bytes_received = result.received_bytes

        # Create a dictionary with meaningful keys
        output_data = {
            'total_bytes_sent': total_bytes_sent,
            'total_bytes_received': total_bytes_received,
            'protocol': args.test,
            'duration': client.duration,
            'server_ip': args.server_ip,
            'client_ip': args.ip,
            'bits_per_second': result.sent_Mbps * 1e6  # Convert Mbps to bps
        }

        # Define the output file path
        bottleneck_bw = args.bottleneck_bw
        other_bw = args.other_bw
        output_file_path = f"output-{args.test}-{bottleneck_bw}-{other_bw}.json"

        # Attempt to write results to the output file with error handling
        try:
            print(f"Attempting to write to file: {output_file_path}")
            with open(output_file_path, 'w') as file:
                json.dump(output_data, file, indent=4)
            print("File written successfully.")
        except Exception as e:
            print(f"An error occurred while writing the file: {e}")

    # Print the current working directory for confirmation
    print("Current working directory:", os.getcwd())

if __name__ == '__main__':
    run_client()
