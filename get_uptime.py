import os
import logging
import paramiko
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command

# Patch Paramiko to allow legacy key exchange
paramiko.transport.Transport._preferred_kex = (
    'diffie-hellman-group14-sha1',
    'diffie-hellman-group1-sha1',
    'diffie-hellman-group-exchange-sha1',
)

# Optional: silence excessive logging
logging.basicConfig(level=logging.INFO)

# Pull credentials from Jenkins environment
username = os.getenv("CISCO_CREDS_USR")
password = os.getenv("CISCO_CREDS_PSW")

# Initialize Nornir
nr = InitNornir(config_file="config.yaml")

# Inject credentials
for host in nr.inventory.hosts.values():
    host.username = username
    host.password = password

# Define the task
def get_uptime(task):
    result = task.run(task=netmiko_send_command, command_string="show version | include uptime")
    output_file = f"{task.host}_uptime.txt"
    with open(output_file, "w") as f:
        f.write(result.result)

# Execute task
nr.run(task=get_uptime)
