import os
import logging
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirExecutionError
import paramiko

# Patch Paramiko to allow legacy SSH key exchange (for Cisco IOS)
paramiko.transport.Transport._preferred_kex = (
    'diffie-hellman-group14-sha1',
    'diffie-hellman-group1-sha1',
    'diffie-hellman-group-exchange-sha1',
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verify required env vars are set
username = os.environ.get("CISCO_USER")
password = os.environ.get("CISCO_PASS")

if not username or not password:
    logger.error("Missing environment variables: CISCO_USER or CISCO_PASS")
    exit(1)

# Log masked credentials for debugging
logger.info(f"Env Username: {username}")
logger.info("Env Password: [HIDDEN]")

# Initialize Nornir
nr = InitNornir(config_file="config.yaml")

# Define the uptime task
def get_uptime(task):
    try:
        result = task.run(task=netmiko_send_command, command_string="show version | include uptime")
        output_file = f"{task.host}_uptime.txt"
        with open(output_file, "w") as f:
            f.write(result.result)
        logger.info(f"[SUCCESS] Uptime saved for {task.host}")
    except Exception as e:
        logger.error(f"[ERROR] {task.host} failed: {e}")

# Run across inventory
try:
    logger.info("Running Nornir uptime collection...")
    result = nr.run(task=get_uptime)
    print_result(result)
except NornirExecutionError as e:
    logger.error(f"[FATAL ERROR] Nornir execution failed: {e}")
    exit(1)
