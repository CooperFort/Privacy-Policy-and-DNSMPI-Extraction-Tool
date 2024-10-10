import argparse
from iperf3 import Server

def run_server():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True, help='Server IP address')
    parser.add_argument('--port', type=int, default=5201, help='iPerf server port')
    args = parser.parse_args()

    server = Server()
    server.bind_address = args.ip
    server.port = args.port
    server.run()

if __name__ == '__main__':
    run_server()
