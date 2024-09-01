import ctypes


read_process_memory = ctypes.windll.kernel32.ReadProcessMemory


def find_dynamic_address(
    process_handle, base_address, offsets: list, architecture=64
) -> int:
    """
    Find Dynamic Memory Allocation Address.
    """

    size = 8
    if architecture == 32:
        size = 4

    address = ctypes.c_uint64(base_address)

    for offset in offsets:
        read_process_memory(process_handle, address, ctypes.byref(address), size, 0)
        address = ctypes.c_uint64(address.value + offset)

    return address.value
