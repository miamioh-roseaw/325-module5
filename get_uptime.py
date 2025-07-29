from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

import os

# Confirm Jenkins working directory (for file visibility)
print(f"[DEBUG] Working directory: {os.getcwd()}")

# Initialize Nornir using your config.yaml file
nr = InitNornir(config_file="config.yaml")

# Define the function that will run on each host
def get_uptime(task):
    try:
        # Run Netmiko command to get uptime info
        result = task.run(task=netmiko_send_command, command_string="show version | include uptime")

        # Display the result in Jenkins logs
        print(f"[INFO] {task.host.name} uptime: {result.result}")

        # Save result to a uniquely named output file in current directory
        file_path = f"{task.host.name}_uptime.txt"
        with open(file_path, "w") as f:
            f.write(result.result)

        print(f"[SUCCESS] Saved uptime info to {file_path}")

    except Exception as e:
        print(f"[ERROR] Failed to process {task.host.name}: {e}")

# Run the task across all defined hosts
print("[INFO] Starting uptime collection using Nornir...")
nr.run(task=get_uptime)
