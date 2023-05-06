
from pwn import *
from math import gcd
from Crypto.Util.number import bytes_to_long, long_to_bytes
from tqdm import tqdm
TARGET_IP = "77.203.226.84"
TARGET_PORT = 80

def get_sig(r,msg):
    r.recvuntil(b'message to sign (hex):')
    r.sendline(str(hex(msg)[2:]))
    r.recvuntil(b'signature (hex): ')
    return int(r.readline().strip()[2:],16)

# with process(["python3 chal.py"], shell=True, level="debug") as r:
# with process(["python3 chal.py"], shell=True) as r:
with remote(TARGET_IP, TARGET_PORT) as r:
    r.recvuntil(b'Public key: N = ')
    N = int(r.readline().strip().decode())
    print(f'N = {N}')

    # offset for `d` in the file:
    #        N ::   e ::  p ::   q   :: d
    offset = 2048 + 3*8 + 1024 + 1024 #+ 2048

    e = 65537
    m = 123456789987654321
    dbits = []

    for i in tqdm(range(2048)):
        r.recvuntil(b'which part of the device do you want to aim your laser at? :')
        r.sendline(str(offset + i))
        sig_i = get_sig(r,m)
        mp1 = pow(m,2**i,N)
        mm1 = pow(pow(m,-1,N),2**i,N)
        if pow(sig_i*mp1,e,N) == m:
            dbits.append(1)
        elif pow(sig_i*mm1,e,N) == m:
            dbits.append(0)
        else:
            print("FAILED!!!")
            exit()

    dbits = [str(x) for x in dbits][::-1]
    dbits = "".join(dbits)
    print(f'dbits = {dbits}')
    d = int(dbits,2)

    assert pow(pow(1234567,e,N),d,N) == 1234567

    r.recvuntil(b'which part of the device do you want to aim your laser at? :')
    # flip bit in N to trigger error detection and dump flag
    r.sendline(b'45')
    r.sendline(b'12345')

    r.recvuntil(b'flag = ')
    flag_enc = int(r.readline().strip().decode(),16)
    flag = pow(flag_enc,d,N)
    print(bytes.fromhex(hex(flag)[2:]))
    exit()
