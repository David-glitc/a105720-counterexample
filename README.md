# A counterexample to the A105720 "only three squares" comment

[OEIS A105720](https://oeis.org/A105720) (Zak Seidov, 2005) is

$$a(n) = p_n + p_{n+1} + \dots + p_{2n},$$

where $p_k$ is the $k$-th prime. Its entry says: *"Terms are squares at only(?) three values of
n = 3, 6, 4072."* The same claim is listed as an open conjecture in
[google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
(`FormalConjectures/OEIS/105720.lean`).

**It is false.** At $n = 111{,}008{,}771$:

| | |
|---|---|
| $p_n$ | 2,274,652,151 |
| $p_{2n}$ | 4,711,447,171 |
| $a(n)$ | 387,024,194,082,134,596 |
| $\sqrt{a(n)}$ | **622,112,686** |

There are no other squares for $4072 < n < 3 \cdot 10^8$.

## How it was checked

1. `verify/a105720.py` streams primes through a segmented sieve and tests every $a(n)$ for
   $n < 3 \cdot 10^8$. It finds the known squares at 3, 6, 4072 and the new one.
2. `verify/verify_a105720.py` is a separate odd-only sieve that sums $p_n, \dots, p_{2n}$ with exact
   integers and takes the integer square root.
3. `verify/verify_sympy.py` uses SymPy: both endpoints are prime, and $\pi(p_n) = 111008771$,
   $\pi(p_{2n}) = 222017542$, so the indices are right.

```bash
python3 verify/verify_a105720.py   # about 2 minutes, NumPy
python3 verify/verify_sympy.py     # SymPy
```

## What Lean checks

`A105720.lean` copies the formal-conjectures definition of `a` and the conjecture verbatim, then proves:

* `sq_identity`: $387024194082134596 = 622112686^2$.
* `endpoints_prime`: 2274652151 and 4711447171 are prime.
* `not_conjecture_of_value`: if $a(111008771) = 387024194082134596$, the conjecture is false.

No `sorry`; only Lean's standard axioms (`lake env lean Check.lean` prints them).
Lean does **not** compute $a(111008771)$ itself: that is a sum of about $1.1 \cdot 10^8$ primes, out of
reach for the kernel. That single value is what the three programs above establish.

```bash
lake exe cache get   # Mathlib v4.36.0
lake build
lake env lean Check.lean
```

## Why a new square was expected

$a(n) \approx 1.5\, n^2 \log n$, so a random number of that size is a square with probability about
$1/(2\sqrt{a(n)})$. Summed over $n$ this diverges like $\sqrt{\log n}$, and predicts roughly one more
square below $n = 10^8$. So the expected number of squares is infinite.

## Author

David Pere, November 2026. Found with Claude Code.

The definition of `a` and the conjecture statement in `A105720.lean` are copied from
google-deepmind/formal-conjectures (Apache License 2.0).
