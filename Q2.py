from mininet.topo import Topo
import argparse
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSController
from mininet.log import setLogLevel, info
import subprocess
import matplotlib.pyplot as plt
import pandas as pd


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

        server_process = n['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt",shell=True)
        congestion_schemes = ['cubic', 'reno', 'bbr', 'vegas']
        for scheme in congestion_schemes:
            client_output_file = f"client_h1_{scheme}.txt"
            client_process = n['h1'].popen(
                f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 -Z {scheme} > {client_output_file}",
                shell=True)

    elif args.config == 'c':
        server_process = n['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt", shell=True)

        congestion_schemes = ['cubic', 'reno', 'bbr', 'vegas']
        for h in ['h1', 'h2', 'h3']:
            for scheme in congestion_schemes:
                client_output_file = f"client_{h}_{scheme}.txt"
                client_process = n[h].popen(f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 -Z {scheme} > {client_output_file}", shell=True)
        
        client_process.wait()
        server_process.wait()

    elif args.config == 'd':
        server_process = n['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt", shell=True)

        congestion_schemes = ['cubic', 'reno', 'bbr', 'vegas']
        link_losses = [0.01, 0.03]  # Add link loss values here

        for link_loss in link_losses:
                for scheme in congestion_schemes:
                    client_output_file = f"client_h1_{scheme}_linkloss_{link_loss}.txt"
                    client_process = n['h1'].popen(
                        f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 -Z {scheme} --link-loss {link_loss} > {client_output_file}",
                        shell=True)

    CLI(n)
    n.stop()

def main():
    runTopo()

main()
