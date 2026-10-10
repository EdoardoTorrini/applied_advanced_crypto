import secrets

from Crypto.Util.number import getPrime

# per far andare la simulazione conviene utilizzare security_bit = 16
class Param: 
    def __init__(self, p: int, security_bit: int = 128):
        self.p = p
        self.r = secrets.randbits(security_bit)
        self.q = secrets.randbits(security_bit ** 5)


def symmetric_mods(r: int, p: int) -> int:
    r = r % p
    if r <= (p - 1) // 2:
        return r
    return r - p 


def bit_encrypt(m: int, p: int, security_bit: int) -> int:
    if m not in [0, 1]:
        raise Exception(f"m must be [0, 1], not {m}")
    param = Param(p, security_bit)
    c = param.q * param.p + 2 * param.r + m
    return c


def bit_decrypt(c: int, p: int) -> int:
    return symmetric_mods(c, p) % 2


def encrypt(m: int, p: int, security_bit: int = 16) -> list:
    if m.bit_length() > security_bit: raise Exception()
    C = []
    for bit in bin(m)[2:].rjust(security_bit, "0")[::-1]:
        C.append( bit_encrypt( int(bit), p, security_bit ) )
    return C


def decrypt(m: list, p: int) -> int:
    res = ""
    for elem in m:
        res += str( bit_decrypt(elem, p) )
    return int(res[::-1], 2)


def h_xor(c_1: int, c_2: int) -> int:
    return c_1 + c_2

def h_and(c_1: int, c_2: int) -> int:
    return c_1 * c_2

def half_adder(c_1: int, c_2: int) -> list:
    p = h_xor(c_1, c_2)
    carry = h_and(c_1, c_2)
    return p, carry

def full_adder(c_1: int, c_2: int, carry_in: int) -> list:
    p1, c1 = half_adder(c_1, c_2)
    p2, c2 = half_adder(p1, carry_in)
    carry_out = h_xor(c1, c2)
    return p2, carry_out

def h_sum(c_1: list, c_2: list, p: int, security_bit: int = 16) -> list:

    if len(c_1) != len(c_2): raise Exception()

    o_sum = []
    carry = bit_encrypt(0, p, security_bit)
    for c_i, c_j in zip(c_1, c_2):
        ret, carry = full_adder(c_i, c_j, carry)
        o_sum.append(ret)

    return o_sum

def h_mul(c_1: list, c_2: list, p: int, security_bit: int = 16) -> list:
    if len(c_1) != len(c_2): raise Exception()
    k = len(c_1) + len(c_2)
    accumulator = [ bit_encrypt(0, p, security_bit) for _ in range(k) ]
    for i, bit_2 in enumerate(c_2):
        partial = [ bit_encrypt(0, p, security_bit) for _ in range(i) ] + [ h_and(bit_2, bit_1) for bit_1 in c_1 ] + [ bit_encrypt(0, p, security_bit) for _ in range(k - len(c_1) - i) ] 
        accumulator = h_sum(accumulator, partial, p, security_bit)
    return accumulator


m_1 = 3
m_2 = 2
security_bit = 4
p = getPrime( security_bit ** 2 )

# dobbiamo aumentare il numero di bit del primo p perché se no il rumore sfonda il tetto di p/2
# r all'inizio è 16 bit mentre la soglia è p/2 = 256^2/2 = 255
# leggere pdf -> report.pdf
p = getPrime( 400 )

c_1 = encrypt(m_1, p, security_bit)
c_2 = encrypt(m_2, p, security_bit)

c = h_sum(c_1, c_2, p)
# non funziona... -> ci mette troppo tempo :( 
# c = h_mul(c_1, c_2, p)

m = decrypt(c, p)
print(f"{m = }")
