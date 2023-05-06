p = 63708208868673992316109933265915655905325467831822549861374592525403329033329
# A = ¯\(ツ)/¯
# B = ¯\(ツ)/¯
g0 = (13301628550179307071144860151714387569482329207248930585747415091165915205586, 55488174360865441257901115711060646854059276399351838704546093655006493763647)
# g1 = ¯\(ツ)/¯
g2 = (33900910496875974714913047358911625265687893754102632447917976519759188305964, 21825297248012176688485127847677240133516855130970823926862346618053041731695)
# g3 = ¯\(ツ)/¯
g4 = (22189149231897579740661301060866045280412209061853428399861778309586361362173, 20302292161171827893851882856250280574237829562573991528262075673086434873994)
# g5 = ¯\(ツ)/¯
g6 = (8561493592831891957433631604091632238869081937058377764938672884849886761811, 17766220815633566043476921452571687647868797607260365978450116609126924493544)
# g7 = ¯\(ツ)/¯
g8 = (43898014721414059387914930214157083349188647946648364824334031843640114720816, 52502973810293470088422234171968569155617165292261237214854367011451810251401)
flag = bytes.fromhex("427b3d0d04fd9468f1ed783542af59fe0c4016f0fce3ce43a3f3f47aa0182975")




F = GF(p)
g0x = F(g0[0])
g0y = F(g0[1])
g2x = F(g2[0])
g2y = F(g2[1])
g0x = F(g4[0])
g0y = F(g4[1])

# we know that for each point the following equation holds
# y^2 = x^3 + A*x + B

# we can use the three equalities
# y1^2 = x1^3 + A*x1 + B
# y2^2 = x2^3 + A*x2 + B
# y3^2 = x3^3 + A*x3 + B
# giving us 3 equations and two unknowns, and jsut solve for A and B


# t1 = A * (g0x) + B
# t2 = A * (g2x) + B
# t3 = t2-t1 = A ( g2x - g0x)
# t4 = t3 / (g2x-g0x) = A
# t5 = t1 - A * g0x = B
t1 = g0y^2 - g0x^3
t2 = g2y^2 - g2x^3
t3 = t1 - t2
t4 = t3 * pow(g0x - g2x,-1,p)
A = int(t4)
t5 = t1 - A * g0x
B = int(t5)
print(f'A = {A}')
print(f'B = {B}')

from pwn import xor
from Crypto.Util.number import long_to_bytes, isPrime
EE = EllipticCurve(F,[A,B])
EEo = EE.order()
assert isPrime(EEo)

g0 = EE(g0)
g2 = EE(g2)


# g2 - g0 = 2 * secret
# divide out 2 by inverting mod order of the curve

b2 = g2 - g0
inv2 = int(pow(2,-1,EEo))
secret = inv2 * b2
mask = int(secret[0])
print(f"flag = {xor(long_to_bytes(mask), flag)}")