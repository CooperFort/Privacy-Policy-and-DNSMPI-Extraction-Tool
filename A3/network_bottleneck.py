import argparse
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController
import os
import subprocess


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

def run_topology_tests(bw_bottleneck, bw_other):
    net = None
    output_dir = './'

    try:
        topo = BottleneckTopo(bw_bottleneck=bw_bottleneck, bw_other=bw_other)
        net = Mininet(topo=topo, link=TCLink, controller=OVSController)
        net.start()

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

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if net is not None:
            net.stop()


if __name__ == '__main__':
    try:
        subprocess.run(['sudo', 'mn', '-c'], check=True)
    except subprocess.CalledProcessError as e: #
        print(f"Failed to clean Mininet state: {e}")
        exit(1)

    parser = argparse.ArgumentParser(description='Network Bottleneck Simulation')
    parser.add_argument('--bw_bottleneck', type=int, default=10,
                        help='Bandwidth of the bottleneck link in Mbps')
    parser.add_argument('--bw_other', type=int, default=100,
                        help='Bandwidth of the other links in Mbps')
    parser.add_argument('--time', type=int, default=10,
                        help='Duration of the traffic simulation in seconds')
    args = parser.parse_args()

    if args.bw_other <= args.bw_bottleneck:
        print("Error: --bw_other must be greater than --bw_bottleneck")
        exit(1)

    run_topology_tests(args.bw_bottleneck, args.bw_other)
