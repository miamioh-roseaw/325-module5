import logging
import paramiko
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command

# Logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Patch Paramiko for legacy kex
paramiko.transport.Transport._preferred_kex = (
    'diffie-hellman-group14-sha1',
    'diffie-hellman-group1-sha1',
    'diffie-hellman-group-exchange-sha1',
)

# Init Nornir
nr = InitNornir(config_file="config.yaml")

def get_uptime(task):
    logger.info(f"[INFO] Running uptime check on {task.host.hostname} ({task.host.hostname})")
    try:
        result = task.run(task=netmiko_send_command, command_string="show version | include uptime")
        output = result.result.strip()
        logger.info(f"[SUCCESS] {task.host.name} uptime: {output}")

        # Write to file
        with open(f"{task.host}_uptime.txt", "w") as f:
            f.write(output + "\n")

    except Exception as e:
        logger.error(f"[ERROR] {task.host.name} failed: {str(e)}")

# Run it
nr.run(task=get_uptime)
