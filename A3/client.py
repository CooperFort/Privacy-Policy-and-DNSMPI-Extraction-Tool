import argparse
from iperf3 import Client
import json
import os

def run_client():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True, help='Client IP address')
    parser.add_argument('--port', type=int, default=5201, help='Client port')
    parser.add_argument('--server_ip', type=str, required=True, help='Server IP address')
    parser.add_argument('--test', type=str, choices=['tcp', 'udp'], required=True, help='Test type (tcp or udp)')
    parser.add_argument('--bottleneck_bw', type=int, required=True, help='Bottleneck Link bandwidth in Mbps')
    parser.add_argument('--other_bw', type=int, required=True, help='Other Links bandwidth in Mbps')
    args = parser.parse_args()

    client = Client()
    client.server_hostname = args.server_ip
    client.port = args.port
    client.protocol = args.test
    client.duration = 60

    result = client.run()
    if result.error:
        print(f"Error: {result.error}")
    else:
        if hasattr(result, 'sent_bytes') and hasattr(result, 'received_bytes'):
            # For TCP
            total_bytes_sent = result.sent_bytes
            total_bytes_received = result.received_bytes
        else:
            # For UDP
            total_bytes_sent = result.bytes
            total_bytes_received = result.bytes
            jitter = result.jitter_ms
            packet_loss = result.lost_percent

        output_data = {
            'total_bytes_sent': total_bytes_sent,
            'total_bytes_received': total_bytes_received,
            'protocol': args.test,
            'duration': client.duration,
            'server_ip': args.server_ip,
            'client_ip': args.ip,
            'bits_per_second': result.bitrate
        }

        if args.test == 'udp':
            output_data['jitter_ms'] = jitter
            output_data['packet_loss'] = packet_loss

        bottleneck_bw = args.bottleneck_bw
        other_bw = args.other_bw
        output_file_path = f"output-{args.test}-{bottleneck_bw}-{other_bw}.json"

        try:
            print(f"Attempting to write to file: {output_file_path}")
            with open(output_file_path, "w") as file:
                json.dump(output_data, file, indent=4)
            print(f"File written successfully: {output_file_path}")
        except Exception as e:
            print(f"An error occurred while writing the file: {e}")

    print(f"Current working directory: {os.getcwd()}")

if __name__ == "__main__":
    run_client()