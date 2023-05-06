from sage.all import *
from Crypto.Util.number import *
from tqdm import tqdm
from pwn import *
# real_e = 1636458454858760840180693790556998798848501900994420331442022625377277644180811089970025459946241490223463311726014945571854849081287707792431396489877340926257758926960788376424057293417995088191685573604269957638760273236060650926947883718841388055041600382567175948589522507038214287578274830498850257945456669027951742452545633577512388503003238315027267563907465460251091826944882862456917687985953
print("spinning up challenge")
# with process("python3 challenge.py", shell=True, level="debug") as rem:
with remote("77.203.226.102", 80) as rem:

    Plain = b"That feeling when you go out of your way to make DDC'22 challenges interesting and original, and the easy path of just making 10 RSA challenges. Then the players complain about there being no RSA challenges!?!! I hope they don't come to regret that :D"
    Plain = int.from_bytes(Plain,'big')

    rem.recvuntil(b'my super important information: ')
    largefactor = int(rem.readline().strip().decode())

    rem.recvuntil(b'Encryption = ')
    Encryption = int(rem.readline().strip().decode())
    rem.recvuntil(b'N = ')
    Nbig = int(rem.readline().strip().decode())
    N = Nbig // (largefactor**2)
    # first deal with non largefactor subgroups
    print(largefactor.bit_length())
    print(Nbig.bit_length())
    print(N.bit_length())
    assert largefactor**2 * N == Nbig
    CT = Encryption

    # factor the two smooth order primes
    g = 2
    g = pow(g, largefactor, N)
    for j in range(5):
        g = pow(g, 2, N)
    # optimised only checing for factors of known size
    for i in tqdm(range((1<<14)+1, (1 << 15)+1,2)):
        if isPrime(i):
            for j in range(5):
                g = pow(g, i, N)
            p = GCD(g - 1, N)
            if p != 1 and p != N:
                q = N // p
                print(p)
                print(q)
                print(p.bit_length())
                print(q.bit_length())
                break

    print(f'n ={N}')
    print(f'p ={p}')
    print(f'q ={q}')

    results = []
    moduli = []

    print("computing dlog mod p")
    Fp = GF(p)
    aa = Fp(Plain) ** largefactor
    bb = Fp(CT) ** largefactor
    smoothorderp = aa.multiplicative_order()
    resp = bb.log(aa)
    results.append(resp)
    moduli.append(smoothorderp)

    print("computing dlog mod q")
    Fq = GF(q)
    aa = Fq(Plain) ** largefactor
    bb = Fq(CT) ** largefactor
    smoothorderq = aa.multiplicative_order()
    resq = bb.log(aa)

    results.append(resq)
    moduli.append(smoothorderq)

    print("computing partial dlog mod largefactor^2")
    # compute dlog mod p^2
    def theta(k,prim):
        num = pow(k,(prim-1)*prim, prim**3) - 1
        denom = prim**2
        # print(f'num = {num}')
        # print(f'denom = {denom}')
        assert num % denom == 0
        return (num // denom) % prim

    # we have moved the dlog into the additive group
    # x_p * theta(g) = theta(y) % prim
    ty = theta(CT, largefactor)
    tg = theta(Plain, largefactor)
    e_largefac = (pow(tg,-1,largefactor) * ty) % largefactor

    results.append(e_largefac)
    moduli.append(largefactor)
    calce = crt(results, moduli)
    rem.sendline(str(calce))
    rem.interactive()