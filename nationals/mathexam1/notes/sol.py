from pwn import *
from math import isqrt

# with process("python3 challenge.py", shell=True, level="debug") as rem:
with remote("77.203.226.54", 80, level="debug") as rem:
    for i in range(11):
        rem.recvuntil(b'A = ')
        A = int(rem.readline().decode().strip())
        rem.recvuntil(b'B = ')
        B = int(rem.readline().decode().strip())
        rem.recvuntil(b'C = ')
        C = -int(rem.readline().decode().strip())
        if A == 0:
            x = B // C
        else:
            D = (B**2) - (4*A*C)
            x = (-B + isqrt(D))//(2*A)
        rem.sendline(str(x))
    
    rem.interactive()
    