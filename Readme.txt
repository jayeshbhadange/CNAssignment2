Group members
Jayesh Bhadange 20110082
Pratik Raj              20110144


How to run the code
Question 1


For part A run the file Q1.py and run pingall to check the connectivity


For part B 
1. run the file Q1.py
2. Run xterm command in the mininet CLI for any one of the router
3. Run the command  tcpdump -i ra-eth1 -w Q1_b.pcap in xterm terminal to capture the packet.
4. Run pingall in mininet CLI 
5. Q1_b.pcap file will contain the captured packets. Check them using wireshark.


For part C, for default route
1. Run the file Q1.py
2. Open terminal for h1 and h6 and run required iperf command on both to communicate. Check Results.pdf file for observations.
3. Run ping h1 ping -c 10 h6 command on mininet CLI. Observation can be found in Results.pdf file.
For modified route
1. Run the file Q1_c.py
2. Open terminal for h1 and h6 and run required iperf command on both to communicate. Check Results.pdf file for observations.
3. Run ping h1 ping -c 10 h6 command on mininet CLI. Observations can be found in Results.pdf file.


For part D, for default route
1. Run the file Q1.py.
2. Respective routing tables will be shown on the terminal. Check Results.pdf file for observation.
For modified route
1. Run the file Q1_c.py
2. Respective routing tables will be shown on the terminal. Check Results.pdf file for observation.




Question 2
1. Run the file Q2.py using the command sudo python3 Q2.py --config <a/b/c/d> . Here a,b,c,d denote the different parts of Question 2. 
2. You will get all the data and plots as required per the question in each case. All the Results can be found on Results.pdf.