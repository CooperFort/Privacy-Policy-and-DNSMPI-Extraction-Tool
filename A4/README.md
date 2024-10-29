## HW4: Building a Basic Network Intelligence and Diagnostic Service
**Project Members:** Sidney Atkins, Cooper Fort, Ben Schlachtenhaufen
**Hawk ID:** statkins, cjfort, bschlachtenhaufen

## Overview
This project consists of three main tasks aimed at implementing network diagnostic tools and a basic network intelligence service. The tasks include:
1. **Ping Program:** Measures round-trip time (RTT) for ICMP Echo packets.
2. **Traceroute Program:** Tracks the network path to a destination by incrementing the Time-To-Live (TTL) for ICMP packets.
3. **Network Intelligence Service:** A TCP-based server that provides information like IP addresses, SSL certificates, Autonomous Systems (ASNs), and hosting organizations.

## Usage

### Task 1: Ping Program
To run the `ping` program:
1. Navigate to the `A4` directory in your terminal.
2. Execute the following command:
   ```bash
   python3 cs3640-ping.py -destination <IP_ADDRESS> -n <NUM_PACKETS> -ttl <TTL_VALUE>
3. Example usage:
    python3 cs3640-ping.py -destination 8.8.8.8 -n 3 -ttl 100
4. Output will display the RTT for each packet and a summary of average RTT and success rate.

### Task 2: Traceroute Program
To run the traceroute program:
1. Navigate to the A4 directory in your terminal.
2. Execute the following command:
   ```bash
3. python3 cs3640-traceroute.py -destination <IP_ADDRESS> -n_hops <NUM_HOPS>
4. The output will display the IP address and RTT for each hop.

### Task 3: Network Intelligence Service
To run the server and client programs:
1. Start the server:
    python3 cs3640-intelserver.py
2. Run the client:
    python3 cs3640-intelclient.py -intel_server_addr <SERVER_ADDR> -intel_server_port <PORT> -domain <DOMAIN_NAME> -service <SERVICE>

## Code Structure
- cs3640-ping.py: Implements ICMP Echo packet sending and receiving.
- cs3640-traceroute.py: Extends the ping program to trace network hops.
- cs3640-intelserver.py: Implements the TCP server for network intelligence.
- cs3640-intelclient.py: Implements the client to query the network intelligence server.

## Member Contributions:

Sidney Atkins

- Created cs3640-intelserver.py, cs3640-intelclient.py and README

Cooper Fort

- Created cs3640-intelserver.py, cs3640-intelclient.py and README

Ben Schlachtenhaufen

- Created cs3640-traceroute.py, cs3640-ping.py and README

## Credit Reel
This project was built with the help of several resources that provided guidance on networking protocols, Python libraries, and best coding practices:

- **Python Documentation:** [https://docs.python.org/3/](https://docs.python.org/3/)  
  This resource was essential in understanding raw socket programming, DNS resolution, and exception handling.
- **dpkt Library:**  
  Used for creating and managing ICMP packets in the `cs3640-ping.py` and `cs3640-traceroute.py` scripts.
- **dnspython Library:**  
  Utilized for DNS resolution in the network intelligence server (`cs3640-intelserver.py`).
- **SSL Module Documentation:**  
  Helped with implementing the TLS_CERT functionality in the server, specifically for fetching and parsing SSL certificates.
- **Course Materials:**  
  The lecture slides and discussion boards provided foundational knowledge on ICMP, TCP, DNS, and SSL/TLS protocols.
