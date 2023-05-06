
from pwn import *
from math import gcd
from Crypto.Util.number import bytes_to_long, long_to_bytes

TARGET_IP = "127.0.0.1"
TARGET_PORT = 13337

def get_sig(r,msg):
    r.recvuntil(b'message to sign (hex):')
    r.sendline(str(hex(msg)[2:]))
    r.recvuntil(b'signature (hex): ')
    return int(r.readline().strip()[2:],16)

# with process(["python3 chal.py"], shell=True, level="debug") as r:
with remote(TARGET_IP, TARGET_PORT) as r:

    # recover N from signing oracle
    sig2 = get_sig(r,2)
    sig4 = get_sig(r,2**2)
    a1 = sig2**2 - sig4

    sig3 = get_sig(r,3)
    sig9 = get_sig(r,3**2)
    a2 = sig3**2 - sig9

    sig5 = get_sig(r,5)
    sig25 = get_sig(r,5**2)
    a3 = sig5**2 - sig25

    sig7 = get_sig(r,7)
    sig49 = get_sig(r,7**2)
    a4 = sig7**2 - sig49
    
    sig11 = get_sig(r,11)
    sig121 = get_sig(r,11**2)
    a5 = sig11**2 - sig121

    n = gcd(a1,a2)
    n = gcd(n,a3)
    n = gcd(n,a4)
    n = gcd(n,a5)

    # n recovered
    print(f'recovered n: {n}')

    r.recvuntil(b'which part of the disk do you want to aim your laser at? :')
    # should land in the lowerst bit of one of the bytes in the middle of "dq"
    r.sendline(b'16000')

    faulty_sig = get_sig(r,123456789)
    print(faulty_sig)

    # recover encrypted flag
    r.recvuntil(b'flag = ')
    enc_flag = int(r.readline().strip()[2:],16)    
    
    p = gcd(pow(faulty_sig,65537,n) -123456789,n)
    q = n // p
    assert p*q == n
    d = pow(65537,-1,(p-1)*(q-1))
    flag = pow(enc_flag,d,n)
    print(long_to_bytes(flag))

    