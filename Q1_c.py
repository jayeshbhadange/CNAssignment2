from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
    "A LinuxRouter connecting three IP subnets"

    def build(self, **_opts):
        # Subnet 1
        subnet1 = '192.168.1.0/24'
        ra = self.addNode('ra', cls=LinuxRouter, ip='192.168.1.1/24')
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1')
        h2 = self.addHost('h2', ip='192.168.1.101/24', defaultRoute='via 192.168.1.1')

        # Subnet 2
        subnet2 = '10.0.0.0/24'
        rb = self.addNode('rb', cls=LinuxRouter, ip='10.0.0.1/24')
        s2 = self.addSwitch('s2')
        h3 = self.addHost('h3', ip='10.0.0.100/24', defaultRoute='via 10.0.0.1')
        h4 = self.addHost('h4', ip='10.0.0.101/24', defaultRoute='via 10.0.0.1')

        # Subnet 3
        subnet3 = '172.16.0.0/24'
        rc = self.addNode('rc', cls=LinuxRouter, ip='172.16.0.1/24')
        s3 = self.addSwitch('s3')
        h5 = self.addHost('h5', ip='172.16.0.100/24', defaultRoute='via 172.16.0.1')
        h6 = self.addHost('h6', ip='172.16.0.101/24', defaultRoute='via 172.16.0.1')

        # Connect subnets to routers
        self.addLink(s1, ra, intfName2='ra-eth1', params2={'ip': '192.168.1.1/24'})
        self.addLink(s2, rb, intfName2='rb-eth1', params2={'ip': '10.0.0.1/24'})
        self.addLink(s3, rc, intfName2='rc-eth1', params2={'ip': '172.16.0.1/24'})
        # Connect host to respective routers
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s3)
        self.addLink(h6, s3)
        # Add links between routers
        self.addLink(ra, rb, intfName1='l', intfName2='m', params1={'ip': '192.168.2.1/24'}, params2={'ip': '192.168.2.2/24'})
        self.addLink(rb, rc, intfName1='n', intfName2='o', params1={'ip': '10.0.2.1/24'}, params2={'ip': '10.0.2.2/24'})
        self.addLink(ra, rc, intfName1='p', intfName2='q', params1={'ip': '172.16.2.1/24'}, params2={'ip': '172.16.2.2/24'})

if __name__ == '__main__':
    setLogLevel('info')
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)

    # Add static routes on ra
    net['ra'].cmd('ip route add 10.0.0.0/24 via 192.168.2.2')  # Route to subnet 2 via rb
    net['ra'].cmd('ip route add 172.16.0.0/24 via 192.168.2.2')  # Route to subnet 3 via rb
    # Add static routes on rb
    net['rb'].cmd('ip route add 192.168.1.0/24 via 192.168.2.1')  # Route to subnet 1 via ra
    net['rb'].cmd('ip route add 172.16.0.0/24 via 10.0.2.2')  # Route to subnet 3 via rc
    # Add static routes on rc
    net['rc'].cmd('ip route add 192.168.1.0/24 via 10.0.2.1')  # Route to subnet 1 via rb
    net['rc'].cmd('ip route add 10.0.0.0/24 via 10.0.2.1')  # Route to subnet 2 via rb


    net.start()
    info('*** Adding static routes on routers:\n')

    info('*** Routing Tables on Routers:\n')
    for router in ['ra', 'rb', 'rc']:
        info(net[router].cmd('route'))
    CLI(net)
    net.stop()
