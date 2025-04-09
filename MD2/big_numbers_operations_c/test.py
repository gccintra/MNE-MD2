a1 = 0xFFFFFFFFFFA8319F
a2 = 0x783913FACBE92313

b1 = 0xFFF222FFFFA8319F
b2 = 0x9999913FACBE931E

ao = int("FFFFFFFFFFA8319F783913FACBE92313", 16)
bo = int("FFF222FFFFA8319F9999913FACBE931E", 16)

sum = ao+bo
diff  = ao-bo

print(f"sum hex: {hex(sum)[2:].upper()}")
print(f"diff hex: {hex(diff)[2:].upper()}")