import platform
import subprocess
import time
import json
import requests
from datetime import datetime

OS_NAME = platform.system()  # 'Windows', 'Darwin' (macOS), 'Linux'
MACHINE_ID = platform.node()  # Hostname
API_URL = "http://localhost:8000/api/system-status"
# print(f"Detected OS: {OS_NAME}, Machine ID: {MACHINE_ID}")

#-----------Function to Check Disk Encryption Status-----------

def check_disk_encryption():
    try:
        if OS_NAME == "Windows":
            result = subprocess.check_output(
                ["manage-bde", "-status"], text=True, shell=True
            )
            return "Percentage Encrypted" in result and "100%" in result
        
        elif OS_NAME == "Darwin":  # macOS
            result = subprocess.check_output(["fdesetup", "status"], text=True)
            return "FileVault is On" in result
        
        elif OS_NAME == "Linux":
            result = subprocess.check_output(
                ["lsblk", "-o", "name,type,fstype,mountpoint"], text=True
            )
            return "crypt" in result  # crude check
        
    except Exception:
        return False
    return False

# check_disk_encryption()

#-----------Function to Check OS Update Status-----------

def check_os_update():
    try:
        if OS_NAME == "Windows":
            # Simple version check
            current_version = platform.version()
            # Ideally, query Windows Update API via PowerShell
            return {"current_version": current_version, "update_needed": False}
        
        elif OS_NAME == "Darwin":
            updates = subprocess.check_output(["softwareupdate", "-l"], text=True)
            return {"current_version": platform.mac_ver()[0], "update_needed": "No new software" not in updates}
        
        elif OS_NAME == "Linux":
            updates = subprocess.check_output(["apt", "list", "--upgradable"], text=True)
            return {"current_version": platform.release(), "update_needed": "upgradable" in updates}
        
    except Exception:
        return {"current_version": "Unknown", "update_needed": False}
# check_os_update()

#-----------Function to Check Firewall Status-----------

def check_antivirus():
    try:
        if OS_NAME == "Windows":
            ps_cmd = 'powershell "Get-MpComputerStatus | ConvertTo-Json"'
            result = subprocess.check_output(ps_cmd, text=True, shell=True)
            return json.loads(result).get("AMServiceEnabled", False)
        
        elif OS_NAME == "Darwin":
            processes = subprocess.check_output(["ps", "aux"], text=True)
            return any(av in processes for av in ["Avast", "McAfee", "Norton", "Sophos"])
        
        elif OS_NAME == "Linux":
            status = subprocess.run(["systemctl", "is-active", "--quiet", "clamav-daemon"])
            return status.returncode == 0
        
    except Exception:
        return False
    return False
# check_antivirus()

#-----------Function to Check Sleep Settings-----------

def check_sleep_settings():
    try:
        if OS_NAME == "Windows":
            ps_cmd = 'powershell "(Get-CimInstance -Namespace root\\cimv2\\power -ClassName Win32_PowerPlan).ElementName"'
            subprocess.check_output(ps_cmd, text=True, shell=True)
            return True
        
        elif OS_NAME == "Darwin":
            result = subprocess.check_output(["pmset", "-g"], text=True)
            for line in result.splitlines():
                if "sleep" in line:
                    minutes = int(line.split()[-1])
                    return minutes <= 10
            return False
        
        elif OS_NAME == "Linux":
            try:
                result = subprocess.check_output(
                    ["gsettings", "get", "org.gnome.settings-daemon.plugins.power", "sleep-inactive-ac-timeout"],
                    text=True
                )
                minutes = int(result.strip()) // 60
                return minutes <= 10
            except Exception:
                return False
            
    except Exception:
        return False
# check_sleep_settings()


def run_all_checks():
    return {
        "machine_id": MACHINE_ID,
        "os": OS_NAME,
        "disk_encryption": check_disk_encryption(),
        "os_update": check_os_update(),
        "antivirus": check_antivirus(),
        "sleep_ok": check_sleep_settings(),
        "timestamp": datetime.utcnow().isoformat()
    }


def send_to_api(data):
    try:
        headers = {"Content-Type": "application/json"}
        r = requests.post(API_URL, json=data, headers=headers, timeout=10)
        print(f"Sent data: {r.status_code}")

    except Exception as e:
        print(f"Failed to send data: {e}")


def main():
    previous_data = None
    while True:
        current_data = run_all_checks()
        if current_data != previous_data:
            send_to_api(current_data)
            previous_data = current_data
        time.sleep(18)  # for testing 

if __name__ == "__main__":
    main()

# This script is designed to run on various operating systems and perform checks related to system security and configuration.
# It checks disk encryption, OS updates, antivirus status, and sleep settings, then sends the results to a specified API endpoint.
# The script runs indefinitely, checking every 30 minutes and only sending data if there are changes




