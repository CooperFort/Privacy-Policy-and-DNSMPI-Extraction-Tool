Homework 3: Network Simulation and Performance Measurement Using Mininet and iPerf

Project Members: Afrim Mustafa, Sidney Atkins, Cooper Fort, Ben Schlachtenhaufen
Hawk ID: amustf, statkins, cjfort, bschlachtenhaufen

Running the Code
Setting up the Network: network_bottleneck.py
This script creates the network topology and runs tests to ensure the network is correctly configured.

Command to run:
bash
python3 network_bottleneck.py --bw_bottleneck <value> --bw_other <value> --time <value>
--bw_bottleneck: Bandwidth of the bottleneck link (default is 10 Mbps).
--bw_other: Bandwidth of the other links (default is 100 Mbps).
--time: Duration of the traffic simulation (default is 10 seconds).

This will create a network with the specified bandwidth settings, perform ifconfig and ping tests, and log the results in files such as:
output-network-config.txt
output-ifconfig-h<i>.txt
output-ping-h<i>.txt

Running iPerf Server: server.py
To start the iPerf server, use the following command:
bash
python3 server.py --ip <server-ip> --port <server-port>
This will start the server with the specified IP and port.

Running iPerf Client: client.py
To start the iPerf client, run the following command:
bash
python3 client.py --ip <client-ip> --port <client-port> --server_ip <server-ip> --test <tcp/udp>
--test: Use tcp for TCP traffic and udp for UDP traffic.
This will generate traffic and save the results as JSON files such as output-<test>-<bottleneck>-<other>.json.

Analyzing Performance: analyze_perf.py
This script runs network simulations with different bandwidth configurations and plots the results.

Command to run:
bash
python3 analyze_perf.py
This script will run network_bottleneck.py multiple times with different bottleneck bandwidth values (8 Mbps, 32 Mbps, and 64 Mbps) and generate a plot (analysis.png) showing the throughput for TCP and UDP traffic. Additionally, insights will be saved in observations.txt.

Output Files
Task 1 Outputs:
output-network-config.txt
output-ifconfig-h1.txt, output-ifconfig-h2.txt, etc.
output-ping-h1.txt, output-ping-h2.txt, etc.

Task 2 Outputs:
output-tcp-<bottleneck>-<other>.json
output-udp-<bottleneck>-<other>.json

Task 3 Outputs:
analysis.png
observations.txt

Member Contributions:

Afrim Mustafa
   Task 1, 2, Comments
Sidney Atkins
    Task 3, README
Cooper Fart
    Task 3, README
Ben Schlachtenhaufen


Credit Reel:

Mininet Introduction Video: https://www.youtube.com/watch?v=tn1-Pxm0ckc
    How to set up mininet, mininet functions, differences in mininet topologies
Mininet Documentation: https://mininet.org/walkthrough/
    Explained how to use mininet with Ubuntu VIM and assisted in solving errors found in debugging
Iperf Documentation: https://iperf.fr/iperf-doc.php
    Background on using Iperf and its commands
iPerf Video: https://www.youtube.com/watch?v=kPnhFxiiUQY
    Information on setting up iPerf servers and clients and connecting them
Matplotlib Documentation: https://matplotlib.org/stable/index.html
    Background documentation on how to use matplotlib and its functions