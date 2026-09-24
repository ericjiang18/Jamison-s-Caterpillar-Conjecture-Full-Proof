# An all-order candidate proof of Jamison’s caterpillar conjecture

## Status and scope

This document presents a **complete computer-assisted proof candidate** of the stronger statement that **every** tree maximizing mean subtree order at a fixed order is a caterpillar. The unbounded parts of the argument are proved by structural inequalities and finite, exact polynomial certificates. The certificate data and a generator/verifier are supplied with this document.

The candidate has not received independent human mathematical review or proof-assistant verification. This document does not claim literature priority or external acceptance. The exact calculations reported below were executed; the finite tree tests are supporting checks, not a replacement for the unbounded proof.

**No large-order theorem, asymptotic benchmark, numerical cutoff, or published finite-order verification is used.** In particular, the original manuscript’s large-order candidate and its subsequently proposed cutoff reduction are not dependencies. The earlier cherry exclusion is used as a base case, and its complete proof is reproduced in Appendix B. The earlier three-leaf-star, general-star, and two-vertex-arm supplements are not needed for the new main chain.

The central change is to choose a terminal arm of **minimum rooted subtree count**, rather than an arbitrary balanced pair. This supplies host inequalities at every cut along that arm. Those inequalities allow all internal leaf packets to be eliminated at once, leaving a broom whose length is unrestricted.

---

## The theorem

> **Theorem.** For every integer \(n\ge1\), every tree on \(n\) vertices maximizing the mean order of its nonempty connected induced vertex subsets is a caterpillar.
>
> Consequently, for every \(n\), a caterpillar attains the maximum mean subtree order among all \(n\)-vertex trees.

The theorem is the conclusion of the proof candidate below, including its supplied finite algebraic certificates.

## 1. Definitions and elementary facts

All trees are finite, nonempty, and simple. A subtree means a nonempty vertex subset inducing a connected graph. For a tree \(X\), let
\[
N_X=\#\{\text{subtrees of }X\},\qquad
R_X=\sum_{S\text{ subtree of }X}|S|,\qquad
\mu(X)=R_X/N_X.
\]
For a specified root, let \(s_X,t_X\) be the corresponding count and order sum restricted to subtrees containing that root.

The skeleton \(K(T)\) is the subgraph of the original tree induced by its non-leaf vertices. A caterpillar is a tree whose skeleton is a path, allowing an empty path or a singleton. The word \(C(c_1,\ldots,c_h)\) denotes a specified path of \(h\) support vertices, with \(c_i\) pendant leaves at support \(i\), rooted at the first support. Its specified path need not equal the intrinsic skeleton of the component considered separately.

### 1.1 Rooted joining identities

Joining disjoint rooted trees \(A,B\) by an edge and retaining the root of \(A\) gives
\[
\begin{aligned}
s_{A+B}&=s_A(1+s_B),&
t_{A+B}&=t_A(1+s_B)+s_At_B,\\
N_{A+B}&=N_A+N_B+s_As_B,&
R_{A+B}&=R_A+R_B+t_As_B+s_At_B.
\end{aligned}
\tag{1.1}
\]
Indeed, a connected set either lies in one component or meets both roots. Thus the formulas include all subtrees, not just the root-containing ones.

Deleting the root into components \(X_i\) gives
\[
s=\prod_i(1+s_i),\qquad
\frac ts=1+\sum_i\frac{t_i}{1+s_i},\qquad
N=s+\sum_iN_i,\qquad R=t+\sum_iR_i.
\tag{1.2}
\]

For a fixed source tree \(T\), always put \(q=\mu(T)\). The fixed-source score of a same-order competitor \(Z\) is
\[
\Delta(Z)=R_Z-qN_Z.
\tag{1.3}
\]
It is positive exactly when \(\mu(Z)>\mu(T)\). Equivalently, its sign is the sign of the integer \(R_ZN_T-R_TN_Z\).

### 1.2 Rooted bounds

For every rooted tree,
\[
2t\le s(s+1).
\tag{1.4}
\]
Induction in (1.2) gives \(t_i/(1+s_i)\le s_i/2\), while \(\prod_i(1+s_i)\ge1+\sum_i s_i\), proving the assertion.

Also,
\[
\mu(X)\le t_X/s_X.
\tag{1.5}
\]
To prove this, write \(L=t/s\) and \(L_i=t_i/s_i\). By (1.4),
\[
L-L_i
=1-\frac{t_i}{s_i(1+s_i)}
 +\sum_{j\ne i}\frac{t_j}{1+s_j}\ge\frac12.
\]
Induction bounds each component’s global mean by its rooted mean. Formula (1.2) expresses the original global mean as a weighted average of \(L\) and those component global means. This proves (1.5).

We shall use the lower bound
\[
s\ge5\quad\Longrightarrow\quad \frac ts\ge\frac52.
\tag{1.6}
\]
Here \(t\ge2s-1\), since only the singleton root-containing subtree has order one. If the root has at least three children, each contributes at least \(1/2\) in (1.2). With two children and \(s\ge5\), one child has count at least two and contributes at least one, while the other contributes at least \(1/2\). With one child, its count is \(s-1\ge4\). Counts at least five give a contribution at least \((2s_i-1)/(s_i+1)\ge3/2\). A rooted tree of count four is either an endpoint-rooted four-vertex path or a two-leaf star rooted at its center; their rooted order sums are ten and eight. The remaining contribution is therefore at least \(8/5\). These cases prove (1.6).

### 1.3 The leaf-neighbor restriction

A maximizing tree of order \(n\ge4\) has \(q>2\). For \(n=4\), the star has mean \(23/11\). For \(n\ge5\), the path has mean \((n+2)/3>2\), obtained by counting its intervals.

Suppose a leaf \(x\) has degree-two neighbor \(u\), with other neighbor \(w\). Let \(H=T-\{u,x\}\), rooted at \(w\), with \(s_H=S,t_H=SM\). Move \(x\) from \(u\) to \(w\), retaining \(wu\). Direct use of (1.1) gives score
\[
S(M+1-q)+q-2>0,
\tag{1.7}
\]
because \(M+1\) is the original tree’s rooted mean at \(w\) and is at least \(q\) by (1.5). This contradicts maximality.

Therefore a maximizing tree has no leaf adjacent to a degree-two vertex. In particular, every leaf of its skeleton supports at least two original leaves.

### 1.4 The cherry base case

We use the following all-order statement:

> **Cherry lemma.** In a maximizing tree of order at least four, a support with exactly two leaf neighbors and one other neighbor cannot have its other neighbor be a skeleton branching vertex.

Appendix B reproduces its complete proof. It uses (1.1)–(1.5), the additional inductive inequality
\[
6t\le4N+s^2+5s-4|V(X)|,
\tag{1.8}
\]
and six exact polynomial positivity certificates. It has no order cutoff and is independent of the large-order manuscript. Its six certificates were regenerated and checked as part of this continuation.

## 2. Minimum-count terminal arms and their host bounds

A **terminal arm** of a non-caterpillar tree is a whole component of \(T-w\), where \(w\) is a branching vertex of \(K(T)\), such that its vertices in \(K(T)\) form a path from a neighbor of \(w\) to a leaf of \(K(T)\), containing no further skeleton branching vertex. The root of the arm is the neighbor of \(w\).

Every non-caterpillar has a terminal arm: root its skeleton at any branching vertex and choose a branching vertex farthest from that root; its outward components are terminal paths. If the root is the only branching vertex, every skeleton component at that root is such a path.

Choose a terminal arm \(P\) minimizing its rooted count, and put
\[
\rho=s_P.
\tag{2.1}
\]
Let \(w\) be its attachment vertex.

### Lemma H: count dominance and propagation into the arm

Choose two other non-leaf components \(B,C\) of \(T-w\), and retain \(w\) and every remaining component in \(A\). Put
\[
p=s_A,\qquad x=s_B,\qquad y=s_C.
\]
Then
\[
x,y\ge\rho.
\tag{2.2}
\]
Moreover, cut \(P\) immediately before any of its support vertices, obtaining a suffix of rooted count \(b\). Let \(H\) be the whole retained tree on the other side of that edge, rooted at the suffix’s attachment vertex. Write \(S=s_H,M=t_H/s_H\). Then
\[
\boxed{S\ge(b+1)^2,\qquad \frac MS\le\frac1{b+1}.}
\tag{2.3}
\]

**Proof.** Every other non-leaf component at \(w\) either is itself a terminal arm, or contains one: in the latter case choose a skeleton branching vertex farthest from \(w\) within the component and one of its outward terminal arms.

Let \(Q\) be such an arm inside \(B\). Every subtree of \(Q\) containing its root can be extended by the fixed path from the root of \(B\) to that root. This gives an injection into root-containing subtrees of \(B\). Thus \(s_B\ge s_Q\ge\rho\). The same argument gives \(s_C\ge\rho\), proving (2.2).

First delete all of \(P\). The retained tree \(H_0\), rooted at \(w\), has
\[
S_0=p(1+x)(1+y)\ge(\rho+1)^2.
\]
By (1.4), its rooted mean satisfies
\[
M_0\le\frac{p+x+y+1}{2}.
\]
Consequently,
\[
\frac{M_0}{S_0}
\le\frac12\left(\frac1{x+1}+\frac1{y+1}\right)
\le\frac1{\rho+1}.
\tag{2.4}
\]
The first inequality uses \(p+x+y+1\le p(x+y+2)\).

Now grow the retained prefix of \(P\) one support vertex at a time, treating the newly added support as root and including its original leaf packet. If the packet has size \(a\ge0\), put \(r=2^a\) and \(e=1+a/2\). A retained rooted pair \((S,M)\) changes to
\[
S'=r(1+S),\qquad M'=e+\frac{SM}{1+S}.
\]
Since \(e/r\le1\),
\[
\frac{M'}{S'}
=\frac{e}{r(1+S)}+\frac{SM}{r(1+S)^2}
\le\frac1S+\frac MS.
\tag{2.5}
\]
Also \(S'\ge S+1\).

Suppose \(d\) support vertices precede the suffix of count \(b\). The recurrence for the original arm, read from its suffix toward its root, gives
\[
\rho\ge b+d.
\tag{2.6}
\]
Each step adds at least one to the rooted count, regardless of its leaf packet.

All retained counts during the growth are at least \(S_0\). By (2.4)–(2.6),
\[
\frac MS
\le\frac1{\rho+1}+\frac d{(\rho+1)^2}
\le\frac{2\rho-b+1}{(\rho+1)^2}
\le\frac1{b+1}.
\]
The last inequality follows from the exact identity
\[
(\rho+1)^2-(2\rho-b+1)(b+1)=(\rho-b)^2\ge0.
\tag{2.7}
\]
Finally \(S\ge S_0\ge(\rho+1)^2\ge(b+1)^2\). This proves (2.3). ∎

The ratio in (2.3) is \(M/S=t_H/s_H^2\), not merely the rooted mean. The lemma controls the actual retained host at every cut along the selected arm; it does not replace that host by a formal tuple.

## 3. Concentrating the last internal packet

For integers \(\ell\ge1,a\ge1,k\ge2\), define
\[
D_{\ell;a,k}=C(a,\underbrace{0,\ldots,0}_{\ell-1},k).
\]
There are \(\ell+1\) support vertices. Write
\[
r=2^a,\qquad z=2^k,\qquad b=r(\ell+z)=s_{D_{\ell;a,k}}.
\]

### Lemma P: packet concentration

Attach \(D_{\ell;a,k}\) to an arbitrary rooted host \(H\) with rooted count \(S\) and rooted mean \(M\), obtaining \(T\). Suppose
\[
S\ge b^2,\qquad M/S\le1/b.
\tag{3.1}
\]
Then either shortening the final support into its predecessor or moving all \(a\) leaves from the first support to the final support strictly increases the global mean.

Both operations preserve the complete vertex set.

### Proof

Put \(q=\mu(T)\), \(d=q-M\), and
\[
\chi_k=\frac{kz}{2(z-1)},\qquad
\eta_a=\frac{ar}{2(r-1)},\qquad
D_0=r(S+1)+\ell-2>0.
\]
Define
\[
\varepsilon=
\frac{(r+\ell-2)M+(\ell-2)(\ell-1+a)/2}{D_0}.
\tag{3.2}
\]

#### The shortening comparison

The exact shortening score is
\[
\boxed{
\Delta_{\rm short}
=(z-1)D_0\left(\ell+\frac a2+\chi_k-\varepsilon-d\right).
}
\tag{3.3}
\]
Here shortening makes the terminal support into an additional leaf at its predecessor. At \(\ell=1\), the replacement word is \(C(a+k+1)\).

For a direct count, let \(U=C(a,0,\ldots,0)\) be the \(\ell\)-support prefix. Its full-prefix count and conditional mean are \(r\) and \(\ell+a/2\). Its rooted count and total order at the **last** support are
\[
g=r+\ell-1,\qquad j=r(\ell+a/2)+\ell(\ell-1)/2.
\]
The generating-polynomial difference for shortening is
\[
((1+u)^k-1)\,[F_H(u)u^{\ell}(1+u)^a+G_U(u)-u].
\]
Indeed, intervals ending at the last two supports are replaced by one interval, and the last support becomes a new singleton leaf. Evaluation and differentiation at \(u=1\), followed by subtraction of \(q\) times the count increment, give (3.3). The identity
\[
(g-1)(M+\ell+a/2)-j+1
=(r+\ell-2)M+(\ell-2)(\ell-1+a)/2
\]
gives the displayed \(\varepsilon\).

If shortening does not improve, (3.3) implies
\[
d\ge d_0:=\ell+a/2+\chi_k-\varepsilon.
\tag{3.4}
\]

#### The concentration comparison

Let \(G\) move all \(a\) leaves from the first support to the final support, producing \(C(0,\ldots,0,a+k)\) on the same \(\ell+1\) supports.

Its component increments, before attaching to \(H\), are
\[
\Delta s=-\ell(r-1),\qquad
\Delta t=-\frac{\ell}{2}\bigl[(r-1)(\ell+1)+ar\bigr],
\]
\[
\Delta N=\ell(r-1)(z-1),
\]
\[
\Delta R=\frac{\ell}{2}
\bigl[(r-1)(z-1)(\ell+1)+ar(z-1)+kz(r-1)\bigr].
\tag{3.5}
\]
These follow by counting spine intervals, or by substituting the two endpoint packets in the double-broom interval formula. Singleton leaf counts are unchanged.

Using (1.1), the full-tree score therefore satisfies
\[
\boxed{
\frac{\Delta(G)}{\ell(r-1)}
=(S-z+1)\left(d-\frac{\ell+1}{2}-\eta_a\right)
-(z-1)M+\frac{kz}{2}.
}
\tag{3.6}
\]
The coefficient \(S-z+1\) is positive by (3.1). We may substitute (3.4) into (3.6) in a lower-bound direction. Its parenthesized expression becomes
\[
\frac{\ell-1}{2}-\frac{a}{2(r-1)}+\chi_k-\varepsilon.
\tag{3.7}
\]
Use \(a\le2^a-1=r-1\).

#### Case \(\ell\ge2\)

Since \(r+\ell-2\le r\ell/2\) and \(\ell-1+a\le\ell+r-2\le r\ell/2\), (3.1)–(3.2) give
\[
\begin{aligned}
\varepsilon
&\le\frac{r+\ell-2}{r^2(\ell+z)}
 +\frac{(\ell-2)(\ell+r-2)}{2rS}\\
&\le\frac1{2r}+\frac{\ell^2}{4S}
\le\frac1{2r}+\frac1{4r^2}
\le\frac5{16}.
\end{aligned}
\tag{3.8}
\]
The first bound uses \(D_0\ge rS\) and \(M\le S/[r(\ell+z)]\).

Since \(\chi_k\ge1\), (3.7) is at least \(\ell/2-5/16\ge11/16\). Also
\[
(z-1)M\le S/2,\qquad kz/2\ge z.
\]
Consequently,
\[
\frac{\Delta(G)}{\ell(r-1)}
\ge\frac{11}{16}(S-z+1)-\frac S2+z
=\boxed{\frac{3S+5z+11}{16}>0}.
\tag{3.9}
\]

#### Case \(\ell=1\)

Equation (3.2) gives
\[
\varepsilon
\le\frac{(r-1)M}{rS}
\le\frac{r-1}{r^2(1+z)}
\le\frac1{4(1+z)}\le\frac1{20}.
\tag{3.10}
\]
Here \((r-1)/r^2\le1/4\). For every integer \(k\ge2\), \(\chi_k\ge4/3\): equality holds at \(k=2\), and \(k\ge3\) gives \(\chi_k>k/2\ge3/2\).

Thus (3.7) is at least
\[
\frac43-\frac12-\frac1{20}=\frac{47}{60}.
\]
Using the same bounds on \((z-1)M\) and \(kz/2\),
\[
\frac{\Delta(G)}{r-1}
\ge\frac{47}{60}(S-z+1)-\frac S2+z
=\boxed{\frac{17S+13z+47}{60}>0}.
\tag{3.11}
\]
Both cases give a strict improvement whenever shortening fails. This proves Lemma P. ∎

### Corollary: a minimum-count terminal arm in a maximizer is a broom

Suppose the selected arm \(P\) of a maximizing tree has an internal leaf packet. Choose its **last** positive internal packet. Its suffix has the form \(D_{\ell;a,k}\) above, with \(a\ge1,k\ge2\). Lemma H gives the stronger bounds \(S\ge(b+1)^2\) and \(M/S\le1/(b+1)\), hence (3.1).

Maximality makes the shortening non-improving. Lemma P then makes the concentration strictly improving, a contradiction.

Therefore
\[
\boxed{P=C(\underbrace{0,\ldots,0}_{\ell},k),\qquad \ell\ge0,\quad k\ge2.}
\tag{3.12}
\]
There is **no bound on \(\ell\)**. There is also no need to preserve the minimum-count property after the concentration: the single strict improvement already contradicts maximality.

## 4. Brooms of arbitrary length

Write \(B_{\ell,k}=C(0^{\ell},k)\), with \(\ell+1\) supports. Its rooted count is
\[
s_{B_{\ell,k}}=\ell+2^k.
\]

### Lemma B: count-dominated broom straightening

Let \(A,B,C\) be arbitrary disjoint nonempty rooted trees, with root \(w\) in \(A\). Attach \(B,C\) and \(B_{\ell,k}\) at \(w\), forming \(T\). Suppose
\[
s_B,s_C\ge\ell+2^k.
\tag{4.1}
\]
Assume either
\[
\ell\ge1,\ k\ge2,
\qquad\text{or}\qquad
\ell=0,\ k\ge3.
\]
Then one of these same-order changes strictly increases the global mean:

1. Shorten the final support of the broom into its predecessor when \(\ell\ge1\); when \(\ell=0\), fold its \(k\) leaves onto \(w\), retaining the star center as one more leaf at \(w\).
2. Retain all \(\ell+1\) supports as a bare path from \(w\) to the root of \(B\), moving \(B\)’s attachment from \(w\) to the terminal support. Distribute the original \(k\) terminal leaves as evenly as possible between the roots of \(B,C\). Permit both choices of the moved branch and both balanced allocations.

The proof of this lemma is a finite algebraic certificate for an unbounded parameter range. We specify the entire calculation next.

### 4.1 Variables and the exact shortening bound

Put
\[
p=s_A,\quad \alpha=t_A/p=1+c/2,\quad 0\le c\le p-1,
\]
\[
x=s_B,\quad y=s_C,\quad
U=\frac{t_B}{x(x+1)},\quad V=\frac{t_C}{y(y+1)}.
\]
The variable \(c\) is a real host-moment parameter, not a leaf count. Equations (1.4) and (1.6) imply
\[
\frac5{2(x+1)}\le U\le\frac12,
\qquad
\frac5{2(y+1)}\le V\le\frac12.
\tag{4.2}
\]
The rooted counts are at least five in the nonstar case, and at least eight in the star case, so (1.6) applies.

Let
\[
z=2^k,\quad S=p(x+1)(y+1),\quad
M=1+c/2+xU+yV,\quad d=q-M,
\]
\[
D=S+\ell-1>0,\qquad \chi_k=\frac{kz}{2(z-1)}.
\]
The symbol \(D\) here is a denominator, not \(n-q\).

The exact shortening/folding score is \((z-1)D(d_0-d)\), where
\[
\boxed{
d_0=\ell+\chi_k-
\frac{(\ell-1)M+(\ell-1)(\ell-2)/2}{S+\ell-1}.
}
\tag{4.3}
\]
For \(\ell\ge1\), this is the same interval count used in (3.3), specialized to an all-zero prefix. For \(\ell=0\), it becomes
\[
d_0=\chi_k+\frac{M-1}{S-1},
\]
which follows directly from the fold polynomial \((F_H(u)-u)((1+u)^k-1)\).

Thus failure of the first move gives \(d\ge d_0\).

### 4.2 Complete insertion counts

Allocate \(b\) terminal leaves to the moved branch \(B\), and \(k-b\) to \(C\). Put
\[
L=2^b,\qquad J=2^{k-b},\qquad LJ=z,\qquad h=\ell+1.
\]
For this paragraph write \(t_B=x(x+1)U\) and \(t_C=y(y+1)V\).

The old broom and new path-plus-\(B\) component have rooted moments
\[
s_P=\ell+z,\quad
 t_P=\ell(\ell+1)/2+z(h+k/2),
\]
\[
s_Q=h+Lx,\quad
 t_Q=h(h+1)/2+L\,[t_B+x(h+b/2)].
\tag{4.4}
\]
The old and new root-containing moments at \(w\) are
\[
s_0=S(1+s_P),\qquad t_0=s_0M+St_P,
\]
\[
s_1=p(1+s_Q)(1+Jy),
\]
\[
t_1=s_1(1+c/2)+p(1+Jy)t_Q
     +p(1+s_Q)J\,[t_C+(k-b)y/2].
\tag{4.5}
\]

The **full global increments**, including subtrees that avoid \(w\), are
\[
\boxed{
\Delta N=s_1-s_0+[(h+1)L-1]x+(J-1)y+h(1-z),
}
\tag{4.6}
\]
\[
\boxed{
\begin{aligned}
\Delta R={}&t_1-t_0+[(h+1)L-1]t_B+(J-1)t_C\\
&+\frac{Lx(h+1)(h+b)}2+\frac{Jy(k-b)}2\\
&+\frac{h(h+1)(1-z)}2-\frac{zkh}{2}.
\end{aligned}
}
\tag{4.7}
\]

For an independent derivation of the terms avoiding \(w\), adding \(b\) leaves at the root of \(B\) changes its global moments by
\[
N_B\mapsto N_B+(L-1)x+b,
\qquad
R_B\mapsto R_B+(L-1)t_B+bLx/2+b.
\]
Appending a bare path of \(h\) new vertices adds \(h(h+1)/2\) path-only subtrees and \(hLx\) mixed subtrees; their order sums are \(h(h+1)(h+2)/6\) and \(hL(t_B+bx/2)+Lxh(h+1)/2\). The original broom has
\[
N_P=k+\ell(\ell+1)/2+zh,
\qquad
R_P=k+\ell(\ell+1)(\ell+2)/6+zh(h+1+k)/2.
\]
Subtracting these expressions, and adding the change inside \(C\), gives exactly (4.6)–(4.7). The verifier checks the same identities by a separate symbolic joining calculation.

The fixed-source score of this insertion is
\[
\Sigma_b=\Delta R-(M+d)\Delta N.
\]
Let \(\mathcal I\) be its arithmetic average over both insertion sides and the allocations \(b\in\{\lfloor k/2\rfloor,\lceil k/2\rceil\}\), counting an even allocation once. It is an average of scores using the **same original \(q\)**, not an average of different means.

If \(\mathcal I>0\), at least one actual insertion strictly improves.

### 4.3 The finite polynomial assertion

The certificate verifies
\[
\boxed{\partial_d\mathcal I>0,\qquad
\mathcal I(U,V,d_0)>0}
\tag{4.8}
\]
throughout the parameter range of Lemma B and the rectangle (4.2).

Here is a complete specification of the polynomials and their proof. The expressions (4.4)–(4.7), their stated average, and (4.3) uniquely define everything that follows.

Put
\[
\mathcal H=8(z-1)D\,\mathcal I(U,V,d_0).
\tag{4.9}
\]
It is affine in \(U,V\). Define
\[
U_0=\frac5{2(x+1)},\quad U_1=\frac12,
\qquad
V_0=\frac5{2(y+1)},\quad V_1=\frac12,
\]
\[
Q_{ij}=(x+1)(y+1)\,\mathcal H(U_i,V_j).
\tag{4.10}
\]
Every cleared factor is strictly positive. By affinity, positivity at the four corners proves positivity on the whole rectangle. Symmetry makes \(Q_{01}\) the variable-swapped version of \(Q_{10}\), so only three corners require separate certificates.

#### Nonstars with \(k\ge8\): unbounded in both \(k\) and \(\ell\)

Write
\[
k=2g+e,\qquad e\in\{0,1\},\qquad v=2^g,\qquad g\ge4.
\]
The balanced powers are \((L,J)=(v,v)\) for \(e=0\), and \((v,2v),(2v,v)\) for \(e=1\). Also \(z=(1+e)v^2\).

Introduce independent nonnegative variables
\[
P=p-1-c,\qquad C=c,\qquad H=\ell-1,
\qquad X=x-\ell-z,\qquad Y=y-\ell-z.
\tag{4.11}
\]
For either parity and each of the three corners, expansion of \(Q_{ij}\) gives 576 nonzero monomials in \(P,C,H,X,Y\). Grouping by \(P,C,X,Y\) leaves **96 polynomials in \(H\)**:
\[
Q_{ij}=\sum_{\nu}P^{\nu_1}C^{\nu_2}X^{\nu_3}Y^{\nu_4}
       \sum_j f_{\nu j}(g,v)H^j.
\tag{4.12}
\]
Every \(f_{\nu j}\) is affine in \(g\).

Put \(W=v-16\ge0\). For every integer \(g\ge4\),
\[
\boxed{4\le g\le v/4=(W+16)/4.}
\tag{4.13}
\]
Indeed \(2^4=4\cdot4\), and doubling \(2^g\ge4g\) preserves the inequality at \(g+1\).

Write a coefficient after \(v=W+16\) as
\[
f=f_0(W)+g[f_+(W)+f_-(W)],
\]
where \(f_+\) has nonnegative coefficients and \(f_-\) has nonpositive coefficients, obtained by splitting the coefficient of \(g\) by monomial sign. Then
\[
\boxed{f\ge B(W):=f_0(W)+4f_+(W)+\frac{W+16}{4}f_-(W).}
\tag{4.14}
\]
The exact difference is
\[
(g-4)f_+(W)+\left(g-\frac{W+16}{4}\right)f_-(W)\ge0.
\]
This identity, including its direction, is checked for each coefficient.

For each grouped polynomial in (4.12), the lower polynomial
\[
\sum_j B_j(W)H^j
\]
has one of the following certificates:

- Every coefficient is nonnegative and \(B_0(0)>0\); or
- All \(B_j\), except possibly \(B_1\), have nonnegative coefficients, and an explicitly recorded positive rational \(\lambda\) gives
\[
\begin{aligned}
\sum_jB_jH^j={}&B_2[H-\lambda(W+16)]^2\\
&+[B_1+2\lambda(W+16)B_2]H\\
&+[B_0-\lambda^2(W+16)^2B_2]
 +\sum_{j\ge3}B_jH^j.
\end{aligned}
\tag{4.15}
\]
Both bracketed remainder polynomials have nonnegative coefficients, and the second has a strictly positive constant. Thus the expression is strictly positive for every \(H,W\ge0\).

**Every one of the 576 grouped certificates is included in the data files.** This counts two parities, three symmetry-distinct corners, and 96 groups. Their 3,456 coefficient lower bounds, exact expressions, square centers, and remainder polynomials are all recorded. No group or coefficient is omitted.

A representative certificate is short enough to display. In the even, upper–upper corner, the coefficient of \(P^2X^3Y^3\) is
\[
\begin{aligned}
G(H,g,v)={}&4(v^2-1)H^2\\
&+(8gv^2-4v^3+12v^2+4v-12)H\\
&+16gv^2+8v^4-16v^3+16v-8.
\end{aligned}
\]
Using \(g\ge4\),
\[
\begin{aligned}
G(H,g,v)\ge{}&4(v^2-1)(H-v/2)^2
 +(44v^2-12)H\\
&+7v^4-16v^3+65v^2+16v-8>0.
\end{aligned}
\tag{4.16}
\]
The final polynomial is positive for \(v\ge16\): \(7v^4-16v^3=v^3(7v-16)>0\), and the remaining terms are positive. The other recorded certificates use exactly the general form (4.15).

For transparency, the square-center ledger is:

| Parity | Corner | Certificates |
|---|---|---|
| Even | lower–lower | 96 coefficient-positive groups |
| Even | upper–lower | \(\lambda=1/4\): 48; \(3/8\): 32; \(1/2\): 16 |
| Even | upper–upper | \(\lambda=1/2\): 48; \(3/4\): 32; \(1\): 13; \(9/8\): 3 |
| Odd | lower–lower | 96 coefficient-positive groups |
| Odd | upper–lower | \(\lambda=3/8\): 48; \(5/8\): 32; \(3/4\): 16 |
| Odd | upper–upper | \(\lambda=3/4\): 48; \(9/8\): 32; \(3/2\): 13; \(13/8\): 3 |

The data associates each center with its precise monomial index. The centers are not numerical fits: substitution gives exact identities with rational coefficients, and every remainder coefficient is checked.

The same substitution proves \(\partial_d\mathcal I>0\) by nonnegative-coefficient expansion, with a strictly positive constant term. This has no dependence on \(U,V\).

Equations (4.12)–(4.15) establish (4.8) for every \(k\ge8\) and every \(\ell\ge1\). There is no upper bound on either parameter.

#### Nonstars with \(2\le k\le7\)

Substitute the exact powers \(z=2^k,L=2^b,J=2^{k-b}\). Keep \(\ell\), the other branch counts, and the host unbounded. After (4.11), group each corner polynomial by \(P,C,X,Y\) as above. Each of its 96 coefficient polynomials has the form
\[
a_0+a_1H+a_2H^2+\cdots.
\]
Either all coefficients are nonnegative with \(a_0>0\), or only \(a_1\) is negative, \(a_2>0\), and
\[
4a_0a_2-a_1^2>0.
\]
In the latter case the exact decomposition is
\[
a_2\left(H+\frac{a_1}{2a_2}\right)^2
+\frac{4a_0a_2-a_1^2}{4a_2}
+\sum_{j\ge3}a_jH^j>0.
\tag{4.17}
\]

| Terminal packet \(k\) | Coefficient-positive groups | Quadratic-square groups | Total groups |
|---:|---:|---:|---:|
| 2 | 288 | 0 | 288 |
| 3 | 288 | 0 | 288 |
| 4 | 285 | 3 | 288 |
| 5 | 273 | 15 | 288 |
| 6 | 261 | 27 | 288 |
| 7 | 225 | 63 | 288 |

All 1,728 boundary groups, including their exact coefficients and the 108 positive discriminants, are recorded. The derivative \(\partial_d\mathcal I\) is also coefficient-positive in every boundary case. This proves (4.8) at the remaining packets.

#### Stars: \(\ell=0,k\ge3\)

Set \(\ell=0\) in (4.3)–(4.10) and use
\[
P=p-1-c,\quad C=c,\quad X=x-z,\quad Y=y-z.
\]
At \(k=3\), each of the three corner numerators and the derivative has nonnegative coefficients and a positive constant. This is a fixed packet calculation with arbitrary host and branch counts.

For even \(k=2g\) and odd \(k=2g+1\), \(g\ge2\), set \(v=2^g\), \(W=v-4\), and use
\[
2\le g\le v/2.
\]
Apply the coefficient-sign splitting (4.14), replacing 4 and \((W+16)/4\) by 2 and \((W+4)/2\). All 576 corner-coefficient lower polynomials have nonnegative coefficients; their base coefficients have positive constants. The derivative certificates have the same property. No square in a path-length variable is needed because the arm has one support.

This proves (4.8) for every star packet \(k\ge3\).

### 4.4 Conclusion of Lemma B

If shortening or folding improves, the first alternative holds. Otherwise \(d\ge d_0\). The positive derivative in (4.8) and the corner certificates imply
\[
\mathcal I(U,V,d)\ge\mathcal I(U,V,d_0)>0.
\]
At least one of the actual balanced insertions therefore has strictly positive fixed-source score. All components remain connected by single attachment edges, and all leaf changes are reattachments; each competitor is a tree on exactly the original vertices.

This proves Lemma B, with the finite algebraic part supplied by (4.4)–(4.17) and the accompanying exact certificates. ∎

## 5. Completion for every order

We now prove the theorem.

Every tree of order at most three is a caterpillar. Fix \(n\ge4\) and let \(T\) be an arbitrary maximizer of mean subtree order among \(n\)-vertex trees. A maximum exists because there are finitely many labeled trees of fixed order.

Suppose \(T\) is not a caterpillar. By Section 1.3, no leaf has a degree-two neighbor. Select a terminal arm \(P\) of minimum rooted subtree count as in Section 2. Its terminal leaf packet is at least two.

If \(P\) has a positive internal leaf packet, its last such packet supplies the suffix in Lemma P. Lemma H supplies the required host bounds. Maximality makes shortening non-improving, so concentration strictly improves, a contradiction. Consequently \(P=B_{\ell,k}\) for some \(\ell\ge0,k\ge2\).

If \(\ell=0,k=2\), \(P\) is a terminal cherry at a skeleton branching vertex, contradicting the cherry lemma.

In every other case, choose two other non-leaf components \(B,C\) at its attachment vertex and retain everything else in \(A\). Lemma H gives
\[
s_B,s_C\ge s_P=\ell+2^k.
\]
All hypotheses of Lemma B hold. That lemma gives a same-order tree with strictly greater global mean, contradicting maximality.

Every case for \(\ell\ge0,k\ge2\) has been included. Therefore \(T\) is a caterpillar. Since the chosen maximizer was arbitrary and every contradiction was strict, **every** maximizer is a caterpillar. The existence statement follows immediately. ∎

### Where the infinite ranges are handled

There is no induction that merely advances the path-length cutoff one step. Arbitrary internal decoration is removed by Lemma P, whose inequalities hold for every suffix length. Arbitrary broom length is the free nonnegative variable \(H=\ell-1\) in the coefficient and square certificates. Arbitrary terminal packet size is covered by the two parities, the inequalities \(2^g\ge4g\), and the finite boundary packets. Host and other branch sizes remain independent unbounded variables throughout.

## 6. Verification, independence, and reproducibility

The executable `verify_jamison_all_orders.py` builds (4.4)–(4.7) from their direct formulas, and checks them against a separate global joining calculation with formal component moments. It reconstructs the polynomials from these definitions before proving their signs; it does not merely read a list claiming that signs are positive.

The executed algebra includes:

- 576 grouped unbounded broom certificates, with 3,456 exact coefficient lower-bound identities and 384 square certificates;
- 1,728 small-packet broom groups, including 108 strictly positive quadratic discriminants;
- the star certificates for \(k=3\) and the two unbounded parities;
- the derivative signs required before replacing \(d\) by its lower bound;
- all six cherry vertex certificates from Appendix B;
- the concentration-score identity, shortening correction, and host propagation identity.

The computer-assisted part consists of finite exact equalities and coefficient-sign checks whose mathematical domains are explicitly stated in Sections 3–4. It uses integer and rational arithmetic, not floating-point optimization.

### Supporting finite checks

An independent adjacency-based implementation enumerated all **81,134** unlabeled trees of orders four through seventeen. Of these, 16,637 were caterpillars. For every one of the **64,497 non-caterpillars**, the prescribed case analysis found an explicitly constructed same-order tree with strictly larger mean. The case counts were:

| Input configuration handled | Trees |
|---|---:|
| Leaf adjacent to degree-two vertex | 61,844 |
| Minimum-count arm is a cherry | 1,808 |
| Minimum-count arm is a nonstar broom | 585 |
| Minimum-count arm is a larger star | 240 |
| Minimum-count arm has an internal packet | 20 |

The adjacency code independently checks the selection and propagated host bounds on the actual graphs. It does not infer the existence of a move solely from formal moment tuples.

Another 30,000 seeded random configurations checked the minimum-count selection and its alternatives. The systematic broom tests included 1,440 configurations, bare-prefix lengths up to 1,000, and terminal packet sizes up to 1,024. These numerical endpoints are only sanity-test endpoints; the proof is unbounded.

Two examples were also counted by enumerating connected vertex subsets rather than using the rooted recurrence:

1. A central vertex with branches \(C(1,0,2),C(4),C(4)\), on seventeen vertices, has \((N,R)=(3821,37861)\). Concentrating the first branch’s internal leaf at its terminal support gives \((3249,32597)\), with integer improvement score
   \[
   32597\cdot3821-37861\cdot3249=1542748>0.
   \]
2. A central vertex with three branches \(C(0,4)\), on nineteen vertices, has \((5943,69363)\). A balanced insertion produces \(C(4,2,0,0,0,2,4)\), with \((5218,62038)\), and score
   \[
   62038\cdot5943-69363\cdot5218=6755700>0.
   \]

These four graphs required 1,310,716 nonempty subset connectivity tests. The examples and exhaustive finite tests support the implementation; they do not replace the proof of Sections 2–5.

### Commands

From the bundle directory:

```bash
python -m pip install sympy networkx
python verify_jamison_all_orders.py --part all --output-dir checks
python exhaustive_graph_check.py --max-order 17 --output checks/graph_checks.json
```

The algebra can also be run in independent phases:

```bash
python verify_jamison_all_orders.py --part even --output-dir checks
python verify_jamison_all_orders.py --part odd --output-dir checks
python verify_jamison_all_orders.py --part boundary --output-dir checks
python verify_jamison_all_orders.py --part stars --output-dir checks
python verify_jamison_all_orders.py --part base --output-dir checks
python verify_jamison_all_orders.py --part tests --output-dir checks
```

The JSON files record exact coefficients as rational strings, not approximate decimal numbers. Source-code and output hashes are supplied in the manifest for file integrity; hashes are not mathematical evidence.

### Remaining verification status

The candidate now contains a proof of the all-order claim, rather than a remaining unproved mathematical case. It has not been independently reviewed or formally verified. The principal items for an independent audit are the minimum-count injection and host propagation in Lemma H; the complete global score in Lemma P; the insertion count identities; the sign-preserving substitutions and exhaustive coefficient support in Lemma B; and the cherry base proof in Appendix B. No claim that LLM checking is independent human certification is intended.

## Appendix A. Source and dependency ledger

The original supplied `jamison_caterpillar_manuscript.pdf` provides the terminology, rooted joining identities, rooted first-moment upper bound, local-versus-global mean inequality, leaf-neighbor restriction, and spine-interval counting convention. The needed elementary arguments are restated in Section 1 and the exact comparisons above.

The earlier supplement `jamison_all_order_cherry_lemma.md` supplies the cherry base case. Its mathematical argument is reproduced in Appendix B, with local numbering, and its six certificate calculations were re-executed.

The **minimum-rooted-count selection**, the **host-ratio propagation**, the **last-internal-packet concentration lemma**, the **count-dominated arbitrary-length broom and star certificate**, and the **all-order assembly** are the new derivation of this continuation.

The original candidate’s asymptotic theorem, benchmark construction, numerical cutoff, and strengthened logarithmic deficit are not used. Neither are the later three-leaf, all-terminal-star, or two-vertex-arm supplements. The present candidate is therefore not relying on an unverified extension of those fixed-length arguments.

## Appendix B. Complete cherry base-case proof

The following reproduces the mathematical proof from the earlier cherry supplement. Its lemma numbers are local to this appendix. Its local result is the cherry lemma used in Section 1.4, not the whole all-order theorem. The proof is included so that the main chain does not rely on an unstated small-star assertion.

### B.1. Notation and elementary rooted facts

For a nonempty rooted tree \(X\), write

\[
(m,s,t,N,R)=(|V(X)|,s_X,t_X,N_X,R_X),\qquad \mu(X)=R/N.
\]

The quantities \(s,t\) count root-containing subtrees and sum their orders; \(N,R\) do the same for all nonempty connected induced vertex sets.

If the components after deleting the root have moments \((m_i,s_i,t_i,N_i,R_i)\), then

\[
s=\prod_i(1+s_i),\quad
 t=s\left(1+\sum_i\frac{t_i}{1+s_i}\right),\quad
 N=s+\sum_iN_i,\quad R=t+\sum_iR_i,\quad m=1+\sum_i m_i.
\tag{1}
\]

These formulas partition subtrees according to whether they contain the root.

#### Lemma 1: rooted first moment

For every rooted tree,
\[
2t\le s(s+1).
\tag{2}
\]

**Proof.** Induct on the order. For a singleton equality holds. Otherwise, induction and (1) give
\[
\frac ts=1+\sum_i\frac{t_i}{1+s_i}
\le1+\frac12\sum_i s_i
\le\frac{1+s}{2},
\]
because \(\prod_i(1+s_i)\ge1+\sum_i s_i\). Multiply by \(2s\). ∎

#### Lemma 2: local mean dominates global mean

For every choice of root,
\[
R/N\le t/s.
\tag{3}
\]

**Proof.** Put \(L=t/s\), \(L_i=t_i/s_i\). By (1)–(2),
\[
L-L_i
=1-\frac{t_i}{s_i(1+s_i)}
 +\sum_{j\ne i}\frac{t_j}{1+s_j}\ge\frac12.
\]
Induction gives \(R_i/N_i\le L_i<L\). Formula (1) expresses the global mean as a weighted average of \(L\) and these component means. ∎

### B.2. A count–moment inequality retaining unrooted information

#### Lemma 3

Every finite nonempty rooted tree satisfies
\[
\boxed{6t\le4N+s^2+5s-4m.}
\tag{4}
\]
Consequently, since \(m\ge t/s\),
\[
\boxed{
N\ge\left(\frac32+\frac1s\right)t-\frac{s^2+5s}{4}.
}
\tag{5}
\]

**Proof.** Use induction on \(m\). A singleton gives equality in (4). For a root-deletion component use the notation in (1), and put
\[
p_i=\frac{s}{1+s_i}\ge1,\qquad A=\sum_i s_i,\qquad Q=\sum_i s_i^2.
\]
The inductive hypotheses give
\[
4N_i-4m_i\ge6t_i-s_i^2-5s_i.
\]
Substitute in the left-hand side of (4), rearranged:
\[
\begin{aligned}
4N+s^2+5s-6t-4m
&\ge s^2+3s-4-Q-5A
       -6\sum_i(p_i-1)t_i\\
&\ge s^2+3s-4+2Q-2A-3sA.
\end{aligned}
\tag{6}
\]
The second inequality uses \(2t_i\le s_i(s_i+1)\) and \(p_i-1\ge0\).

It remains to show
\[
\mathcal G(p,A,Q):=p^2+3p+2Q-2A-3pA\ge4
\quad\text{when }p=\prod_i(1+s_i).
\tag{7}
\]
For the empty list, \(p=1,A=Q=0\), so \(\mathcal G=4\). Append an integer \(z\ge1\) to the list. The change is
\[
z[-3Ap+p^2z+2p^2-3pz+2z-2].
\]
Since \(A\le p-1\), it is at least
\[
z(z-1)(p-1)(p-2)\ge0.
\]
Indeed, \(p=1\) before any factor has been added, and afterwards the integer \(p\ge2\). Thus (7) follows by induction on the number of factors. Equations (6)–(7) prove (4). Finally substitute \(m\ge t/s\) into (4), rearranging to obtain (5). ∎

The important distinction from a rooted-deficit estimate alone is that (4)–(5) keep \(N\), the number of **all** subtrees. A proposed combination of rooted count and rooted mean therefore forces a minimum unrooted count as well.

### B.3. Exact cherry comparisons

Let \(H\) be a tree rooted at \(w\). Add new vertices \(u,\ell_1,\ell_2\) and edges \(wu,u\ell_1,u\ell_2\), obtaining \(T\). Write \(q=\mu(T)\).

The **fold** \(F\) moves \(\ell_1,\ell_2\) from \(u\) to \(w\), retaining \(wu\). If \(wz\) is an edge of \(H\), the **swing** \(C\) deletes \(wz\) and adds \(uz\).

The rooted three-vertex cherry has moments
\[
(s,t,N,R)=(4,8,6,10).
\]
Partitioning at the attachment edge gives, with \(S=s_H\) and \(M=t_H/S\),
\[
N_F-N_T=3(S-1),\qquad R_F-R_T=3MS+4S-7.
\tag{8}
\]
For the swing, let \(A,B\) be the components of \(H-wz\), rooted at \(w,z\). Put
\[
a=s_A,\quad \alpha=t_A/a,\qquad b=s_B,\quad \beta=t_B/b.
\]
Then
\[
N_C-N_T=b(4-a),
\]
\[
R_C-qN_C=b[(a-4)(q-\beta)-a\alpha+8].
\tag{9}
\]
All scores use the fixed original mean \(q\); positive score is exactly strict improvement.

#### Lemma 4: sufficient condition from the manuscript, with its missing factor restored

If
\[
25a^2+48a-120t_A\ge0,
\tag{10}
\]
then the fold or the swing strictly improves \(T\).

**Proof.** Suppose the fold does not improve. Since \(S=a(1+b)>1\) and \(M=\alpha+b\beta/(1+b)\), (8) implies
\[
q-M\ge\frac43+\frac{q-7/3}{S}.
\tag{11}
\]
As \(M\ge1\), rearranging proves \(q\ge7/3\). Lemma 1 gives \(\beta/(1+b)\le1/2\).

Root \(T\) at \(z\). Its local mean is
\[
\beta+\frac{5a}{1+5a}\left(\alpha+\frac85\right),
\]
so Lemma 2 gives
\[
q-\beta-2<\alpha-\frac25.
\tag{12}
\]
By (9), the swing score divided by \(ab\) equals
\[
q-M-\frac{\beta}{1+b}-\frac4a(q-\beta-2).
\]
Using (11)–(12), this is strictly greater than
\[
\frac56-\frac{4\alpha}{a}+\frac{8}{5a}
=\frac{25a^2+48a-120t_A}{30a^2}\ge0.
\]
Thus the swing strictly improves. ∎

### B.4. The three-branch lemma for every order

#### Theorem 5

Let \(B,C\) be arbitrary nonempty rooted trees satisfying \(s_B,s_C\ge4\). Form \(T\) by attaching \(B,C\) and a three-vertex cherry to a new vertex \(w\), and also attach \(c\ge0\) singleton leaves to \(w\).

Then at least one of the following strictly increases the mean subtree order while preserving the vertex set:

1. Fold the two cherry leaves onto \(w\).
2. Move the entire branch \(B\) from \(w\) to the cherry center.
3. Move the entire branch \(C\) from \(w\) to the cherry center.

There is no order cutoff.

#### Proof for \(c\ge2\)

Apply Lemma 4 to the edge attaching \(B\). The retained side \(A\) consists of \(w\), its \(c\) leaves, and \(C\). Set \(y=s_C\). Then
\[
a=2^c(1+y)\ge5\cdot2^c,
\qquad
\alpha=1+\frac c2+\frac{t_C}{1+y}
\le\frac{c+1}{2}+\frac{a}{2^{c+1}}.
\]
Consequently,
\[
\frac{25a^2+48a-120t_A}{a}
\ge(25-60/2^c)a-60c-12
\ge125\cdot2^c-60c-312>0.
\]
The final expression is 68 at \(c=2\), and increases thereafter. Lemma 4 applies.

#### Proof for \(c=0,1\): exact reduction to two variables

Put
\[
x=s_B,\quad y=s_C,\quad
U=\frac{t_B}{x(x+1)},\quad V=\frac{t_C}{y(y+1)}.
\]
By Lemma 1,
\[
x,y\ge4,\qquad 0<U,V\le\frac12.
\tag{13}
\]
Write
\[
p=2^c,\quad S=p(1+x)(1+y),\quad
M=1+\frac c2+xU+yV,\quad d=q-M.
\]
Suppose all three changes are non-improving. Equation (8) gives
\[
d\ge d_0:=\frac43+\frac{c/2+xU+yV}{S-1}.
\tag{14}
\]
The two swing inequalities from (9), weakened by replacing \(d\) by \(d_0\), are
\[
G_B:=[p(1+y)-4](d_0-U)-4yV+4-2c\le0,
\tag{15}
\]
\[
G_C:=[p(1+x)-4](d_0-V)-4xU+4-2c\le0.
\tag{16}
\]
Both replacement coefficients \(p(1+y)-4\) and \(p(1+x)-4\) are positive, so this weakening is valid.

The local mean of \(B\) is \((x+1)U\), and similarly for \(C\). The subtrees of \(T\) avoiding \(w\) lie in \(B,C\), in the cherry, or are one of the \(c\) singleton leaves. Thus
\[
\begin{aligned}
0=R_T-qN_T
&=5S(8/5-d)+(R_B-qN_B)+(R_C-qN_C)\\
&\quad+10+c-(6+c)q.
\end{aligned}
\tag{17}
\]
Apply Lemma 2 to \(B,C\). The resulting upper bound on (17) is strictly decreasing as a function of \(d\), with derivative
\[
-[5S+N_B+N_C+6+c]<0.
\]
It may therefore be further bounded above by its value at \(d=d_0\). Set
\[
q_0=M+d_0.
\]
Notice
\[
q_0-(x+1)U=1+c/2+yV+d_0-U>0,
\]
and likewise with \(B,C\) exchanged. Now, and only now, use Lemma 3 to replace \(N_B,N_C\) by the respective lower bounds
\[
\mathcal B_x(U)=\left(\frac32x+1\right)(x+1)U-\frac{x^2+5x}{4},
\qquad
\mathcal B_y(V)=\left(\frac32y+1\right)(y+1)V-\frac{y^2+5y}{4}.
\tag{18}
\]
This is valid even if a lower bound happens to be negative, since the coefficients just displayed are positive. The order of the preceding steps matters: monotonicity in \(d\) was used with the actual positive counts, not with possibly negative relaxed counts.

We obtain the necessary inequality
\[
\boxed{0\le\mathcal F_c(U,V),}
\tag{19}
\]
where
\[
\begin{aligned}
\mathcal F_c(U,V)
&=5S(8/5-d_0)\\
&\quad-\mathcal B_x(U)[q_0-(x+1)U]
      -\mathcal B_y(V)[q_0-(y+1)V]\\
&\quad-(6+c)q_0+10+c.
\end{aligned}
\tag{20}
\]
We next prove that (19) is impossible under (13), (15), and (16).

#### Why only four vertices need checking

For fixed \(x,y,c\), the constraints define a compact polygon \(\mathcal P\) in \([0,1/2]^2\). Both coefficients in each of the affine inequalities \(G_B,G_C\le0\) are negative. No point on \(U=0\) or \(V=0\) is feasible: for example, at \(U=0,V\le1/2\),
\[
G_C\ge[p(1+x)-4](4/3-1/2)+4-2c>0.
\]
The upper corner \((1/2,1/2)\) satisfies both inequalities strictly.

The common intersection of \(G_B=G_C=0\) is \(I=(U_I,V_I)\). For \(c=0\),
\[
U_I=\frac{4(x+2)}{15(x+1)},\qquad
V_I=\frac{4(y+2)}{15(y+1)}.
\tag{21}
\]
For \(c=1\),
\[
U_I=\frac{16x^2y+4x^2+24xy+x+2y-5}
 {6(x+1)(6xy+x+y-1)},
\tag{22}
\]
and \(V_I\) is obtained by exchanging \(x,y\). These lie strictly between zero and \(1/2\). In (22), positivity is immediate at \(x,y\ge4\), and the denominator minus twice the numerator is
\[
2(x-1)(2xy-x-y-2)>0.
\]

The right vertex is \(J=(1/2,V_J)\), with
\[
V_J=\frac{5xy+17x+5y+9}{6(4x+3)(y+1)}\quad(c=0),
\tag{23}
\]
\[
V_J=\frac{10xy^2+15xy-x+10y^2+10y-2}
 {6y(4x+3)(y+1)}\quad(c=1).
\tag{24}
\]
In each case \(0<V_J<1/2\). Substituting this right vertex into the other constraint gives
\[
G_C(J)=-\frac{x(7x-1)}{2(4x+3)}<0\quad(c=0),
\]
\[
G_C(J)=-\frac{(x-1)(2xy-x-y-2)}{3y(4x+3)}<0\quad(c=1).
\]
The top vertex is obtained by exchanging \(x,y\) and \(U,V\). These, together with \(I\) and the upper corner, are exactly the four vertices of \(\mathcal P\).

The function \(\mathcal F_c\) is quadratic in \(U,V\). Its \(U^2,V^2\) coefficients are positive and its \(UV\) coefficient is negative. To see this directly, put
\[
A_x=(3x/2+1)(x+1),\quad A_y=(3y/2+1)(y+1),
\quad d_x=x/(S-1),\ d_y=y/(S-1).
\]
The three coefficients are
\[
A_x(1-d_x)>0,\quad A_y(1-d_y)>0,
\quad-[A_x(y+d_y)+A_y(x+d_x)]<0.
\]
There is no interior local maximum, since restriction to a horizontal line is strictly convex. Every boundary edge is horizontal, vertical, or has negative slope. Restriction to any such edge is convex as well: if its direction is \((a,b)\) with \(ab\le0\), all three quadratic contributions to its second derivative are nonnegative. Therefore the maximum of \(\mathcal F_c\) occurs at a vertex.

#### The vertex certificates

Appendix B.A supplies exact polynomials proving
\[
\mathcal F_c(I)<0,\qquad
\mathcal F_c(J)<0,\qquad
\mathcal F_c(1/2,1/2)<0
\quad(c=0,1).
\tag{25}
\]
The top vertex follows by symmetry. These are polynomial inequalities for **every real** \(x,y\ge4\), not a finite sample of counts. Consequently \(\mathcal F_c<0\) on the entire polygon, contradicting (19). At least one move strictly improves, completing the proof of Theorem 5. ∎

### B.5. Excluding terminal cherries at skeleton branch vertices

#### Corollary 6

Let \(T\) be an order-\(n\) mean-subtree-order maximizer, with \(n\ge4\). Suppose \(u\) has precisely two leaf neighbors and one other neighbor \(w\). Then
\[
\boxed{\deg_{K(T)}(w)\le2.}
\tag{26}
\]

**Proof.** First recall the elementary leaf-neighbor restriction from manuscript Lemma 4.1. A maximizer of order \(n\ge4\) has \(q>2\): the four-vertex star proves this at \(n=4\), and the path mean \((n+2)/3\) proves it for \(n\ge5\). If a leaf \(z\) has degree-two neighbor \(v\), let \(a,b\) be rooted count and sum of \(T-\{v,z\}\) at the remaining neighbor of \(v\). Moving \(z\) to that remaining neighbor has score
\[
a\left(\frac ba+1-q\right)+q-2>0.
\]
Here \(b/a+1\) is the local mean of the original tree at that remaining neighbor and is at least \(q\) by Lemma 2. This contradicts maximality.

Consequently, every component of \(T-w\) rooted at a non-leaf neighbor of \(w\) has rooted count at least four. Indeed, its order is at most its rooted count (grow a rooted connected set through each order). A nontrivial component of rooted count at most three must be a two-vertex path or a three-vertex path rooted at an endpoint, either of which would exhibit a leaf with a degree-two neighbor in \(T\).

Suppose \(\deg_{K(T)}(w)\ge3\). Besides the cherry at \(u\), there are at least two other non-leaf components.

If there are exactly two, Theorem 5 applies, including every possible number of singleton leaves at \(w\), and produces a strict improvement.

If there are at least three, select one of them as \(B\) in Lemma 4. The retained \(A\) at \(w\) has at least two child components of rooted counts at least four. Put \(a=s_A\), \(\alpha=t_A/a\). Its child factors \(1+s_i\) are all at least two, with at least two at least five. Thus \(a\ge25\) and
\[
\sum_i s_i\le a/5+3.
\]
For completeness, retain one factor \(f\ge5\) and combine the rest into a product \(g\ge5\). The sum of the original factors minus one is at most \((f-1)+(g-1)\), and
\[
f+g-2\le fg/5+3
\]
follows from \((f-5)(g-5)\ge0\).

By Lemma 1,
\[
\alpha\le1+\tfrac12\sum_i s_i\le a/10+5/2.
\]
Hence
\[
25a^2+48a-120t_A
\ge a(13a-252)>0,
\]
since \(a\ge25\). Lemma 4 again supplies a strict improvement. Both cases contradict maximality, proving (26). ∎


### B.A. Exact positivity certificates

Set \(X=x-4\ge0\), \(Y=y-4\ge0\). At each indicated vertex, \(-\mathcal F_c\) is the shifted numerator below divided by the displayed denominator, which is positive for \(x,y\ge4\). For the upper and right vertices, the omitted top vertex follows by exchanging the two branches.

#### Central leaf count 0, middle vertex

\[
-\mathcal F_c=\frac{P(X,Y)}{900}.
\]

A sum-of-squares decomposition with nonnegative remaining coefficients is

\[
P(X,Y)=356 \left(X - Y\right)^{2}+\bigl[36 X^{2} Y + 103 X^{2} + 36 X Y^{2} + 279 X + 103 Y^{2} + 279 Y + 13464\bigr].
\]

Its strictly positive constant is 13464, proving strict positivity throughout the quadrant.

#### Central leaf count 0, upper vertex

\[
-\mathcal F_c=\frac{P(X,Y)}{12 x y + 12 x + 12 y}.
\]

All coefficients of the following expanded numerator are nonnegative:

\[
P(X,Y)=3 X^{3} Y^{2} + 38 X^{3} Y + 118 X^{3} + 3 X^{2} Y^{3} + 62 X^{2} Y^{2} + 571 X^{2} Y + 1705 X^{2} + 38 X Y^{3} + 571 X Y^{2} + 3984 X Y + 10454 X + 118 Y^{3} + 1705 Y^{2} + 10454 Y + 24336.
\]

Its strictly positive constant is 24336, proving strict positivity throughout the quadrant.

#### Central leaf count 0, right vertex

\[
-\mathcal F_c=\frac{P(X,Y)}{12 \left(4 x + 3\right)^{2}}.
\]

A sum-of-squares decomposition with nonnegative remaining coefficients is

\[
P(X,Y)=458 \left(X - Y\right)^{2}+\bigl[20 X^{4} Y + 304 X^{4} + 6 X^{3} Y^{2} + 149 X^{3} Y + 5288 X^{3} + 114 X^{2} Y^{2} + 33 X^{2} Y + 37296 X^{2} + 705 X Y^{2} + 131700 X + 964 Y^{2} + 705 Y + 185730\bigr].
\]

Its strictly positive constant is 185730, proving strict positivity throughout the quadrant.

#### Central leaf count 1, middle vertex

\[
-\mathcal F_c=\frac{P(X,Y)}{72 \left(6 x y + x + y - 1\right)^{2}}.
\]

All coefficients of the following expanded numerator are nonnegative:

\[
P(X,Y)=480 X^{4} Y^{3} + 8724 X^{4} Y^{2} + 48048 X^{4} Y + 83463 X^{4} + 480 X^{3} Y^{4} + 9040 X^{3} Y^{3} + 116574 X^{3} Y^{2} + 645519 X^{3} Y + 1174982 X^{3} + 8724 X^{2} Y^{4} + 116574 X^{2} Y^{3} + 972832 X^{2} Y^{2} + 4594312 X^{2} Y + 8055637 X^{2} + 48048 X Y^{4} + 645519 X Y^{3} + 4594312 X Y^{2} + 18628422 X Y + 30064868 X + 83463 Y^{4} + 1174982 Y^{3} + 8055637 Y^{2} + 30064868 Y + 45250668.
\]

Its strictly positive constant is 45250668, proving strict positivity throughout the quadrant.

#### Central leaf count 1, upper vertex

\[
-\mathcal F_c=\frac{P(X,Y)}{24 x y + 24 x + 24 y + 12}.
\]

All coefficients of the following expanded numerator are nonnegative:

\[
P(X,Y)=6 X^{3} Y^{2} + 82 X^{3} Y + 263 X^{3} + 6 X^{2} Y^{3} + 92 X^{2} Y^{2} + 912 X^{2} Y + 3035 X^{2} + 82 X Y^{3} + 912 X Y^{2} + 5844 X Y + 16729 X + 263 Y^{3} + 3035 Y^{2} + 16729 Y + 40570.
\]

Its strictly positive constant is 40570, proving strict positivity throughout the quadrant.

#### Central leaf count 1, right vertex

\[
-\mathcal F_c=\frac{P(X,Y)}{72 y^{2} \left(4 x + 3\right)^{2}}.
\]

All coefficients of the following expanded numerator are nonnegative:

\[
P(X,Y)=240 X^{4} Y^{3} + 4344 X^{4} Y^{2} + 23232 X^{4} Y + 38784 X^{4} + 216 X^{3} Y^{4} + 4704 X^{3} Y^{3} + 65526 X^{3} Y^{2} + 353688 X^{3} Y + 612096 X^{3} + 4050 X^{2} Y^{4} + 55649 X^{2} Y^{3} + 519128 X^{2} Y^{2} + 2518229 X^{2} Y + 4291602 X^{2} + 24267 X Y^{4} + 321386 X Y^{3} + 2418429 X Y^{2} + 10130572 X Y + 16183752 X + 47058 Y^{4} + 653276 Y^{3} + 4587808 Y^{2} + 17386724 Y + 25904712.
\]

Its strictly positive constant is 25904712, proving strict positivity throughout the quadrant.

