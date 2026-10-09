import secrets
import random

# in this example we use the Mersenne prime
# otherwise can be used 2 ** 8 with arbitrary data and files
# and lastly using with q ~ secp256k1 in the web3 application (with MPC and TSS)
class GFInt(int):
    q = 2 ** 521 - 1

    def __new__(cls, value=None):
        val = secrets.randbits(1024) % cls.q if value is None else int(value) % cls.q
        return super().__new__(cls, val)

    def __add__(self, other):
        return type(self)((int(self) + int(other)) % self.q)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return type(self)(other) - self

    def __mul__(self, other):
        return type(self)((int(self) * int(other)) % self.q)

    def __rmul__(self, other):
        return self * other

    def __pow__(self, exponent):
        return type(self)(pow(int(self), int(exponent), self.q))

    def __truediv__(self, other):
        if not isinstance(other, (int, type(self))):
            return NotImplemented 
        return self * pow(int(other) % self.q, -1, self.q)

    def __rtruediv__(self, other):
        return type(self)(other) / self

    def __neg__(self):
        return type(self)((-int(self)) % self.q)


def gen_point(k: int, n: int) -> list:
    S = GFInt() 
    print(f"secret: {S}")

    eq, pt = [ (S, GFInt(0)) ], []

    for i in range(1, k):
        a_i = GFInt()
        eq.append( (a_i, GFInt(i)) )

    for i in range(1, n):
        s = GFInt(0)
        for el in eq:
            s += el[0] * (GFInt(i) ** el[1])
        pt.append( (GFInt(i), s) )

    return eq, pt


def reconstruct(pt: list):
    a_0, k = GFInt(0), len(pt)

    for j in range(0, k):
        tmp = pt[j][1]
        for m in range(0, k):
            if m == j:
                continue
            tmp *= pt[m][0] / (pt[m][0] - pt[j][0])
        a_0 += tmp

    return a_0

eq, pt = gen_point(4, 11)
a_0 = reconstruct( random.sample(pt, 4) )
print(f"{a_0 = }")

