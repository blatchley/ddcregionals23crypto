from Crypto.Util.number import long_to_bytes, getStrongPrime, isPrime, getRandomRange

def xor(a,b):
    return bytes([x^^y for x,y in zip(a,b)])


with open("output.txt", "r") as f:
    _ = f.readline()
    _ = f.readline()
    _ = f.readline()
    x0 = int(f.readline().split()[2][1:-1])
    x1 = int(f.readline().split()[2][1:-1])
    x2 = int(f.readline().split()[2][1:-1])
    x3 = int(f.readline().split()[2][1:-1])
    x4 = int(f.readline().split()[2][1:-1])
    _ = f.readline()
    _ = f.readline()
    _ = f.readline()
    _ = f.readline()
    flag = bytes.fromhex(f.readline().split()[2])
    n = int(f.readline().split()[2],16)


PR.<y2, y3> = PolynomialRing(ZZ)
PQ = PR.fraction_field()


polynomials = []

polynomials.append(PR(n))


# xb yb - xa ya
def curve_sub_b(xa,ya,xb,yb):
    pi = (yb + ya) / PQ(xb - xa)
    xconstraint = pi^2 - xb - xa
    yconstraint = pi * (xa - xconstraint) + ya
    return xconstraint, yconstraint


# xb yb - xa ya
def curve_sub(xa,ya,xb,yb, xc):
	return curve_add(xa,-ya,xb,yb,xc)
    #pi = (yb + ya) / PR(xb - xa)
    #xconstraint = pi^2 - xb - xa
    #yconstraint = pi * (xa - xconstraint) + ya
    #polynomials.append((xconstraint - xc).numerator())
    #return yconstraint.numerator()


# xb yb + xa ya
def curve_add(xa,ya,xb,yb, xc):
    pi = (yb - ya) / PQ(xb - xa)
    xconstraint = pi^2 - xb - xa
    yconstraint = pi * (xa - xconstraint) - ya
    polynomials.append((xconstraint - xc).numerator())
    return yconstraint


bx, by = curve_sub_b(x2,y2,x3,y3)

y1 = curve_sub(bx,by,x2,y2, x1)
y0 = curve_sub(bx,by,x1,y1, x0)

y4 = curve_add(x3,y3,bx,by, x4)

# curve equations
A = -((x2^3 - y2^2) - (x3^3 - y3^2)) / (x2 - x3)
B = y2^2 - x2^3 - A*x2

polynomials.append(((x0^3 + A*x0 + B) - y0^2).numerator())
polynomials.append(((x1^3 + A*x1 + B) - y1^2).numerator())

polynomials.append(((x4^3 + A*x4 + B) - y4^2).numerator())

polynomials.append(((bx^3 + A*bx + B) - by^2).numerator())

from sage.arith.functions import LCM_list
def rational_poly_to_int_poly(p):
    l = LCM_list(c.denominator() for (c, t) in p)
    #print(l)
    #for c, t in p:
    #    print(l * c)
    return sum(ZZ(l * c) * t for (c, t) in p)

polynomials = [PR(rational_poly_to_int_poly(x)) for x in polynomials]
# polynomials.append(PR(N))
print([x.parent() for x in polynomials])

# for x in polynomials:
#     print(x)

print("")
# exit()
I = ideal(*polynomials)
# I = Ideal(PR,polynomials)
#print(I)
print("Solving Groebner")
B = I.groebner_basis()
print(B)

prime = I.groebner_basis()[-1].constant_coefficient()

QR = PR.quotient_ring(I)
bx_num = QR(bx.numerator()).lift().constant_coefficient()
bx_dom = QR(bx.denominator()).lift().constant_coefficient()
bx_computed = bx_num / GF(prime)(bx_dom)

print(bx_computed)

print(xor(long_to_bytes(int(bx_computed)), flag))