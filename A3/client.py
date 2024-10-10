import argparse
from iperf3 import Client

def run_client():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True, help='Server IP address')
    parser.add_argument('--port', type=int, default=5201, help='iPerf server port')
    parser.add_argument('--protocol', type=str, choices=['tcp', 'udp'], default='tcp', help='Protocol to use')
    parser.add_argument('--duration', type=int, default=10, help='Duration of test in seconds')
    args = parser.parse_args()

    client = Client()
    client.server_hostname = args.ip
    client.port = args.port
    client.protocol = args.protocol
    client.duration = args.duration

    result = client.run()
    if result.error:
        print(f"Error: {result.error}")
    else:
        print(result.json)
        
        # Save the result to a file
        with open(f'output-tests-{args.protocol}-{args.duration}-bandwidth.txt', 'w') as file:
            file.write(str(result.json))

if __name__ == '__main__':
    run_client()
