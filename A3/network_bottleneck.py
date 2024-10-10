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
        self.addLink(s1, s2, cls=TCLink, bw=bw_bottleneck)
        self.addLink(s2, h3, cls=TCLink, bw=bw_other)
        self.addLink(s2, h4, cls=TCLink, bw=bw_other)

def run_topology_tests(net, bw_bottleneck, bw_other):
    output_dir = './'

    with open(f'{output_dir}output-network-config.txt', 'w') as f:
        f.write("Network Configuration:\n")
        for link in net.links:
            src = link.intf1.node.name
            dst = link.intf2.node.name
            bw = link.intf1.params.get('bw', 'Unknown')
            f.write(f"Link between {src} and {dst} with bandwidth {bw} Mbps\n")

    hosts = ['h1', 'h2', 'h3', 'h4']

    for host_name in hosts:
        host = net.get(host_name)
        output = host.cmd('ifconfig')
        with open(f'{output_dir}output-ifconfig-{host_name}.txt', 'w') as f:
            f.write(output)

    for src_name in hosts:
        src_host = net.get(src_name)
        with open(f'{output_dir}output-ping-{src_name}.txt', 'w') as f:
            for dst_name in hosts:
                if src_name != dst_name:
                    dst_host = net.get(dst_name)
                    ping_result = src_host.cmd(f'ping -c 4 {dst_host.IP()}')
                    f.write(f'Ping from {src_name} to {dst_name}:\n{ping_result}\n')

def run_perf_tests(net, bw_bottleneck, bw_other):
    h3 = net.get('h3')
    h4 = net.get('h4')

    h3.cmd(f'python3 server.py --ip {h3.IP()} --port 5201 &')
    h4.cmd(f'python3 server.py --ip {h4.IP()} --port 5201 &')

    time.sleep(2)

    h1 = net.get('h1')
    h2 = net.get('h2')

    h1.cmd(f'python3 client.py --ip {h1.IP()} --port 5201 --server_ip {h3.IP()} --test tcp --bottleneck_bw {bw_bottleneck} --other_bw {bw_other}')
    h2.cmd(f'python3 client.py --ip {h2.IP()} --port 5201 --server_ip {h4.IP()} --test udp --bottleneck_bw {bw_bottleneck} --other_bw {bw_other}')

    tcp_output_file = f'output-tcp-{bw_bottleneck}-{bw_other}.json'
    udp_output_file = f'output-udp-{bw_bottleneck}-{bw_other}.json'

    tcp_output = h1.cmd(f'cat {tcp_output_file}')
    udp_output = h2.cmd(f'cat {udp_output_file}')

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

        from mininet.cli import CLI
        CLI(net)

    finally:
        if net is not None:
            net.stop()

if __name__ == '__main__':
    subprocess.run(['sudo', 'mn', '-c'], check=True)

    parser = argparse.ArgumentParser(description='Network Bottleneck Simulation')
    parser.add_argument('--bw_bottleneck', type=int, default=10,
                        help='Bandwidth of the bottleneck link in Mbps')
    parser.add_argument('--bw_other', type=int, default=100,
                        help='Bandwidth of the other links in Mbps')
    args = parser.parse_args()

    if args.bw_other <= args.bw_bottleneck:
        exit(1)

    main()
