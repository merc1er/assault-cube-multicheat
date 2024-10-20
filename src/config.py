import pyMeow as pm


process_name = "ac_client.exe"

try:
    process = pm.open_process(process_name)
    base_address = pm.get_module(process, process_name)["base"]
    print(f"Process found at 0x{base_address:x}.")
except Exception:
    print(f"Process {process_name} not found. Make sure Assault Cube is running.")
    exit()
