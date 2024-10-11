import json
import argparse
import subprocess
import matplotlib.pyplot as plt


def run_subprocess(command, output_file):
    # Runs a subprocess and writes the output to a file
    result = subprocess.run(command, capture_output=True, text=True)
    with open(output_file, "w") as file:
        file.write(result.stdout)


def analyze_results(file_path):
    # Load JSON data from the specified file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract values directly from the root level
    throughput = data['bits_per_second'] / 1e6  # Convert to Mbps
    jitter = data.get('jitter', None)  # Handle null values gracefully
    packet_loss = data.get('packet_loss', None)  # Handle null values gracefully

    return throughput, jitter, packet_loss


def plot_data(results, filename="analysis.png"):
    # Unzip the results into separate lists
    labels, throughputs, jitters, losses = zip(*results)

    # Create a plot for throughput vs bandwidth
    plt.figure()
    plt.plot(labels, throughputs, marker='o', label='Throughput (Mbps)')
    plt.xlabel('Bandwidth (Mbps)')
    plt.ylabel('Throughput (Mbps)')
    plt.title('Throughput vs Bandwidth')
    plt.legend()
    plt.savefig(filename)


def main():
    # Updated bandwidths for Task 3
    bandwidth_tests = [8, 32, 64]
    results = []
    for bw in bandwidth_tests:
        tcp_file = f"output-tcp-{bw}-32.json"
        udp_file = f"output-udp-{bw}-32.json"

        # Analyze TCP results
        tcp_throughput, tcp_jitter, tcp_loss = analyze_results(tcp_file)
        results.append((bw, tcp_throughput, tcp_jitter, tcp_loss))

        # Analyze UDP results
        udp_throughput, udp_jitter, udp_loss = analyze_results(udp_file)
        results.append((bw, udp_throughput, udp_jitter, udp_loss))

    plot_data(results)

    # Write observations to file
    with open("observations.txt", "w") as file:
        file.write("Network Performance Observations:\n")
        for bw, throughput, jitter, loss in results:
            file.write(
                f"Bandwidth: {bw} Mbps - Throughput: {throughput} Mbps, Jitter: {jitter} ms, Packet Loss: {loss} %\n")


if __name__ == '__main__':
    main()