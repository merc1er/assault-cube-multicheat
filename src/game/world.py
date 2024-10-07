from pymem import Pymem  # type: ignore


class World:
    """
    Represents the game world, including physics.
    """

    def __init__(self, process: Pymem) -> None:
        self.process = process

    class Offsets:
        # Jump code
        jump_code_start = 0xC2486

    def enable_jump_hack(self) -> None:
        address = self.process.base_address + self.Offsets.jump_code_start
        allocated_memory = self.process.allocate(2048)

        # The assembly instructions translated to their hex equivalent.
        # This will mov [esi + 18], 40A00000 (which is 5 in float) and then jump to the
        # original code.
        new_code = [
            0xC7,
            0x46,
            0x18,
            0x00,
            0x00,
            0xA0,
            0x40,  # mov [esi+18],40A00000 (5.0 in float)
            0xE9,
            0x00,
            0x00,
            0x00,
            0x00,  # jmp exit (the relative address will be filled in later)
        ]

        # Calculate the jump back address for returnhere
        # Distance from the allocated memory to "ac_client.exe" + C2486 + 7 (size of
        # original code + NOPs)
        return_address = (address + 7) - (allocated_memory + len(new_code))

        # Patch the jump address into the new code (E9 uses a relative address for the
        # jump)
        new_code[-4:] = return_address.to_bytes(4, byteorder="little", signed=True)

        # Write the new code to the allocated memory
        self.process.write_bytes(allocated_memory, bytes(new_code), len(new_code))

        # Patch the original code at "ac_client.exe" + C2486 to jump to the allocated
        # memory
        jmp_newmem = (
            b"\xE9"
            + (allocated_memory - address - 5).to_bytes(
                4, byteorder="little", signed=True
            )
            + b"\x90\x90"
        )
        self.process.write_bytes(address, jmp_newmem, len(jmp_newmem))

    def disable_jump_hack(self) -> None:
        address = self.process.base_address + self.Offsets.jump_code_start
        # mov [esi+18],40000000
        original_code = b"\xC7\x46\x18\x00\x00\x00\x40"
        self.process.write_bytes(address, original_code, len(original_code))
