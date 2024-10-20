"""
Convert assembly code to bytecode.
"""

from keystone import Ks, KS_ARCH_X86, KS_MODE_32

# Initialize the Keystone assembler for x86 32-bit
ks = Ks(KS_ARCH_X86, KS_MODE_32)


assembly_code = """
cmp [eax+2C8],0
je originalcode

mov [eax],0
mov eax,[esi+14]

originalcode:
mov [eax],ecx
mov eax,[esi+14]
"""

# Assemble the instruction into machine code
encoding, count = ks.asm(assembly_code)

# Convert the encoding (bytecode) to a byte object
bytecode = bytes(encoding)

# Print the bytecode
print(f"Bytecode: {bytecode.hex()}")
