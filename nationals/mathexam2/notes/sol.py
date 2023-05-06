from sage.all import *
from pwn import *

with process("python3 challenge.py", shell=True, level="debug") as rem:
# with remote("127.0.0.1", 1337, level="debug") as rem:
    for i in range(1,25):
        rem.recvuntil(b'P = ')
        P = int(rem.readline().decode().strip())
        rem.recvuntil(b'A = ')
        A = int(rem.readline().decode().strip())
        rem.recvuntil(b'B = ')
        B = int(rem.readline().decode().strip())
        rem.recvuntil(b'C = ')
        C = -int(rem.readline().decode().strip())
        
        if A == 0:
            x = B // C
        else:
            F = GF(P)
            A = F(A)
            B = F(B)
            C = F(C)
            D = (B**2) - (4*A*C)
            x = (-B + D.sqrt())//(2*A)
            print(x)
        rem.sendline(str(int(x)))

    rem.interactive()

    