import logging
import paramiko
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command

# Optional debug logging (can remove in production)
paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

# Patch Paramiko to allow legacy key exchange algorithms
paramiko.transport.Transport._preferred_kex = (
    'diffie-hellman-group14-sha1',
    'diffie-hellman-group1-sha1',
    'diffie-hellman-group-exchange-sha1',
)

# Initialize Nornir from config file
nr = InitNornir(config_file="config.yaml")

# Define the task to run on each host
def get_uptime(task):
    result = task.run(task=netmiko_send_command, command_string="show version | include uptime")
    output_file = f"{task.host}_uptime.txt"
    with open(output_file, "w") as f:
        f.write(result.result)

# Run the task across inventory
nr.run(task=get_uptime)
