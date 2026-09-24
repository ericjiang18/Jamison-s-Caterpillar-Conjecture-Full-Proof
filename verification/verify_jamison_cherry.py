#!/usr/bin/env python3
"""Exact algebra and finite sanity checks for the all-order cherry lemma.

Requirements: Python >= 3.10; SymPy (pip install sympy).
The symbolic checks support the written analytic proof. The finite tree checks
are tests only, not a substitute for an all-order proof or a proof assistant.
"""
from __future__ import annotations
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement, product
from fractions import Fraction
import json
from pathlib import Path
import sympy as sp

Moments = tuple[int, int, int, int, int]  # order, rooted count, rooted sum, N, R
LEAF: Moments = (1, 1, 1, 1, 1)

def node(branches: list[Moments] | tuple[Moments, ...]) -> Moments:
    """Add a new root adjacent to the root of every supplied disjoint branch."""
    m = s = t = 1
    N = R = 0
    for mi, si, ti, Ni, Ri in branches:
        t, s = t * (1 + si) + s * ti, s * (1 + si)
        m += mi
        N += Ni
        R += Ri
    return m, s, t, N + s, R + t

CHERRY = node([LEAF, LEAF])

def score(new: Moments, old: Moments) -> int:
    assert new[0] == old[0]
    return new[4] * old[3] - old[4] * new[3]

def word(packets: list[int]) -> Moments:
    if not packets or any(c < 0 for c in packets):
        raise ValueError('A word requires a nonempty list of nonnegative packets.')
    tail: Moments | None = None
    for k in reversed(packets):
        tail = node([LEAF] * k + ([] if tail is None else [tail]))
    assert tail is not None
    return tail

@lru_cache(None)
def multiplicative_partitions(n: int, minimum: int = 2) -> tuple[tuple[int, ...], ...]:
    out = [(n,)] if n >= minimum else []
    a = minimum
    while a * a <= n:
        if n % a == 0:
            out.extend((a,) + p for p in multiplicative_partitions(n // a, a))
        a += 1
    return tuple(out)

def rooted_shapes_by_count(limit: int) -> list[list[Moments]]:
    """Enumerate rooted shapes by child multisets; retain one entry per shape.

    Different shapes can have equal moment tuples; duplicates are intentional.
    Rooted count satisfies s=product(1+s_i), so this recurrence is exhaustive
    for the stated rooted-count cap, NOT for an arbitrary vertex-count cap.
    """
    buckets: list[list[Moments]] = [[] for _ in range(limit + 1)]
    buckets[1] = [LEAF]
    for s in range(2, limit + 1):
        for factors in multiplicative_partitions(s):
            choices = []
            for factor, multiplicity in Counter(factors).items():
                children = buckets[factor - 1]
                choices.append(combinations_with_replacement(range(len(children)), multiplicity))
            groups = list(Counter(factors).items())
            for selected in product(*choices):
                branches = []
                for (factor, _), indices in zip(groups, selected):
                    branches.extend(buckets[factor - 1][i] for i in indices)
                row = node(branches)
                assert row[1] == s
                buckets[s].append(row)
    return buckets

def symbolic_certificates() -> list[dict[str, str | int]]:
    x, y, U, V = sp.symbols('x y U V', positive=True)
    X, Y = sp.symbols('X Y', nonnegative=True)
    records = []
    for c in (0, 1):
        p = 2**c
        S = p * (x + 1) * (y + 1)
        d = sp.Rational(4, 3) + (sp.Rational(c, 2) + x*U + y*V)/(S - 1)
        q = 1 + sp.Rational(c, 2) + x*U + y*V + d
        Bx = (sp.Rational(3, 2)*x + 1)*(x + 1)*U - (x*x + 5*x)/4
        By = (sp.Rational(3, 2)*y + 1)*(y + 1)*V - (y*y + 5*y)/4
        F = (5*S*(sp.Rational(8, 5) - d)
             - Bx*(q - (x + 1)*U) - By*(q - (y + 1)*V)
             - (6+c)*q + 10+c)
        GB = (p*(1+y)-4)*(d-U)-4*y*V+4-2*c
        GC = (p*(1+x)-4)*(d-V)-4*x*U+4-2*c
        middle = sp.solve([GB, GC], [U, V])
        vright = sp.factor(sp.solve(GB, V)[0].subs(U, sp.Rational(1, 2)))
        assert sp.simplify(GB.subs(middle)) == 0
        assert sp.simplify(GC.subs(middle)) == 0
        assert sp.simplify(GB.subs({U: sp.Rational(1, 2), V: vright})) == 0
        points = {
            'middle': middle,
            'upper': {U: sp.Rational(1, 2), V: sp.Rational(1, 2)},
            'right': {U: sp.Rational(1, 2), V: vright},
        }
        # Left point follows by exchanging x,y and U,V.
        assert sp.simplify(F - F.xreplace({x:y, y:x, U:V, V:U})) == 0
        for name, point in points.items():
            f = sp.factor(-F.subs(point))
            num, den = sp.fraction(f)
            P = sp.Poly(sp.expand(num.subs({x:X+4, y:Y+4})), X, Y)
            den_shift = sp.Poly(sp.expand(den.subs({x:X+4, y:Y+4})), X, Y)
            assert all(a >= 0 for a in den_shift.coeffs())
            assert den_shift.coeff_monomial(1) > 0
            sos = sp.Integer(0)
            if c == 0 and name == 'middle':
                sos = 356*(X-Y)**2
            elif c == 0 and name == 'right':
                sos = 458*(X-Y)**2
            remainder = sp.Poly(sp.expand(P.as_expr()-sos), X, Y)
            assert all(a >= 0 for a in remainder.coeffs()), (c, name, remainder)
            assert remainder.coeff_monomial(1) > 0
            records.append({
                'c': c, 'vertex': name,
                'minus_F': str(f), 'denominator': str(den),
                'shifted_numerator': str(P.as_expr()),
                'sos': str(sos), 'remainder': str(remainder.as_expr()),
                'positive_constant': int(remainder.coeff_monomial(1)),
                'latex_numerator': sp.latex(P.as_expr()),
                'latex_denominator': sp.latex(den),
                'latex_remainder': sp.latex(remainder.as_expr()),
                'latex_sos': sp.latex(sos),
            })
    return records

def tree_checks() -> dict[str, int | list[str]]:
    buckets = rooted_shapes_by_count(50)
    rows = [r for bucket in buckets for r in bucket]
    for m, s, t, N, R in rows:
        assert 2*t <= s*(s+1)
        assert 6*t <= 4*N+s*s+5*s-4*m
        assert 4*t <= 2*N+s*(s+1)
        assert R*s <= t*N
        assert 4*s*N >= (6*s+4)*t-s**3-5*s*s
    tested_branches = [r for k in range(4, 21) for r in buckets[k]]
    comparisons = 0
    for i, B in enumerate(tested_branches):
        for C in tested_branches[i:]:
            for c in (0, 1, 2, 3):
                T = node([B, C, CHERRY] + [LEAF]*c)
                flat = node([B, C] + [LEAF]*(c+3))
                moveB = node([C, node([B, LEAF, LEAF])] + [LEAF]*c)
                moveC = node([B, node([C, LEAF, LEAF])] + [LEAF]*c)
                assert max(score(Z, T) for Z in (flat, moveB, moveC)) > 0
                comparisons += 1
    # Exact obstruction to extending the same three moves to a three-leaf star.
    S3 = node([LEAF]*3)
    T = node([S3, S3, S3])
    flat = node([S3, S3] + [LEAF]*4)
    swing = node([S3, node([S3] + [LEAF]*3)])
    competitor = word([5, 0, 5])
    assert score(flat,T) == -90000
    assert score(swing,T) == -24840
    assert score(competitor,T) == 60576
    return {
        'rooted_shapes_with_count_at_most_50': len(rows),
        'branch_shapes_with_count_from_4_through_20': len(tested_branches),
        'cherry_configurations_checked': comparisons,
        'counterexample_means': [str(Fraction(Z[4], Z[3])) for Z in (T,flat,swing,competitor)],
    }

def main() -> None:
    certs = symbolic_certificates()
    checks = tree_checks()
    target = Path(__file__).resolve().parent
    (target/'cherry_certificates.json').write_text(json.dumps(certs, indent=2))
    (target/'cherry_test_results.json').write_text(json.dumps(checks, indent=2))
    print('All six symbolic positivity certificates passed exactly.')
    print(json.dumps(checks, indent=2))

if __name__ == '__main__':
    main()
