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
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    throughput = data['end']['sum_received']['bits_per_second'] / 1e6  # Mbps
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
    # Updated bandwidths for Task 3
    bandwidth_tests = [8, 32, 64]
    results = []

    for bw in bandwidth_tests:
        run_subprocess(
            ["python3", "network_bottleneck.py", "--bottleneck", str(bw), "--other", "100"],
            f"output-tests-{bw}-bandwidth.txt"
        )
        throughput, jitter, packet_loss = analyze_results(f"output-tests-{bw}-bandwidth.txt")
        results.append((bw, throughput, jitter, packet_loss))
    
    plot_data(results)

    # Write observations to file
    with open("observations.txt", "w") as file:
        file.write("Network Performance Observations:\n")
        for bw, throughput, jitter, loss in results:
            file.write(f"Bandwidth: {bw} Mbps - Throughput: {throughput} Mbps, Jitter: {jitter} ms, Packet Loss: {loss} %\n")

if __name__ == '__main__':
    main()
