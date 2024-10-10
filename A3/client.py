import argparse
from iperf3 import Client
import os

def run_client():
    # Set up argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True, help='Server IP address')
    parser.add_argument('--port', type=int, default=5201, help='iPerf server port')
    parser.add_argument('--protocol', type=str, choices=['tcp', 'udp'], default='tcp', help='Protocol to use')
    parser.add_argument('--duration', type=int, default=10, help='Duration of test in seconds')
    args = parser.parse_args()

    # Initialize client with parsed arguments
    client = Client()
    client.server_hostname = args.ip
    client.port = args.port
    client.protocol = args.protocol
    client.duration = args.duration

    # Run the client and collect results
    result = client.run()
    if result.error:
        print(f"Error: {result.error}")
    else:
        print(result.json)

        # Define the output file path
        output_file_path = f"output-tests-{args.protocol}-{args.duration}-bandwidth.txt"

        # Attempt to write results to the output file with error handling
        try:
            print(f"Attempting to write to file: {output_file_path}")
            with open(output_file_path, 'w') as file:
                file.write(str(result.json))
            print("File written successfully.")
        except Exception as e:
            print(f"An error occurred while writing the file: {e}")

    # Print the current working directory for confirmation
    print("Current working directory:", os.getcwd())

if __name__ == '__main__':
    run_client()
