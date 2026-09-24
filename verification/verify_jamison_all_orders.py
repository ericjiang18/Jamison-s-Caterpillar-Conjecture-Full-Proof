#!/usr/bin/env python3
"""Exact certificates for the all-order Jamison proof candidate.

The algebra phase checks finitely many polynomial identities/positivity certificates
whose written inequalities cover unbounded path lengths and leaf packets. The test
phase is supporting evidence, not an alternative to those inequalities.

Dependencies: Python >= 3.10 and SymPy. NetworkX is only needed for --max-order.
Usage:
  python verify_jamison_all_orders.py --part all --output-dir checks
  python verify_jamison_all_orders.py --part even --output-dir checks
  python verify_jamison_all_orders.py --part odd --output-dir checks
  python verify_jamison_all_orders.py --part boundary --output-dir checks
  python verify_jamison_all_orders.py --part tests --max-order 16 --output-dir checks
This is not proof-assistant verification or independent mathematical review.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations_with_replacement
import json
import math
from pathlib import Path
import random
import time
from typing import Any, Iterable
import sympy as sp


def require(condition: Any, message: str = "certificate assertion failed") -> None:
    if not bool(condition):
        raise AssertionError(message)


def nonnegative(poly: sp.Poly, *, strict_constant: bool = False) -> bool:
    return (all(a >= 0 for a in poly.coeffs())
            and (not strict_constant or poly.coeff_monomial(1) > 0))


def poly_record(poly: sp.Poly) -> dict[str, Any]:
    return {"variables": [str(v) for v in poly.gens],
            "terms": [[list(m), str(c)] for m, c in poly.terms()]}


@dataclass(frozen=True)
class Moments:
    s: int
    t: int
    N: int
    R: int
    n: int

ONE = Moments(1, 1, 1, 1, 1)


def join(A: Moments, B: Moments) -> Moments:
    return Moments(A.s*(1+B.s), A.t*(1+B.s)+A.s*B.t,
                   A.N+B.N+A.s*B.s,
                   A.R+B.R+A.t*B.s+A.s*B.t, A.n+B.n)


def leaves(A: Moments, k: int) -> Moments:
    require(k >= 0)
    z = 1 << k
    extra = k*z*A.s//2  # integral also when k=0
    return Moments(z*A.s, z*A.t+extra, A.N+(z-1)*A.s+k,
                   A.R+(z-1)*A.t+extra+k, A.n+k)


def word(packets: Iterable[int], tail: Moments | None = None) -> Moments:
    packets = tuple(packets)
    require(bool(packets), "word requires at least one support")
    for k in reversed(packets):
        tail = leaves(ONE if tail is None else join(ONE, tail), k)
    require(tail is not None)
    return tail


def score(T: Moments, Z: Moments) -> int:
    require(T.n == Z.n, "competitor changes the vertex count")
    return Z.R*T.N-T.R*Z.N


def source(A: Moments, B: Moments, C: Moments, packets: Iterable[int]) -> Moments:
    return join(join(join(A, B), C), word(packets))


def make_model() -> dict[str, Any]:
    """Broom insertion from direct rooted and global interval counts.

    ell is the number of bare supports preceding the terminal support. The
    identities also hold at ell=0 (a star); shortening there means folding at w.
    """
    p,c,x,y,U,V,d,ell,k,z,b,L,J = sp.symbols('p c x y U V d ell k z b L J')
    alpha = 1+c/2
    tb,tc = x*(x+1)*U, y*(y+1)*V
    S = p*(x+1)*(y+1)
    M = alpha+x*U+y*V
    q = M+d
    h = ell+1
    sP = ell+z
    tP = ell*(ell+1)/2+z*(ell+1+k/2)
    sQ = h+L*x
    tQ = h*(h+1)/2+L*(tb+x*(h+b/2))
    s0 = S*(1+sP)
    t0 = s0*M+S*tP
    s1 = p*(1+sQ)*(1+J*y)
    t1 = s1*alpha+p*(1+J*y)*tQ+p*(1+sQ)*J*(tc+(k-b)*y/2)
    DN = s1-s0+((h+1)*L-1)*x+(J-1)*y+h*(1-z)
    DR = (t1-t0+((h+1)*L-1)*tb+(J-1)*tc
          +L*x*(h+1)*(h+b)/2+J*y*(k-b)/2
          +h*(h+1)*(1-z)/2-z*k*h/2)
    raw = sp.expand(DR-q*DN).subs(L*J,z)
    # Direct independent global joining check; formal component global moments.
    NA,RA,NB,RB,NC,RC = sp.symbols('NA RA NB RB NC RC')
    def sj(A, B):
        aa,at,aN,aR=A;bb,bt,bN,bR=B
        return (aa*(1+bb),at*(1+bb)+aa*bt,
                aN+bN+aa*bb,aR+bR+at*bb+aa*bt)
    AA=(p,p*alpha,NA,RA);BB=(x,tb,NB,RB);CC=(y,tc,NC,RC)
    NP=k+ell*(ell+1)/2+z*h
    RP=k+ell*(ell+1)*(ell+2)/6+z*h*(h+1+k)/2
    BP=(sP,tP,NP,RP)
    OLD=sj(sj(sj(AA,BB),CC),BP)
    NBL=NB+(L-1)*x+b
    RBL=RB+(L-1)*tb+b*L*x/2+b
    NQ=NBL+h*(h+1)/2+h*L*x
    RQ=(RBL+h*(h+1)*(h+2)/6
        +h*L*(tb+b*x/2)+L*x*h*(h+1)/2)
    CQ=(J*y,J*(tc+(k-b)*y/2),NC+(J-1)*y+k-b,
        RC+(J-1)*tc+(k-b)*J*y/2+k-b)
    NEW=sj(sj(AA,(sQ,tQ,NQ,RQ)),CQ)
    require(sp.expand(NEW[2]-OLD[2]-DN)==0, "global count identity")
    require(sp.expand(NEW[3]-OLD[3]-DR)==0, "global first-moment identity")
    D=S+ell-1
    dnum=(ell+k*z/(2*(z-1)))*D-((ell-1)*M+(ell-1)*(ell-2)/2)
    # For each allocation, include both insertion sides. Summing balanced
    # allocations afterward makes all permitted choices equally weighted.
    avg_side=sp.expand((raw+raw.xreplace({x:y,y:x,U:V,V:U}))/2)
    return locals()


def parity_model(md: dict[str,Any], parity: int):
    g,v=sp.symbols('g v')
    sy={key:md[key] for key in ('k','z','b','L','J')}
    k,z,b,L,J=(sy[key] for key in ('k','z','b','L','J'))
    sub={k:2*g+parity,z:(1+parity)*v*v,b:g,L:v,J:(1+parity)*v}
    I=sp.expand(md['avg_side'].subs(sub))
    if parity:
        I=sp.expand((I+md['avg_side'].subs({**sub,b:g+1,L:2*v,J:v}))/2)
    return I,sub,g,v


def fixed_model(md: dict[str,Any], k0:int):
    vals=sorted({k0//2,(k0+1)//2})
    I=sp.expand(sum(md['avg_side'].subs({md['k']:k0,md['z']:2**k0,
                         md['b']:j,md['L']:2**j,md['J']:2**(k0-j)})
                    for j in vals)/len(vals))
    return I,{md['k']:k0,md['z']:2**k0}


def corner_polynomials(md:dict[str,Any], I:sp.Expr, sub:dict,
                       *, star:bool=False):
    d,U,V,x,y=(md[key] for key in ('d','U','V','x','y'))
    if star:
        I=sp.expand(I.subs(md['ell'],0))
    D=md['D'].subs(md['ell'],0) if star else md['D']
    num=md['dnum'].subs(sub)
    if star:num=num.subs(md['ell'],0)
    Cd=sp.diff(I,d)
    Hpoly=sp.cancel(8*(sub[md['z']]-1)*(D*(I-Cd*d)+Cd*num)).expand()
    require(sp.diff(Hpoly,U,2)==0 and sp.diff(Hpoly,V,2)==0
            and sp.diff(Hpoly,U,V)==0, "affine corner reduction")
    hu,hv=sp.diff(Hpoly,U),sp.diff(Hpoly,V)
    h0=Hpoly.subs({U:0,V:0})
    corners={}
    for iu,iv in ((0,0),(1,0),(1,1)):
        corners[(iu,iv)]=sp.expand((x+1)*(y+1)*h0
            +(y+1)*(x+1 if iu else 5)*hu/2
            +(x+1)*(y+1 if iv else 5)*hv/2)
    require(sp.expand(I-I.xreplace({x:y,y:x,U:V,V:U}))==0,
            "symmetry supplying the fourth corner")
    return Cd,corners


def lower_affine_g(expr:sp.Expr,g:sp.Symbol,v:sp.Symbol,W:sp.Symbol,
                   gmin:int)->tuple[sp.Expr,dict[str,Any]]:
    """gmin<=g<=v/(2**gmin/gmin), v>=2**gmin.

    The upper bound is justified in the proof by 2**g >=
    (2**gmin/gmin)*g for every integer g>=gmin.
    """
    require(sp.Poly(expr,g,v).degree(g)<=1, "non-affine g coefficient")
    v0=2**gmin
    ratio=sp.Rational(v0,gmin)
    c0=sp.Poly(expr.subs(g,0).subs(v,W+v0),W)
    cg=sp.Poly(sp.diff(expr,g).subs(v,W+v0),W)
    pos=sum(a*W**m[0] for m,a in cg.terms() if a>0)
    neg=sum(a*W**m[0] for m,a in cg.terms() if a<0)
    lower=sp.Poly(c0.as_expr()+gmin*pos+(W+v0)*neg/ratio,W)
    # Explicitly check the algebraic identity behind the lower-bound direction.
    difference=sp.expand(expr.subs(v,W+v0)-lower.as_expr()
                         -(g-gmin)*pos-(g-(W+v0)/ratio)*neg)
    require(difference==0, "affine coefficient lower-bound identity")
    return lower.as_expr(),{"exact":str(expr),"lower":poly_record(lower),
                            "positive_g_part":str(pos),"negative_g_part":str(neg)}


def unbounded_broom(md:dict[str,Any],parity:int)->dict[str,Any]:
    I,sub,g,v=parity_model(md,parity)
    Cd,corners=corner_polynomials(md,I,sub)
    P,C,H,X,Y,W=sp.symbols('P C H X Y W')
    ell=md['ell'];zval=sub[md['z']]
    transform={md['p']:1+C+P,md['c']:C,
               md['x']:ell+zval+X,md['y']:ell+zval+Y}
    def expand(poly):
        return sp.Poly(sp.expand(poly.subs(transform).subs(ell,H+1)),P,C,H,X,Y)
    cp=expand(Cd)
    cprows=[]
    for mon,expr in cp.terms():
        lower,record=lower_affine_g(expr,g,v,W,4)
        require(nonnegative(sp.Poly(lower,W)), "Cd coefficient")
        record['monomial']=list(mon);cprows.append(record)
    require(cp.coeff_monomial(1).subs({g:4,v:16})>0,
            "strict Cd at base")
    result={"parity":parity,"g_min":4,"v_shift":16,
            "count_derivative":cprows,"corners":{}}
    for corner,qpoly in corners.items():
        expanded=expand(qpoly)
        groups={};coefficient_count=0
        for mon,expr in expanded.terms():
            pm,cm,hm,xm,ym=mon;idx=(pm,cm,xm,ym)
            lower,rec=lower_affine_g(expr,g,v,W,4)
            groups.setdefault(idx,{})[hm]=(lower,rec)
            coefficient_count+=1
        records=[]
        for idx,rows in groups.items():
            bs={degree:sp.Poly(row[0],W) for degree,row in rows.items()}
            rec={"monomial_PCXY":list(idx),"H_coefficients":{
                 str(deg):row[1] for deg,row in sorted(rows.items())}}
            if all(nonnegative(pol) for pol in bs.values()):
                require(bs[0].nth(0)>0,"strict positive coefficient group")
                rec['certificate']='nonnegative_coefficients'
            else:
                require(all(nonnegative(pol) for deg,pol in bs.items() if deg!=1),
                        "only linear H term may be negative")
                B0,B1,B2=(bs[j].as_expr() for j in (0,1,2))
                chosen=None
                # A fixed finite collection of rational square centers. Finding
                # one is merely certificate construction; both sign checks below
                # independently establish its validity at every W>=0.
                for lam in (sp.Rational(j,8) for j in range(1,17)):
                    R1=sp.Poly(B1+2*lam*(W+16)*B2,W)
                    R0=sp.Poly(B0-lam**2*(W+16)**2*B2,W)
                    if nonnegative(R1) and nonnegative(R0,strict_constant=True):
                        chosen=(lam,R1,R0);break
                require(chosen is not None,f"missing square certificate: {parity} {corner} {idx}")
                lam,R1,R0=chosen
                original=sum(pol.as_expr()*H**degree for degree,pol in bs.items())
                rhs=(B2*(H-lam*(W+16))**2+R1.as_expr()*H+R0.as_expr()
                    +sum(pol.as_expr()*H**deg for deg,pol in bs.items() if deg>=3))
                require(sp.expand(original-rhs)==0,"H-square identity")
                rec.update(certificate='square',lambda_value=str(lam),
                           linear_remainder=poly_record(R1),constant_remainder=poly_record(R0))
            records.append(rec)
        require(len(records)==96 and coefficient_count==576,
                "unexpected unbounded coefficient support")
        result['corners'][str(corner)]={"groups":records,
                                      "coefficient_count":coefficient_count}
        print(f"broom parity {parity}, corner {corner}: {len(records)} groups passed",flush=True)
    return result


def boundary_brooms(md:dict[str,Any])->dict[str,Any]:
    P,C,H,X,Y=sp.symbols('P C H X Y');result={}
    for k0 in range(2,8):
        I,sub=fixed_model(md,k0);Cd,corners=corner_polynomials(md,I,sub)
        ell=md['ell'];z=2**k0
        transform={md['p']:1+C+P,md['c']:C,md['x']:ell+z+X,md['y']:ell+z+Y}
        def expand(poly):
            return sp.Poly(sp.expand(poly.subs(transform).subs(ell,H+1)),P,C,H,X,Y)
        cp=expand(Cd);require(nonnegative(cp,strict_constant=True),"boundary Cd")
        case={"Cd":poly_record(cp),"corners":{}}
        for corner,poly in corners.items():
            expr=expand(poly).as_expr();groups=sp.Poly(expr,P,C,X,Y)
            records=[]
            for mon,hpoly in groups.terms():
                pp=sp.Poly(hpoly,H);rec={"monomial_PCXY":list(mon),"H_polynomial":poly_record(pp)}
                if nonnegative(pp,strict_constant=True):
                    rec['certificate']='nonnegative_coefficients'
                else:
                    require(all(a>=0 or deg[0]==1 for deg,a in pp.terms()),
                            "only H-linear boundary term may be negative")
                    a0,a1,a2=(pp.nth(j) for j in (0,1,2))
                    discriminant=4*a0*a2-a1*a1
                    require(a2>0 and discriminant>0,"boundary square discriminant")
                    rhs=a2*(H+a1/(2*a2))**2+discriminant/(4*a2)
                    rhs+=sum(a*H**deg[0] for deg,a in pp.terms() if deg[0]>=3)
                    require(sp.expand(hpoly-rhs)==0,"boundary square identity")
                    rec.update(certificate='square',discriminant=str(discriminant))
                records.append(rec)
            require(len(records)==96,"unexpected boundary support")
            case['corners'][str(corner)]=records
        result[str(k0)]=case
        print(f"broom boundary k={k0}: all three corners passed",flush=True)
    return result


def stars(md:dict[str,Any])->dict[str,Any]:
    """ell=0, k>=3. The k=2 case is the separate cherry lemma."""
    P,C,X,Y,W=sp.symbols('P C X Y W');result={"fixed":{},"unbounded":{}}
    for mode in ('k3','even','odd'):
        if mode=='k3':I,sub=fixed_model(md,3)
        else:I,sub,g,v=parity_model(md,int(mode=='odd'))
        Cd,corners=corner_polynomials(md,I,sub,star=True)
        transform={md['p']:1+C+P,md['c']:C,
                   md['x']:sub[md['z']]+X,md['y']:sub[md['z']]+Y}
        case={}
        for name,pol in [('Cd',Cd)]+[(str(co),qp) for co,qp in corners.items()]:
            poly=sp.Poly(sp.expand(pol.subs(transform)),P,C,X,Y)
            if mode=='k3':
                require(nonnegative(poly,strict_constant=True),f"star {name}")
                case[name]=poly_record(poly)
            else:
                rows=[]
                for mon,expr in poly.terms():
                    lower,rec=lower_affine_g(expr,g,v,W,2)
                    require(nonnegative(sp.Poly(lower,W)),f"unbounded star {name}")
                    if all(e==0 for e in mon):
                        require(sp.Poly(lower,W).nth(0)>0,"strict star base")
                    rec['monomial']=list(mon);rows.append(rec)
                case[name]=rows
        result['fixed' if mode=='k3' else 'unbounded'][mode]=case
        print(f"star {mode}: all certificates passed",flush=True)
    return result


def concentration_identities()->dict[str,Any]:
    S,M,q,d,r,z,a,k,ell=sp.symbols('S M q d r z a k ell')
    # Suffix C(a,0^(ell-1),k) versus C(0^ell,a+k).
    h=ell+1
    s0=r*(ell+z)
    t0=r*ell*(ell+1+a)/2+r*z*(h+(a+k)/2)
    s1=ell+r*z
    t1=ell*(ell+1)/2+r*z*(h+(a+k)/2)
    N0=a+k+r*z+ell*(r+z)+(ell-1)*ell/2
    R0=a+k+r*z*(h+(a+k)/2)+ell*(r*(h+a)+z*(h+k))/2+(ell-1)*ell*(ell+1)/6
    N1=a+k+r*z+ell*(1+r*z)+(ell-1)*ell/2
    R1=a+k+r*z*(h+(a+k)/2)+ell*(h+r*z*(h+a+k))/2+(ell-1)*ell*(ell+1)/6
    change=sp.expand(R1-R0-q*(N1-N0)+S*((t1-t0)+(M-q)*(s1-s0)))
    eta=a*r/(2*(r-1))
    F=(S-z+1)*(d-(ell+1)/2-eta)-(z-1)*M+k*z/2
    require(sp.cancel(change.subs(q,M+d)-ell*(r-1)*F)==0,"concentration identity")
    # Shortening at the far end: compare the two explicit branch moment sets.
    # The prefix remains C(a,0^(ell-2),k+1), interpreted as a star at ell=1.
    f=r*ell;tpre=r*ell*(ell+1+a)/2
    g=r+ell-1;j=(ell-1)*ell/2+r*(ell+a/2)
    L0=ell+a/2
    eps=((r+ell-2)*M+(ell-2)*(ell-1+a)/2)/(r*(S+1)+ell-2)
    eps2=((g-1)*(M+L0)-j+1)/(S*r+g-1)
    require(sp.cancel(eps-eps2)==0,"shortening epsilon identity")
    # Finite algebra behind the elementary host and epsilon inequalities.
    m,b=sp.symbols('m b')
    require(sp.expand((m+1)**2-(2*m-b+1)*(b+1)-(m-b)**2)==0,
            "host propagation square identity")
    require(sp.expand(r*ell/2-r-ell+2-(r-2)*(ell-2)/2)==0,
            "epsilon factor inequality")
    require(sp.expand(r*r/4-(r-1)-(r-2)**2/4)==0,
            "ell=1 epsilon bound")
    return {"concentration_score":str(ell*(r-1)*F),"epsilon":str(eps),
            "ell_ge_2_margin":"(3*S+5*z+11)/16",
            "ell_eq_1_margin":"(17*S+13*z+47)/60",
            "identities_passed":5}


def graph_moments(adj:list[set[int]],root:int=0)->Moments:
    """Independent graph recursion, not using word/insertion formulas."""
    parent={root:-1};order=[root]
    for u in order:
        for v in adj[u]:
            if v!=parent[u]:
                require(v not in parent,"not a tree")
                parent[v]=u;order.append(v)
    require(len(order)==len(adj),"disconnected graph")
    rows={}
    for u in reversed(order):
        rr=ONE
        for v in adj[u]:
            if parent.get(v)==u:rr=join(rr,rows[v])
        rows[u]=rr
    return rows[root]


def randword(rng:random.Random,max_length:int=30,max_packet:int=15)->tuple[int,...]:
    length=rng.randint(1,max_length)
    return tuple(rng.randint(0,max_packet) if rng.random()<.22 else 0
                 for _ in range(length-1))+(rng.randint(2,max_packet),)


def finite_tests(seed:int=20260920, rounds:int=30000)->dict[str,Any]:
    rng=random.Random(seed);concentrations=brooms=stars_n=identities=0
    for it in range(rounds):
        W=[randword(rng) for _ in range(3)]
        W.sort(key=lambda pp:word(pp).s)
        pp,bw,cw=W
        A=word(randword(rng,25,12));B=word(bw);C=word(cw)
        T=source(A,B,C,pp);m=word(pp).s
        require(B.s>=m and C.s>=m)
        S0=join(join(A,B),C)
        require(S0.s>=(m+1)**2)
        require(S0.t*(m+1)<=S0.s*S0.s,"initial host ratio")
        if any(pp[:-1]):
            last=max(i for i,k0 in enumerate(pp[:-1]) if k0)
            H=S0
            for kk in pp[:last]:H=leaves(join(ONE,H),kk)
            suffix=pp[last:];bs=word(suffix).s
            require(H.s>=(bs+1)**2 and H.t*(bs+1)<=H.s*H.s,"propagated host ratio")
            new=list(pp);new[-1]+=new[last];new[last]=0
            sh=pp[:-2]+(pp[-2]+pp[-1]+1,)
            require(max(score(T,source(A,B,C,new)),score(T,source(A,B,C,sh)))>0,
                    "concentration or shortening")
            concentrations+=1
        else:
            ell=len(pp)-1;k0=pp[-1]
            candidates=[]
            if ell:
                candidates.append(source(A,B,C,pp[:-2]+(k0+1,)))
            else:
                candidates.append(leaves(join(join(A,B),C),k0+1))
            for b0 in sorted({k0//2,(k0+1)//2}):
                for BB,CC in ((B,C),(C,B)):
                    candidates.append(join(join(A,word((0,)*(ell+1),leaves(BB,b0))),leaves(CC,k0-b0)))
            if ell or k0>=3:
                require(max(score(T,Q) for Q in candidates)>0,"broom alternatives")
                if ell:brooms+=1
                else:stars_n+=1
        # Explicit shortening and concentration formulas on actual moments.
        if it<2000:
            ell=rng.randint(1,80);a=rng.randint(1,12);k0=rng.randint(2,16)
            H=word(randword(rng));P0=(a,)+(0,)*(ell-1)+(k0,)
            OLD=join(H,word(P0));NEW=join(H,word((0,)*ell+(a+k0,)))
            q=Fraction(OLD.R,OLD.N);M=Fraction(H.t,H.s);d=q-M;r=2**a;z=2**k0
            F=((H.s-z+1)*(d-Fraction(ell+1,2)-Fraction(a*r,2*(r-1)))
               -(z-1)*M+Fraction(k0*z,2))
            require(F*ell*(r-1)*OLD.N==score(OLD,NEW),"integer concentration score")
            identities+=1
    # Terminal brooms, rather than random dense decorated words, also get a
    # systematic family including large lengths and arbitrary rooted partners.
    systematic=0
    for ell in [1,2,3,5,10,30,100,1000]:
        for k0 in [2,3,4,5,6,7,8,9,16,24,63,64,127,256,1024]:
            pp=(0,)*ell+(k0,);base=word(pp)
            for aa in [(0,),(0,0,0,0),(3,),(0,7)]:
                A=word(aa)
                for extra in [0,1,3]:
                    B=leaves(base,extra);C=join(ONE,base)
                    T=source(A,B,C,pp)
                    cand=[source(A,B,C,pp[:-2]+(k0+1,))]
                    for b0 in sorted({k0//2,(k0+1)//2}):
                        for BB,CC in ((B,C),(C,B)):
                            cand.append(join(join(A,word((0,)*(ell+1),leaves(BB,b0))),leaves(CC,k0-b0)))
                    require(max(score(T,Q) for Q in cand)>0,"systematic broom comparison")
                    systematic+=1
    return {"seed":seed,"random_rounds":rounds,"concentration_cases":concentrations,
            "random_broom_cases":brooms,"random_star_cases_k_ge_3":stars_n,
            "exact_integer_identity_checks":identities,"systematic_broom_cases":systematic,
            "largest_terminal_packet":1024,"largest_bare_prefix":1000}


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--part',choices=['all','even','odd','boundary','stars','base','tests'],default='all')
    parser.add_argument('--output-dir',type=Path,default=Path('checks'))
    parser.add_argument('--max-order',type=int,default=0,
                        help='optional exhaustive unlabeled graph test; requires NetworkX')
    args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();out={"part":args.part,"status":"passed"}
    md=make_model() if args.part not in ('base','tests') else None
    if args.part in ('all','even','odd'):
        for parity in (0,1):
            if args.part=='even' and parity==1:continue
            if args.part=='odd' and parity==0:continue
            data=unbounded_broom(md,parity)
            (args.output_dir/f'broom_unbounded_{parity}.json').write_text(json.dumps(data,indent=2))
            out[f'broom_unbounded_{parity}']={"group_certificates":288,"coefficient_lower_bounds":1728}
    if args.part in ('all','boundary'):
        data=boundary_brooms(md)
        (args.output_dir/'broom_boundaries.json').write_text(json.dumps(data,indent=2))
        out['broom_boundaries']={"group_certificates":1728}
    if args.part in ('all','stars'):
        data=stars(md)
        (args.output_dir/'star_certificates.json').write_text(json.dumps(data,indent=2))
        out['stars']={"unbounded_corner_coefficients":576,"k3_corner_coefficients":288}
    if args.part in ('all','base'):
        from verify_jamison_cherry import symbolic_certificates,tree_checks
        cc=symbolic_certificates()
        (args.output_dir/'cherry_certificates.json').write_text(json.dumps(cc,indent=2))
        out['cherry']={"symbolic_certificates":len(cc),"supporting_checks":tree_checks()}
        out['concentration_identities']=concentration_identities()
    if args.part in ('all','tests'):
        out['finite_tests']=finite_tests()
        if args.max_order:
            from exhaustive_graph_check import check_through_order
            out['graph_tests']=check_through_order(args.max_order)
    out['elapsed_seconds']=round(time.monotonic()-start,3)
    (args.output_dir/f'result_{args.part}.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
