import pyMeow as pm

process_name = "ac_client.exe"


def check_process() -> tuple | None:
    """
    Checks if the game process is running and returns the process and base address.
    """
    try:
        process = pm.open_process(process_name)
        base_address = pm.get_module(process, process_name)["base"]
        return process, base_address
    except Exception:
        return None
