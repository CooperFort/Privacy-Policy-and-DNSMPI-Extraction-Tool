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

def run_topology(bottleneck_bw, other_bw):
    topo = BottleneckTopo(bottleneck_bw, other_bw)
    net = Mininet(topo=topo, link=TCLink, controller=Controller)
    net.start()
    
    # Testing connectivity
    net.pingAll()

    # Stopping network
    net.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bottleneck', type=int, default=10, help="Bandwidth of the bottleneck link in Mbps")
    parser.add_argument('--other', type=int, default=100, help="Bandwidth of other links in Mbps")
    args = parser.parse_args()

    run_topology(args.bottleneck, args.other)
