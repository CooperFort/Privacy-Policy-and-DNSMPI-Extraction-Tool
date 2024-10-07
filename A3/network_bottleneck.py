### Task 1: Creating a Network Topology in Mininet
# network_bottleneck.py
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI
import argparse
import json
import os
import time

# Task 1: Define the network topology with bottleneck and other links
class NetworkBottleneck(Topo):
    def build(self, bwBottleneck=10, bwOther=100):
        # Create Hosts and Switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        server1 = self.addHost('server1')
        server2 = self.addHost('server2')

        # Add Links with Bandwidth Constraints
        self.addLink(h1, s1, cls=TCLink, bw=bwOther)
        self.addLink(h2, s1, cls=TCLink, bw=bwOther)
        self.addLink(s1, s2, cls=TCLink, bw=bwBottleneck)  # Bottleneck link
        self.addLink(s2, server1, cls=TCLink, bw=bwOther)
        self.addLink(s2, server2, cls=TCLink, bw=bwOther)

# Task 2: Run tests on the network to evaluate performance
# This includes ping tests and iPerf tests between nodes
def run_tests(net, output_dir):
    # Run ping test between all nodes
    nodes = ['h1', 'h2', 'server1', 'server2']
    results = {}
    for src in nodes:
        for dst in nodes:
            if src != dst:
                src_node = net.get(src)
                result = src_node.cmd(f'ping -c 4 {net.get(dst).IP()}')
                results[f'{src}_to_{dst}'] = result

    # Save results to JSON file
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, 'ping_results.json'), 'w') as f:
        json.dump(results, f, indent=4)

    # Run iPerf tests between clients and servers
    iperf_results = {}
    for client in ['h1', 'h2']:
        for server in ['server1', 'server2']:
            client_node = net.get(client)
            server_node = net.get(server)
            server_node.cmd('iperf -s -u -D')  # Start iPerf server in UDP mode
            time.sleep(1)  # Allow server to start
            result = client_node.cmd(f'iperf -c {server_node.IP()} -u -t 10 -i 1')  # Run iPerf client in UDP mode
            iperf_results[f'{client}_to_{server}'] = result
            server_node.cmd('kill %iperf')  # Stop iPerf server

    # Save iPerf results to JSON file
    with open(os.path.join(output_dir, 'iperf_results.json'), 'w') as f:
        json.dump(iperf_results, f, indent=4)

# Task 3: Analyze the performance of the network and generate graphs
# This includes plotting bandwidth data from iPerf results
def analyze_performance(output_dir):
    import matplotlib.pyplot as plt

    # Load iPerf results
    with open(os.path.join(output_dir, 'iperf_results.json'), 'r') as f:
        iperf_results = json.load(f)

    # Extract bandwidth data for plotting
    bandwidth_data = {}
    for key, result in iperf_results.items():
        lines = result.split('\n')
        for line in lines:
            if 'Mbits/sec' in line:
                parts = line.split()
                bandwidth = float(parts[-2])
                if key not in bandwidth_data:
                    bandwidth_data[key] = []
                bandwidth_data[key].append(bandwidth)

    # Plot bandwidth data
    for key, bandwidths in bandwidth_data.items():
        plt.plot(bandwidths, label=key)

    plt.xlabel('Time (s)')
    plt.ylabel('Bandwidth (Mbits/sec)')
    plt.title('Network Performance Analysis')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'analysis.png'))
    plt.close()

if __name__ == '__main__':
    # Parse arguments for bandwidth values and output directory
    parser = argparse.ArgumentParser()
    parser.add_argument('--bwBottleneck', type=int, default=10, help='Bandwidth of bottleneck link in Mbps')
    parser.add_argument('--bwOther', type=int, default=100, help='Bandwidth of other links in Mbps')
    parser.add_argument('--outputDir', type=str, default='results', help='Directory to save output results')
    args = parser.parse_args()

    # Set log level to info for better visibility
    setLogLevel('info')
    # Create network topology
    topo = NetworkBottleneck(bwBottleneck=args.bwBottleneck, bwOther=args.bwOther)
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    
    # Task 2: Run tests and save results
    run_tests(net, args.outputDir)
    
    # Task 3: Analyze network performance
    analyze_performance(args.outputDir)
    
    # Launch CLI for manual interaction if needed
    CLI(net)
    net.stop()