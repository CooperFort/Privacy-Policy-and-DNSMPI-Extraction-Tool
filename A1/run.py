import subprocess
import sys
import os

# Function to run a command and save the output
def run_command(command, output_file):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output_file.write(f"Command: {' '.join(command)}\n")
        output_file.write(result.stdout)
        output_file.write("\n*****\n")
    except subprocess.CalledProcessError as e:
        error_message = f"[Error] Command '{' '.join(command)}' failed with message: {e.stderr}\n"
        output_file.write(error_message)
        print(error_message)

def main():
    # Path to output.txt (since you're inside A1, no need for 'A1/' prefix)
    output_path = "output.txt"

    # Create or open output.txt in write mode
    with open(output_path, "w") as output_file:
        # Write HawkID and Name at the top
        output_file.write("HawkID: your_hawk_id\n")
        output_file.write("Name: Your Name\n")
        output_file.write("\n*****\n")

        # Commands to execute
        commands = [
            ["date"],
            ["whoami"],
            ["ifconfig"]
        ]

        # Execute each command and write output
        for cmd in commands:
            run_command(cmd, output_file)

        # Check if an input parameter was provided
        if len(sys.argv) < 2:
            error_message = "[Error] No input provided for ping and traceroute.\n"
            output_file.write(error_message)
            print(error_message)
            return
        
        # Extract input for ping and traceroute
        input_param = sys.argv[1]

        # Execute ping and traceroute with input
        ping_command = ["ping", input_param, "-c", "10"]
        traceroute_command = ["traceroute", input_param, "-m", "10"]

        run_command(ping_command, output_file)
        run_command(traceroute_command, output_file)

if __name__ == "__main__":
    main()
