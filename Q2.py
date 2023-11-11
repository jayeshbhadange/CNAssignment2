from mininet.topo import Topo
import argparse
import os
import pandas as pd
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSController
from mininet.log import setLogLevel, info
import subprocess
import matplotlib.pyplot as plt

def plot_bandwidth(number,file_path,output_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    intervals = []
    bandwidths = []

    # Skip the first few lines of headers
    if number=='a':
        data_lines = lines[6:]
    else:
        data_lines = lines[7:]
   
    for line in data_lines:
        # Split the line into columns
        columns = line.split()
        # Extract interval and bandwidth
        interval = float(columns[2].split('-')[1])
        bandwidth = float(columns[4])
        if(columns[5]=='GBytes'):
            bandwidth*=1000
        elif columns[5]=='KBytes':
            bandwidth/=1000

        intervals.append(interval)
        bandwidths.append(bandwidth)

    # Plot the data
    plt.plot(intervals, bandwidths, marker='o')
    plt.title('Interval vs. Bandwidth')
    plt.xlabel('Interval (sec)')
    plt.ylabel('Transfer (MBytes)')
    #plt.ylim(0, max(bandwidths) + 1)
    plt.grid(True)
    plt.savefig(output_path)
    plt.show()



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
        plot_bandwidth('a','client_h1.txt','client_h1.png')


    elif args.config == 'b':
        server_process = n['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt", shell=True)
        congestion_schemes = ['cubic', 'reno', 'bbr', 'vegas']
        client_output_files = []
        client_processes = []

        for scheme in congestion_schemes:
            client_output_file = f"client_h1_{scheme}.txt"
            client_process = n['h1'].popen(f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 -Z {scheme} > {client_output_file}", shell=True)
            client_output_files.append(client_output_file)
            client_processes.append(client_process)

        # Wait for all client processes to finish
        for client_process in client_processes:
            client_process.wait()

        # Plot the data
        for client_output_file, scheme in zip(client_output_files, congestion_schemes):
            file_path = client_output_file
            output_path = f'client_h1_{scheme}.png'
            plot_bandwidth('b', file_path, output_path)



    elif args.config == 'c':
        server_process = n['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt", shell=True)

        congestion_schemes = ['cubic', 'reno', 'bbr', 'vegas']
        hosts = ['h1', 'h2', 'h3']
        client_output_files = []
        client_processes = []

        for h in hosts:
            for scheme in congestion_schemes:
                client_output_file = f"client_{h}_{scheme}.txt"
                client_process = n[h].popen(f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 -Z {scheme} > {client_output_file}", shell=True)
                client_output_files.append(client_output_file)
                client_processes.append(client_process)

        # Wait for all client processes to finish
        for client_process in client_processes:
            client_process.wait()

        # Plot the data for each client
        for h in hosts:
            for scheme in congestion_schemes:
                file_pattern = f"client_{h}_{scheme}.txt"
                output_path = f'{file_pattern.split(".")[0]}.png'
                plot_bandwidth('c', file_pattern, output_path)

    elif args.config == 'd':
        server_process = n['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt", shell=True)

        congestion_schemes = ['cubic', 'reno', 'bbr', 'vegas']
        link_losses = [0.01, 0.03]  # Add link loss values here

        for link_loss in link_losses:
                for scheme in congestion_schemes:
                    client_output_file = f"client_h1_{scheme}linkloss{link_loss}.txt"
                    client_process = n['h1'].popen(f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 -Z {scheme} --link-loss {link_loss} > {client_output_file}",shell=True)

    CLI(n)
    n.stop()

def main():
    runTopo()

main()
