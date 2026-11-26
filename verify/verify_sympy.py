# Cross-check the endpoint primes and their indices with SymPy (pip install sympy).
import sympy
p_n, p_2n = 2274652151, 4711447171
print("isprime:", sympy.isprime(p_n), sympy.isprime(p_2n))
print("primepi(p_n)  =", sympy.primepi(p_n), "(expect 111008771)")
print("primepi(p_2n) =", sympy.primepi(p_2n), "(expect 222017542)")
