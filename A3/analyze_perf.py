import json
import matplotlib.pyplot as plt


def analyze_results(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    throughput = data['end']['sum_received']['bits_per_second'] / 1e6  # Convert to Mbps
    jitter = data['end']['sum']['jitter_ms']
    packet_loss = data['end']['sum']['lost_percent']
    return throughput, jitter, packet_loss


def plot_data(results, filename="analysis.png"):
    labels, throughputs, jitters, losses = zip(*results)

    plt.figure()
    plt.plot(labels, throughputs, marker='o', label='Throughput (Mbps)')
    plt.xlabel('Bandwidth (Mbps)')
    plt.ylabel('Throughput (Mbps)')
    plt.title('Throughput vs Bandwidth')
    plt.legend()
    plt.savefig(filename)


def main():
    bandwidth_tests = [8, 32, 64]
    results = []
    for bw in bandwidth_tests:
        # Assuming output filenames based on TCP and UDP tests
        tcp_file = f"output-tcp-{bw}-32.json"  # Adjust '32' as needed if other values are used
        udp_file = f"output-udp-{bw}-32.json"

        # Analyze both TCP and UDP
        tcp_throughput, tcp_jitter, tcp_loss = analyze_results(tcp_file)
        udp_throughput, udp_jitter, udp_loss = analyze_results(udp_file)

        # Store the results for plotting and observations
        results.append((f"TCP {bw} Mbps", tcp_throughput, tcp_jitter, tcp_loss))
        results.append((f"UDP {bw} Mbps", udp_throughput, udp_jitter, udp_loss))

    plot_data(results)

    # Write observations to file
    with open("observations.txt", "w") as file:
        file.write("Network Performance Observations:\n")
        for label, throughput, jitter, loss in results:
            file.write(f"{label} - Throughput: {throughput} Mbps, Jitter: {jitter} ms, Packet Loss: {loss} %\n")


if __name__ == '__main__':
    main()