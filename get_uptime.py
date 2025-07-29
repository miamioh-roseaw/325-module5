from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

import os

# Initialize Nornir using config.yaml
nr = InitNornir(config_file="config.yaml")

# Define the task that each device will run
def get_uptime(task):
    result = task.run(task=netmiko_send_command, command_string="show version | include uptime")

    # Print output to Jenkins log
    print(f"{task.host.name} uptime: {result.result}")

    # Save to a file named after the device
    with open(f"{task.host.name}_uptime.txt", "w") as f:
        f.write(result.result)

# Run the task on all hosts
nr.run(task=get_uptime)
