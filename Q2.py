from mininet.topo import Topo
import argparse
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSController
from mininet.log import setLogLevel, info
import subprocess

class MyTopo( Topo ):
    "My topology."

    def build( self ):
        "custom topo."

        # Add hosts and switches
        Host1 = self.addHost( 'h1' )
        Host2 = self.addHost( 'h2' )
        Host3 = self.addHost( 'h3' )
        Host4 = self.addHost( 'h4' )
        Switch1 = self.addSwitch( 's1' )
        Switch2 = self.addSwitch( 's2' )

        # Add links
        self.addLink( Host1, Switch1 )
        self.addLink( Host2, Switch1 )
        self.addLink( Host3, Switch2 )
        self.addLink( Host4, Switch2 )
        self.addLink( Switch1, Switch2 )


topos = { 'mytopo': ( lambda: MyTopo() ) }



def runTopo():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Mininet')

    # Add command-line argument options
    parser.add_argument('--config', type=str)
    parser.add_argument('--congestion', type=str)

    # Parse the command-line arguments
    args = parser.parse_args()
    # print(args.config)

    topology  =  MyTopo()
    n = Mininet(topology)
    n.start()

    if args.config == 'a':
        server_process = n['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt",shell=True)
        h1_clinet_process = n['h1'].popen(f"iperf -c 10.0.0.4 -t 5  -i 0.5 -p 3000 > client_h1.txt",shell=True)
        h1_clinet_process.wait()

    elif args.config == 'b':
        #server_file_output = f"_{args.config}server_file_output.txt"
        # print(server_file_output)
        # print(f"iperf -s -t 5 -i 1 -p 3000 -Z {args.congestion} > {server_file_output}")

        server_process = n['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt",shell=True)
        h1_clinet_process_cubic = n['h1'].popen(f"iperf -c 10.0.0.4 -t 5  -i 0.5 -p 3000 -Z cubic > client_h1_cubic.txt",shell=True)
        h1_clinet_process_reno = n['h1'].popen(f"iperf -c 10.0.0.4 -t 5  -i 0.5 -p 3000 -Z reno > client_h1_reno.txt",shell=True)
        h1_clinet_process_bbr = n['h1'].popen(f"iperf -c 10.0.0.4 -t 5  -i 0.5 -p 3000 -Z bbr > client_h1_bbr.txt",shell=True)
        h1_clinet_process_vegas = n['h1'].popen(f"iperf -c 10.0.0.4 -t 5  -i 0.5 -p 3000 -Z vegas > client_h1_vegas.txt",shell=True)
        h1_clinet_process_cubic.wait()
        h1_clinet_process_reno.wait()
        h1_clinet_process_bbr.wait()
        h1_clinet_process_vegas.wait()

    elif args.config == 'c':
        server_process = n['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt", shell=True)

        # Run client processes on H1, H2, H3 for each congestion control scheme
        congestion_schemes = ['cubic', 'reno', 'bbr', 'vegas']
        for h in ['h1', 'h2', 'h3']:
            for scheme in congestion_schemes:
                client_output_file = f"client_{h}_{scheme}.txt"
                client_process = n[h].popen(f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 -Z {scheme} > {client_output_file}", shell=True)
        
        client_process.wait()
        server_process.wait()
    CLI(n)
    n.stop()

def main():
    # congestions = ['cubic','reno', 'bbr', 'vegas']
    # for congestion in congestions:
    runTopo()

main()