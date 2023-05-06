from pwn import *
from tqdm import tqdm
# with process(["python3 challenge.py"], shell=True, level="debug") as r:
# with process(["python3 challenge.py"], shell=True) as r:
# with remote("77.203.226.78", 80, level="debug") as r:
with remote("77.203.226.78", 80) as r:
    charset = 'abcdefghijklmnopqrstuvwxyz_}'
    # May need some manual fiddling 
    flagsofar = " TO: ____DDC{"

    while True:
        bestlength = 0x9999
        candidate = ""
        for x in tqdm(charset):
            for y in charset:
                # for z in charset:
                r.recvuntil(b"Whats your msg?: ")
                r.sendline(flagsofar + x + y)
                # r.recvuntil(b'pm ')
                # print(r.readline())
                r.recvuntil(b'We intercepted the following message leaving the relay node: ')
                rlen = len(r.readline())
                # print(f'{flagsofar +x+y+z} has {rlen}')
                if rlen < bestlength:
                    bestlength = rlen
                    candidate = x+y
        guess = candidate
        flagsofar += guess
        print(flagsofar)