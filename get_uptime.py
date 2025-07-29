from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import os

print("[DEBUG] Jenkins Working Directory:", os.getcwd())
print("[DEBUG] Env Username:", os.getenv("CISCO_CREDS_USR"))
print("[DEBUG] Env Password:", os.getenv("CISCO_CREDS_PSW"))

# Initialize Nornir using config.yaml
try:
    nr = InitNornir(config_file="config.yaml")
except Exception as e:
    print(f"[FATAL] Nornir initialization failed: {e}")
    exit(1)

def get_uptime(task):
    try:
        print(f"[INFO] Connecting to {task.host.name} ({task.host.hostname})")

        # Run command to get uptime line from show version
        result = task.run(
            name="Get Uptime",
            task=netmiko_send_command,
            command_string="show version | include uptime"
        )

        if result.failed:
            print(f"[ERROR] Task failed on {task.host.name}")
            return

        output = result.result
        print(f"[INFO] {task.host.name} uptime output:\n{output}")

        # Write to file
        filename = f"{task.host.name}_uptime.txt"
        with open(filename, "w") as f:
            f.write(output)
        print(f"[SUCCESS] Saved to {filename}")

    except Exception as e:
        print(f"[EXCEPTION] {task.host.name}: {e}")

# Execute across inventory
print("[INFO] Running Nornir uptime collection...")
try:
    results = nr.run(task=get_uptime)
    print_result(results)
except Exception as e:
    print(f"[FATAL] Nornir execution failed: {e}")
