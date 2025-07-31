import os
import logging
import paramiko
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command

# Patch Paramiko to allow legacy key exchange algorithms
paramiko.transport.Transport._preferred_kex = (
    'diffie-hellman-group14-sha1',
    'diffie-hellman-group1-sha1',
    'diffie-hellman-group-exchange-sha1',
)

# Credentials from environment
username = os.getenv("CISCO_USER")
password = os.getenv("CISCO_PASS")

logging.basicConfig(level=logging.INFO)

nr = InitNornir(config_file="config.yaml")

nr.inventory.defaults.username = username
nr.inventory.defaults.password = password

def get_uptime(task):
    result = task.run(task=netmiko_send_command, command_string="show version | include uptime")
    output_file = f"{task.host}_uptime.txt"
    with open(output_file, "w") as f:
        f.write(result.result)

nr.run(task=get_uptime)
