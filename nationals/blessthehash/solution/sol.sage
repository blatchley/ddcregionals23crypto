import hashlib
import subprocess

# an example of a BLS-12 curve with ate pairing

def frobenius_point(Q):
    return Q.curve()(Q[0].frobenius(), Q[1].frobenius())

def trace_point(Q, n):
    Qi = Q
    R = Qi
    for i in range(1, n):
        Qi = frobenius_point(Qi)
        R = R + Qi
    return R

def trace_zero(Q, n):
    return n*Q - trace_point(Q, n)

def params():
    global P, Q, r, t, p, E, Ep12
    # Define parameters for curve BLS12-381
    QQx.<x> = QQ[]
    rx = cyclotomic_polynomial(12)
    tx = x+1
    cx = (x-1)^2//3 # the cofactor
    px = cx*rx + tx - 1

    u = -0xd201000000010000
    p = ZZ(px(u))
    r = ZZ(rx(u))
    t = ZZ(tx(u))
    c = ZZ(cx(u))

    Fp = GF(p)
    Fr = GF(r)
    a = Fp(0)
    b = Fp(4)
    E = EllipticCurve(Fp, [a, b])
    P0 = E.random_element()
    P = c*P0
    assert E.order() == r*c
    assert P.order() == r

    # Define an extension of degree 12 with p = 3 mod 4
    # one can define a first level to be Fp2 with non residues \beta = -1, and upper extensions with \xi = 1+i
    Fpz.<z> = Fp[]
    Fp2.<i> = Fp.extension(z^2+1)
    xi = 1 + i

    Fp2s.<s> = Fp2[]
    Fq6.<j> = Fp2.extension(s^6 - xi)
    a0, a1 = xi.polynomial().list()
    Fp12.<w> = Fp.extension(z^12 -2*a0*z^6 + a0^2 + a1^2)

    Ep12 = E.base_extend(Fp12)
    cofactor = Ep12.order() // (r^2)
    Q0 = Ep12.random_element()
    Q = cofactor * trace_zero(Q0, 12)

    assert p*Q == frobenius_point(Q)
    assert trace_point(Q, 12) == Ep12(0)

    # Test bilinearity
    P = Ep12(P)
    k = randrange(r)
    assert P.ate_pairing(k*Q, r, 12, t, p) == (P.ate_pairing(Q, r, 12, t, p))^k
    assert (k*P).ate_pairing(Q, r, 12, t, p) == (P.ate_pairing(Q, r, 12, t, p))^k
    
def bls_keygen():
    sk = randrange(r)
    return (sk, sk*Q)
    
def bls_hash(M):    
    # Hash the message by hashing to scalar and multiplying generator
    k = Integer(hashlib.sha512(M.encode()).hexdigest(), 16) % r
    return k * P
    
def bls_sign(M, sk):
    H = bls_hash(M)
    return (sk * H)
    
def bls_verify(M, S, PK):
    if PK == 0 * Q:
        return false
    H = bls_hash(M)
    return (S.ate_pairing(Q, r, 12, t, p) == H.ate_pairing(PK, r, 12, t, p))

params()

x = int(input())
y = int(input())

sig = E(x,y)

# Attack code below. Because hashing is insecure, we can just replace the hashed message in the signature and forge!
M = "This is such a lame message to sign."
_M = "Hold my beer while I sign all the things!"
k = Integer(hashlib.sha512(M.encode()).hexdigest(), 16) % r
_k = Integer(hashlib.sha512(_M.encode()).hexdigest(), 16) % r
new_sig = _k * pow(k, -1, r) * sig
print(new_sig)
