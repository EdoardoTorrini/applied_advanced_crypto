import random
import secrets

import numpy as np


def poly_mul_ring(p1: np.array, p2: np.ndarray, q: int, N: int) -> np.ndarray:
    p = np.convolve(p1, p2)
    
    # riduzione polinomiale Zq[x](x^N + 1) tramile lo slicing in python
    # è possibile farlo anche con un for, ma è computazionalmente oneroso
    # le lib in C utilizzano la NTT
    ret, tail = p[:N].copy(), p[N:]
    ret[:len(tail)] -= tail

    # riduzione modulo q
    return ret % q


def gen_e_x(N: int, sigma: float = 3.2) -> np.array:
    # la media deve essere 0.0. Il rumore aggiunto non deve alterare i dati 
    e_x_R = np.random.normal(loc=0.0, scale=sigma, size=N)
    e_x = np.round(e_x_R).astype(int)
    return e_x


def gen_secret_key(q: int, N: int) -> np.array:
    return np.random.choice([-1, 0, 1], size=N)


def gen_public_key(q: int, N: int, sk: np.array, sigma: float = 3.2) -> tuple:

    # campionamento un polinomio a(x) uniformemente casuale da tutto Zq[x](x^N + 1)
    a_x = np.random.randint(0, q, size=N)
    
    # campionamento per e(x) da una gaussiana
    e_x = gen_e_x(N, sigma)

    # calcolo del polinomio b(x)
    b_x = ( poly_mul_ring(a_x, sk, q, N) + e_x ) % q
    
    return (a_x, b_x)


def encrypt(m: int, a_x: np.array, b_x: np.array, q: int, t: int, N: int, sigma: float = 3.2) -> tuple:

    if m.bit_length() > N: raise Exception()

    m_x = np.array( list( bin(m)[2:].rjust(N, '0') )).astype(int) 

    u_x = np.random.choice([-1, 0, 1], size=N)
    delta = np.floor_divide(q, t)
    e1_x, e2_x = gen_e_x(N, sigma), gen_e_x(N, sigma)

    c_0 = (poly_mul_ring(b_x, u_x, q, N) + e1_x + delta * m_x) % q
    c_1 = (poly_mul_ring(a_x, u_x, q, N) + e2_x) % q

    return (c_0, c_1)


def decrypt(c_0: np.array, c_1: np.array, sk: np.array, q: int, t: int, N: int) -> int:
    m_scaled = ( c_0 - poly_mul_ring(c_1, sk, q, N) ) % q

    # m(x) mods q
    m_tmp = np.where(m_scaled > q // 2, m_scaled - q, m_scaled)
    delta = np.floor_divide(q, t, dtype=int)

    # dividiamo per Delta e arrotondiamo
    m_x = np.round(m_tmp / delta).astype(int) % t

    return int("".join(str(bit) for bit in m_x), 2)


def main():
    # t=2 mappa su ogni coefficente del polinomio un bit del messaggio
    # quindi la somma è lo XOR e la moltiplicazione è l'AND
    q, t, N = 2**15, 2, 16

    # key gen
    sk = gen_secret_key(q, N)
    a_x, b_x = gen_public_key(q, N, sk)

    # encrypt
    m = 42
    c_0, c_1 = encrypt(m, a_x, b_x, q, t, N)

    m1 = 6
    c1_0, c1_1 = encrypt(m1, a_x, b_x, q, t, N)
    print(f"m: {bin(m)[2:]}, m1: {bin(m1)[2:]}")

    c0_sum, c1_sum = (c_0 + c1_0) % q, (c_1 + c1_1) % q

    # decrypt
    m_new = decrypt(c0_sum, c1_sum, sk, q, t, N)
    print(f"m_new: {m_new}") 


if __name__ == "__main__":
    main()



