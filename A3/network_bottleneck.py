from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import Controller
import argparse

class BottleneckTopo(Topo):
    def build(self, bottleneck_bw=10, other_bw=100):
        # Adding hosts and switches
        clients = [self.addHost(f'c{i+1}') for i in range(2)]
        servers = [self.addHost(f's{i+1}') for i in range(2)]
        switches = [self.addSwitch(f'sw{i+1}') for i in range(2)]

        # Adding links between nodes with specified bandwidth
        for client in clients:
            self.addLink(client, switches[0], bw=other_bw)
        for server in servers:
            self.addLink(server, switches[1], bw=other_bw)
        self.addLink(switches[0], switches[1], bw=bottleneck_bw)

def run_topology_tests(bottleneck_bw, other_bw, time_duration):
    topo = BottleneckTopo(bottleneck_bw=bottleneck_bw, other_bw=other_bw)
    net = Mininet(topo=topo, link=TCLink, controller=Controller)
    net.start()

    # Output filenames
    config_filename = 'output-network-config.txt'
    ping_filename = 'output-ping.txt'

    # Log network configuration
    with open(config_filename, 'w') as config_file:
        for host in net.hosts:
            config_file.write(f"{host.name} configuration:\n")
            config_file.write(host.cmd('ifconfig') + "\n")

    # Ping all hosts
    ping_results = net.pingAll()
    with open(ping_filename, 'w') as ping_file:
        ping_file.write(f"Ping results: {ping_results}\n")

    # Example of using the time_duration parameter with iperf
    client = net.get('c1')
    server = net.get('s1')

    # Start iperf server on the server node
    server.cmd(f'iperf -s -t {time_duration} &')

    # Run iperf client on the client node
    client_output = client.cmd(f'iperf -c {server.IP()} -t {time_duration}')
    print(client_output)

    # Stopping the network
    net.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bottleneck', type=int, default=10, help="Bandwidth of the bottleneck link in Mbps")
    parser.add_argument('--other', type=int, default=100, help="Bandwidth of other links in Mbps")
    parser.add_argument('--time', type=int, default=10, help="Duration of the traffic simulation in seconds")
    args = parser.parse_args()

    run_topology_tests(args.bottleneck, args.other, args.time)
