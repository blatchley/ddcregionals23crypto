
from pwn import *
from math import gcd
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from hashlib import sha256

def prp(pt):
    prp_cipher = AES.new(b'Even_Mansour_key', AES.MODE_ECB)
    return bytes([a^b for a,b in zip(pt, prp_cipher.encrypt(pt))])

def forge_mac(shortmac):

    # shortmac is state after sk :: "A"*16 :: (16).to_bytes(16,"big")
    mac = shortmac
    h = sha256()
    h.update(mac + prp(b'give_me_the_flag'))
    mac =  h.digest()

    # real length
    msg_len = 48
    l = msg_len.to_bytes(16,"big")
    h = sha256()
    h.update(mac + prp(l))
    mac =  h.digest()
    return mac


with process("python3 challenge.py", shell=True, level="debug") as rem:
    rem.recvuntil(b'sender_id (hex): ')
    rem.sendline(b"A".hex()*16)
    rem.recvuntil(b'message (hex): ')
    rem.sendline(b"A".hex()*48)

    rem.recvuntil(b'enc_user:')
    nonce1, msg1, mac1 = [bytes.fromhex(x) for x in rem.readline().strip().decode().split(":")]
    rem.recvuntil(b'enc_msg:')
    nonce2, msg2, mac2 = [bytes.fromhex(x) for x in rem.readline().strip().decode().split(":")]
    keystream2 = xor(msg2, b"A"*48)
    
    newmac = forge_mac(mac1)
    
    msg_len = 16
    l = msg_len.to_bytes(16,"big")
    
    newcipher = xor(keystream2, b'A'*16 + l + b'give_me_the_flag')
    rem.sendline(nonce2.hex() + ":" + newcipher.hex() + ":" + newmac.hex())
    rem.interactive()




