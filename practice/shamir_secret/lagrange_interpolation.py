# Squirtography 

import secrets
import random


# try to go over 32 bits number generated, 
# conduct to the collapse of the precision of the floating division
def gen_point(k: int, n: int) -> list:
    S = secrets.randbits(32)

    eq, pt = [ S ] + [ secrets.randbits(32) for _ in range(1, k) ], []

    for i in range(1, n):
        s = 0
        for j, el in enumerate(eq):
            s += el * (i ** j)
        pt.append( (i, s) )

    return eq, S, pt

def reconstruct_secret_lagrange(pt: list) -> int:
    # https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing#Computationally_efficient_approach
    a_0, k = 0, len(pt)

    for j in range(0, k):
        tmp = pt[j][1]
        for m in range(0, k):
            if m == j:
                continue
            tmp *= pt[m][0] / (pt[m][0] - pt[j][0])
        a_0 += tmp

    return round(a_0)


def discrete_convolution(vectors: list) -> list:
    if len(vectors) == 1:
        return vectors[0]

    v1, v2 = vectors[0], vectors[1]
    new_vector = [0] * (len(v1) + len(v2) - 1)

    # cauchy product
    for i in range(len(v1)):
        for j in range(len(v2)):
            new_vector[i + j] += v1[i] * v2[j]

    return discrete_convolution([new_vector] + vectors[2:])

def matrix_prod(v: list, m: list) -> list:
    ret = []
    for col_idx in range(len(m[0])):
        tmp = 0
        for row_idx, el in enumerate(v):
            tmp += el * m[row_idx][col_idx]
        ret.append(round(tmp))
    return ret


def reconstruct_eq_lagrange_basis(pt: list):
    # https://en.wikipedia.org/wiki/Lagrange_polynomial#Definition

    k = len(pt)
    lagrange_basis = []
    for j in range(k):
        x_j, y_j = pt[j]

        vector, den = [], 1
        for m in range(0, k):
            if m == j:
                continue
            
            x_m, _ = pt[m]
            vector.append( [1, -x_m] )
            den *= (x_j - x_m)
        
        num = discrete_convolution(vector)
        l_j = [el / den for el in num]
        lagrange_basis.append(l_j)

    y = [ pt[i][1] for i in range(k) ]

    eq_cmp = matrix_prod(y, lagrange_basis)
    eq_cmp.reverse()
    return eq_cmp

def compute_barycentric_weight(pt: list) -> int:
    k = len(pt)

    w = []
    for j in range(k):
        x_j, _ = pt[j]
        w_j = 1
        for m in range(k):
            if j == m:
                continue
            x_m, _ = pt[m]
            w_j *= pow( (x_j - x_m), -1)
        w.append(w_j)

    return w

def ruffini_division(poly: list, root: int) -> list:
    degree = len(poly) - 1
    q = [0] * degree
    
    q[-1] = poly[-1]
    
    for i in range(degree - 2, -1, -1):
        q[i] = poly[i + 1] + root * q[i + 1]
        
    return q


def reconstruct_secret_barycentric(pt: list) -> int:
    # https://en.wikipedia.org/wiki/Lagrange_polynomial#Barycentric_form
    
    k = len(pt)
    w = compute_barycentric_weight(pt)

    # utilizzo della seconda forma baricentrica 
    # per calcolare il segreto condiviso
 
    a_0 = 0
    num, den = 0.0, 0.0
    for j in range(k):
        x_j, y_j = pt[j]
        term = w[j] / (0 - x_j)

        num += y_j * term
        den += term
    a_0 += num /den
    return round(a_0)


def reconstruct_eq_barycentric_form(pt: list) -> list:
    # https://en.wikipedia.org/wiki/Lagrange_polynomial#Barycentric_form

    k = len(pt)
    w = compute_barycentric_weight(pt)
    final_eq = [0.0] * k

    # utilizzo della prima forma baricentrica
    # e la regola di ruffini per calcolare il polinomio di partenza
    # per calcolare l(x) possiamo utilizzare la convuluzione discreta
    
    l_x = discrete_convolution([ [-pt[j][0], 1] for j in range(k) ])
    
    for j in range(k):
        x_j, y_j = pt[j]

        # calcoliamo qj_x = l(x) / (x - x_j) attraverso la regola di ruffini
        q_x = term = ruffini_division(l_x, x_j)
        multiplier = w[j] * y_j

        for i in range(k):
            final_eq[i] += q_x[i] * multiplier

    return [ round(c) for c in final_eq ]
 

# random.choices -> can choose the same element multiple time 
# random.sample -> without replacement

shares, piece = 4, 11

eq, secret, pt = gen_point(shares, 11)
a_0 = reconstruct_secret_lagrange( random.sample(pt, k=shares) )
assert secret == a_0

a_0 = reconstruct_secret_barycentric( random.sample(pt, k=shares) )
assert secret == a_0

eq_solve = reconstruct_eq_lagrange_basis( random.sample(pt, k=shares) )
assert eq == eq_solve

eq_solve = reconstruct_eq_barycentric_form( random.sample(pt, k=shares) )
assert eq == eq_solve
