import secrets
import random
import sys

from Crypto.Util.number import getPrime


def symmetric_mods(r: int, p: int) -> int:
    r = r % p
    if r <= (p - 1) // 2:
        return r
    return r - p 


def bit_encrypt(m: int, p: int, security_bit: int) -> int:
    if m not in [0, 1]:
        raise Exception(f"m must be [0, 1], not {m}")
    
    r, q = secrets.randbits(security_bit), secrets.randbits(security_bit ** 5)
    c = q * p + 2 * r + m
    return c


def encrypt(m: int, p: int, security_bit: int = 16) -> list:
    if m.bit_length() > security_bit: raise Exception()
    C = []
    for bit in bin(m)[2:].rjust(security_bit, "0")[::-1]:
        C.append( bit_encrypt( int(bit), p, security_bit ) )
    return C


# i bit di sicurezza vengono chiamati lambda
security_bit = int(sys.argv[1]) if len(sys.argv) > 1 else 4

# per trasformare il dghv (simmetrico) in un algoritmo asimmetrico, per riuscire ad applicare il bootstrapping
# che permette di rendere il dghv un FHE, in quanto la profondità del circuito non porta a divergenza l'errore

# rho = omega * (log lambda) ~ lambda -> è la lunghezza in bit dei rumori r_i
rho = security_bit

# signed_rho = rho + omega * (log lambda) ~ 2 * lambda -> è la lunghezza massima in bit dei rumori r_i
sign_rho = 2 * security_bit

# eta >= rho * theta * (lambda * log^2 lambda) ~ lambda^2 -> è la lunghezza in bit della SK
eta = security_bit ** 2

# gamma = omega * (eta^2 * log lambda) ~ lambda^5 -> è la lunghezza in bit di ogni intero della PK
gamma = security_bit ** 5

# tau = gamma + omega * (log lambda) ~ gamma + lambda
tau = gamma + security_bit

# key generation
sk = getPrime(eta)

pk = None
while True:
    pk_tmp = [ bit_encrypt(0, sk, security_bit) for _ in range(tau + 1) ]
    x_0 = max(pk_tmp)

    # x_0 deve essere dispari e x_0 mod p è pari
    if (x_0 % 2 != 0) and ( (x_0 % sk) % 2 == 0 ):
        pk_tmp.remove(x_0)
        pk = [x_0] + pk_tmp
        break


def pk_bit_encrypt(b: int, pk: list, sign_rho: int) -> int:

    if b not in [0, 1]:
        raise Exception()

    x_0 = pk[0]
    subset_size = secrets.choice( range(1, len(pk)) )
    S = random.sample( pk[1:], subset_size )

    r = secrets.choice( range(-2**sign_rho, 2**sign_rho) )
    
    return (b + 2*r + sum(S)) % x_0

def pk_bit_decrypt(c: int, sk: int) -> int:
    return symmetric_mods(c, sk) % 2

m = 1
c = pk_bit_encrypt(m, pk, sign_rho)
print(f"{c = }")

m = pk_bit_decrypt(c, sk)
print(f"{m = }")

