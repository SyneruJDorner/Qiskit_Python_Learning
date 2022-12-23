import os, subprocess

__installation_path = os.path.join(os.getcwd(), "installation")
__full_path = os.path.join(__installation_path, "install.bat")

def install_wizzard():
    if os.name == 'nt':
        subprocess.call([__full_path, "install"])
    else:
        print("Installation is only supported on windows.")

def uninstall_wizzard():
    if os.name == 'nt':
        subprocess.call([__full_path, "uninstall"])
    else:
        print("Uninstallation is only supported on windows.")