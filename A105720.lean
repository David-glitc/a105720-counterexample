import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.NumberTheory.PrimeCounting
import Mathlib.Tactic.NormNum.Prime
import Mathlib.Algebra.Group.Even

/-!
# OEIS A105720: the "only three squares" comment is false

A105720 (Zak Seidov, 2005): `a(n) = prime(n) + prime(n+1) + ... + prime(2n)`.
OEIS comment: "Terms are squares at only(?) three values of n = 3, 6, 4072."
google-deepmind/formal-conjectures states this as `OeisA105720.conjecture` (research open).

At `n = 111008771`:
* `prime(111008771) = 2274652151`, `prime(222017542) = 4711447171`,
* `a(n) = 387024194082134596 = 622112686 ^ 2`.

What Lean checks here (no `sorry`, standard axioms):
* `sq_identity`: `387024194082134596 = 622112686 ^ 2`.
* `endpoints_prime`: both endpoint values are prime.
* `not_conjecture_of_value`: if `a 111008771 = 387024194082134596`, the conjecture is false.

What Lean does not check: the value of `a 111008771` itself. It is a sum of about 1.1 * 10^8
primes, computed and cross-checked by three independent programs (see `verify/`).
The definition of `a` is copied verbatim from formal-conjectures `FormalConjectures/OEIS/105720.lean`.
-/

namespace OeisA105720

open Nat Finset

/-- Verbatim from formal-conjectures: the sum of primes from the `n`-th to the `2n`-th prime. -/
noncomputable def a (n : ℕ) : ℕ :=
  if n = 0 then 0
  else ∑ i ∈ Ico (n - 1) (2 * n), Nat.nth Nat.Prime i

/-- The conjecture exactly as formal-conjectures states it. -/
def Conjecture : Prop :=
  ∀ n : ℕ, 0 < n → (IsSquare (a n) ↔ (n = 3 ∨ n = 6 ∨ n = 4072))

/-- The counterexample index. -/
def N : ℕ := 111008771

/-- The computed value `a N`. -/
def S : ℕ := 387024194082134596

theorem sq_identity : S = 622112686 ^ 2 := by norm_num [S]

set_option maxRecDepth 100000 in
theorem endpoints_prime : Nat.Prime 2274652151 ∧ Nat.Prime 4711447171 := by
  constructor <;> norm_num

/-- If `a N = S` (the computed value), then the conjecture is false. -/
theorem not_conjecture_of_value (h : a N = S) : ¬ Conjecture := by
  intro hc
  have hsq : IsSquare (a N) := ⟨622112686, by rw [h]; norm_num [S]⟩
  have := (hc N (by norm_num [N])).mp hsq
  norm_num [N] at this

end OeisA105720

