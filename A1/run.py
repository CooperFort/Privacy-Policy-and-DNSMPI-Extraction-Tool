import subprocess
import sys
import platform

def write_output(message):
    try:
        with open("output.txt", "a") as file:
            file.write(message + "\n")
    except:
        print("File can't be opened!")

def main():
   
    hawkid = "amustf"
    name = "Afrim Mustafa"

    with open("output.txt", "w") as file:
        file.write(f"HawkID: {hawkid}\nName: {name}\n\n")

    
    if platform.system() == "Darwin":  
        traceroute_cmd = ["traceroute", sys.argv[1]]
    else:  
        traceroute_cmd = ["traceroute", sys.argv[1], "-m", "10"]

    commands = [
        ["date"],
        ["whoami"],
        ["ifconfig"],
        ["ping", sys.argv[1], "-c", "10"],
        traceroute_cmd
    ]

    for cmd in commands:
        command_str = " ".join(cmd)
        write_output(f"Command: {command_str}")
        write_output("*****")
        result = subprocess.run(cmd, capture_output=True, text=True)
        write_output(result.stdout)

if __name__ == "__main__":
    main()
