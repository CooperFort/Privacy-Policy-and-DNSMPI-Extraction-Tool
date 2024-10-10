import argparse
import subprocess
import time
import json
import os

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController

class BottleneckTopo(Topo):
    def build(self, bw_bottleneck, bw_other):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        self.addLink(h1, s1, cls=TCLink, bw=bw_other)
        self.addLink(h2, s1, cls=TCLink, bw=bw_other)
        self.addLink(s1, s2, cls=TCLink, bw=bw_bottleneck)  # Bottleneck link
        self.addLink(s2, h3, cls=TCLink, bw=bw_other)
        self.addLink(s2, h4, cls=TCLink, bw=bw_other)

def run_topology_tests(net, bw_bottleneck, bw_other):
    output_dir = './'

    try:
        # Collect network configuration
        with open(f'{output_dir}output-network-config.txt', 'w') as f:
            f.write("Network Configuration:\n")
            for link in net.links:
                src = link.intf1.node.name
                dst = link.intf2.node.name
                bw = link.intf1.params.get('bw', 'Unknown')
                f.write(f"Link between {src} and {dst} with bandwidth {bw} Mbps\n")

        hosts = ['h1', 'h2', 'h3', 'h4']

        # Collect ifconfig outputs
        for host_name in hosts:
            host = net.get(host_name)
            output = host.cmd('ifconfig')
            with open(f'{output_dir}output-ifconfig-{host_name}.txt', 'w') as f:
                f.write(output)

        # Perform ping tests
        for src_name in hosts:
            src_host = net.get(src_name)
            with open(f'{output_dir}output-ping-{src_name}.txt', 'w') as f:
                for dst_name in hosts:
                    if src_name != dst_name:
                        dst_host = net.get(dst_name)
                        ping_result = src_host.cmd(f'ping -c 4 {dst_host.IP()}')
                        f.write(f'Ping from {src_name} to {dst_name}:\n{ping_result}\n')

    except Exception as e:
        print(f"An error occurred in run_topology_tests: {e}")

def run_perf_tests(net, bw_bottleneck, bw_other):
    # Start the servers on h3 and h4
    h3 = net.get('h3')
    h4 = net.get('h4')

    # Start server.py on h3 for TCP test
    h3.cmd(f'python3 server.py --ip {h3.IP()} --port 5201 &')
    # Start server.py on h4 for UDP test
    h4.cmd(f'python3 server.py --ip {h4.IP()} --port 5201 &')

    time.sleep(2)  # Give servers time to start

    # Start the clients on h1 and h2
    h1 = net.get('h1')
    h2 = net.get('h2')

    # Run TCP test between h1 and h3
    h1.cmd(f'python3 client.py --ip {h1.IP()} --port 5201 --server_ip {h3.IP()} --test tcp '
           f'--bottleneck_bw {bw_bottleneck} --other_bw {bw_other}')
    # Run UDP test between h2 and h4
    h2.cmd(f'python3 client.py --ip {h2.IP()} --port 5201 --server_ip {h4.IP()} --test udp '
           f'--bottleneck_bw {bw_bottleneck} --other_bw {bw_other}')

    # Define output file names
    tcp_output_file = f'output-tcp-{bw_bottleneck}-{bw_other}.json'
    udp_output_file = f'output-udp-{bw_bottleneck}-{bw_other}.json'

    # Read the output files from h1 and h2
    tcp_output = h1.cmd(f'cat {tcp_output_file}')
    udp_output = h2.cmd(f'cat {udp_output_file}')

    # Save the outputs to the host machine
    with open(tcp_output_file, 'w') as f:
        f.write(tcp_output)
    with open(udp_output_file, 'w') as f:
        f.write(udp_output)

    print(f"Saved TCP test results to {tcp_output_file}")
    print(f"Saved UDP test results to {udp_output_file}")

def main():
    net = None

    try:
        topo = BottleneckTopo(bw_bottleneck=args.bw_bottleneck, bw_other=args.bw_other)
        net = Mininet(topo=topo, link=TCLink, controller=OVSController)
        net.start()

        run_topology_tests(net, args.bw_bottleneck, args.bw_other)
        run_perf_tests(net, args.bw_bottleneck, args.bw_other)

        # Start the CLI for further interaction if needed
        from mininet.cli import CLI
        CLI(net)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if net is not None:
            net.stop()

if __name__ == '__main__':
    # Clean up any existing Mininet instances
    try:
        subprocess.run(['sudo', 'mn', '-c'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to clean Mininet state: {e}")
        exit(1)

    parser = argparse.ArgumentParser(description='Network Bottleneck Simulation')
    parser.add_argument('--bw_bottleneck', type=int, default=10,
                        help='Bandwidth of the bottleneck link in Mbps')
    parser.add_argument('--bw_other', type=int, default=100,
                        help='Bandwidth of the other links in Mbps')
    args = parser.parse_args()

    if args.bw_other <= args.bw_bottleneck:
        print("Error: --bw_other must be greater than --bw_bottleneck")
        exit(1)

    main()
