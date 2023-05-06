

# XOR's two bytestrings together. 
def xor(a,b):
    xor_result = b''
    for i in range(len(a)):
        xor_result += bytes([a[i]^b[i]])
    return xor_result

with open("output.txt", "r") as f:
    msg1 = f.readline()
    msg2 = f.readline()


msg1 = bytes.fromhex(msg1.split()[2])
msg2 = bytes.fromhex(msg2.split()[2])


key = b''

msg1prefix = b'was the flag for the challenge '

key += xor(msg1prefix,msg1)

while len(key) < len(msg1):
    progress = xor(key,msg2)
    print(progress)
    nextptbyte = bytes([progress[-1]])
    nextkeybyte = bytes([xor(b'\x00'*len(key)+nextptbyte, msg1)[-1]])
    key += nextkeybyte

