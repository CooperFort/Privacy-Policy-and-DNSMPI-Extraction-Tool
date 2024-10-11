import argparse
from iperf3 import Client
import json
import os


def run_client():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, required=True, help="Client IP address")
    parser.add_argument("--port", type=int, required=True, help="Client port")
    parser.add_argument("--server_ip", type=str, required=True, help="Server IP address")
    parser.add_argument("--test", type=str, choices=["tcp", "udp"], required=True, help="Test type (tcp or udp)")
    parser.add_argument("--bottleneck_bw", type=int, required=True, help="Bottleneck Link bandwidth in Mbps")
    parser.add_argument("--other_bw", type=int, required=True, help="Other Links bandwidth in Mbps")
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
        total_bytes_sent = result.sent_bytes
        total_bytes_received = result.received_bytes

        # Determine bits_per_second based on protocol
        if args.test == "tcp":
            bits_per_second = result.sent_Mbps * 1e6  # Assuming this is valid for TCP
        elif args.test == "udp":
            bits_per_second = result.bps  # Assuming this is valid for UDP

            # UDP-specific metrics
            jitter = result.jitter_ms
            packet_loss = result.lost_percent
        else:
            jitter = None
            packet_loss = None

        output_data = {
            "total_bytes_sent": total_bytes_sent,
            "total_bytes_received": total_bytes_received,
            "protocol": args.test,
            "duration": client.duration,
            "server_ip": args.server_ip,
            "client_ip": args.ip,
            "bits_per_second": bits_per_second,
            "jitter": jitter,
            "packet_loss": packet_loss
        }

        bottleneck_bw = args.bottleneck_bw
        other_bw = args.other_bw
        output_file_path = f"output-{args.test}-{bottleneck_bw}-{other_bw}.json"

        try:
            print(f"Attempting to write to file: {output_file_path}")
            with open(output_file_path, "w") as file:
                json.dump(output_data, file, indent=4)
            print("File written successfully.")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

    print("Current working directory:", os.getcwd())


if __name__ == "__main__":
    run_client()