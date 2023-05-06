from pwn import *

with process("python3 challenge.py", shell=True, level="debug") as rem:
# with remote("127.0.0.1", 1337, level="debug") as rem:
    for i in range(1,100):
        rem.recvuntil(b'P = ')
        P = int(rem.readline().decode().strip())

        # 2-p mod (p-1) gives 1
        # 2 - p mod p gives 2
        # (2-p)**(2-p) mod p = 2**1 = 2
        # cute math :D

        rem.sendline(str(2-P))

    rem.interactive()

    