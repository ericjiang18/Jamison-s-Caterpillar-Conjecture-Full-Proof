#!/usr/bin/env python3
"""Finite supporting experiments for the Jamison manuscript; not an infinite proof.

Input trees: all NetworkX nonisomorphic trees with 4 <= n <= max_order.
All extremal comparisons and improvement checks use Python integers or Fraction.
The manuscript's supplied transformation routine is called without modification.
Its returned graph is recounted with a separate implementation below.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, platform, sys, time
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'verification'))
import networkx as nx
from exhaustive_graph_check import improve, make_three_arms, clone, move_edge, component


def counts(adj: list[set[int]]) -> tuple[int, int]:
    """Count connected vertex subsets by highest vertex in a rooted traversal."""
    n = len(adj)
    if n == 0: raise ValueError('Trees must be nonempty')
    parent = [-2] * n; parent[0] = -1; order = [0]
    for u in order:
        for v in sorted(adj[u]):
            if v == parent[u]: continue
            if parent[v] != -2: raise ValueError('Cycle or inconsistent adjacency')
            parent[v] = u; order.append(v)
    if len(order) != n: raise ValueError('Disconnected graph')
    s = [0]*n; t = [0]*n; N = [0]*n; R = [0]*n
    for u in reversed(order):
        ss=tt=1; nn=rr=0
        for v in sorted(adj[u]):
            if parent[v] == u:
                tt = tt*(1+s[v]) + ss*t[v]
                ss *= 1+s[v]
                nn += N[v]; rr += R[v]
        s[u],t[u],N[u],R[u] = ss,tt,ss+nn,tt+rr
    return N[0],R[0]


def is_caterpillar(adj: list[set[int]]) -> bool:
    inside = [len(neigh) >= 2 for neigh in adj]
    return all(sum(inside[v] for v in neigh) <= 2 for u,neigh in enumerate(adj) if inside[u])


def graph6(adj: list[set[int]]) -> str:
    G=nx.Graph();G.add_nodes_from(range(len(adj)))
    G.add_edges_from((u,v) for u,row in enumerate(adj) for v in row if u<v)
    return nx.to_graph6_bytes(G,header=False).decode().strip()


def rational(x: Fraction | None) -> str | None:
    return None if x is None else str(x)


def median(xs: list[Fraction]) -> Fraction:
    ys=sorted(xs); m=len(ys)//2
    return ys[m] if len(ys)%2 else (ys[m-1]+ys[m])/2


def subset_distribution(adj: list[set[int]]) -> list[int]:
    """Independent bitset connectivity test of EVERY nonempty vertex subset."""
    n=len(adj); neigh=[sum(1<<v for v in row) for row in adj]; out=[0]*(n+1)
    for mask in range(1,1<<n):
        seen=mask&-mask;front=seen
        while front:
            bit=front&-front;front^=bit
            extra=neigh[bit.bit_length()-1]&mask&~seen
            seen|=extra;front|=extra
        if seen==mask: out[mask.bit_count()]+=1
    return out


def example_graphs() -> list[tuple[str,list[set[int]],list[set[int]]]]:
    G=make_three_arms([(1,0,2),(4,),(4,)])
    K={u for u,row in enumerate(G) if len(row)>=2}
    start=next(u for u in G[0] if len(component(G,u,0))==6)
    path=[start];prev=0;u=start
    while (G[u]&K)-{prev}:
        nxt=next(iter((G[u]&K)-{prev}));path.append(nxt);prev,u=u,nxt
    Z=clone(G)
    for leaf in sorted(G[start]-K):move_edge(Z,start,leaf,path[-1])
    H=make_three_arms([(0,4)]*3)
    # Keep labels fixed: select the first branch; move the second to its tip.
    roots=sorted(H[0]);chosen=roots[0];moved=roots[1];retained=roots[2]
    tip=next(v for v in H[chosen] if v!=0)
    leafs=sorted(v for v in H[tip] if v!=chosen)
    Y=clone(H);move_edge(Y,0,moved,tip)
    for i,leaf in enumerate(leafs):move_edge(Y,tip,leaf,moved if i<2 else retained)
    return [('concentration',G,Z),('insertion',H,Y)]


def run(max_order: int, outdir: Path) -> dict[str,Any]:
    if not 7 <= max_order <= 20: raise ValueError('Choose max_order between 7 and 20')
    outdir.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();summaries=[];totals=Counter()
    fields=['n','input_graph6','output_graph6','case','move','N_old','R_old','N_new','R_new','cross_score','mean_gain']
    with (outdir/'noncaterpillar_moves.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for n in range(4,max_order+1):
            cases=Counter();gains=[];lo=hi=catmax=nonmax=None;maximizers=0;bestg=None
            for G in nx.nonisomorphic_trees(n):
                adj=[set(G.neighbors(u)) for u in range(n)]
                N,R=counts(adj);mu=Fraction(R,N);cat=is_caterpillar(adj)
                cases['trees']+=1
                lo=mu if lo is None else min(lo,mu)
                if hi is None or mu>hi:
                    hi=mu;maximizers=1;bestg=graph6(adj)
                elif mu==hi:maximizers+=1
                if cat:
                    cases['caterpillar']+=1;catmax=mu if catmax is None else max(catmax,mu)
                    continue
                nonmax=mu if nonmax is None else max(nonmax,mu)
                got=improve(adj,return_graph=True);Z=got['graph'];Nz,Rz=counts(Z)
                if len(Z)!=n or sum(map(len,Z)) != 2*(n-1): raise AssertionError('Not a same-order tree')
                cross=Rz*N-R*Nz
                if cross != got['cross_score'] or cross<=0:raise AssertionError('Improvement or recount mismatch')
                gain=Fraction(cross,N*Nz);gains.append(gain);cases[got['case']]+=1
                writer.writerow(dict(n=n,input_graph6=graph6(adj),output_graph6=graph6(Z),case=got['case'],move=got.get('move','pendant_path_fold'),N_old=N,R_old=R,N_new=Nz,R_new=Rz,cross_score=cross,mean_gain=str(gain)))
            # These are exact finite observations, not assumptions of the proof.
            if hi != catmax:raise AssertionError('Noncaterpillar attains the finite maximum')
            if lo != Fraction(n+2,3):raise AssertionError('Path minimum check failed')
            if nonmax is not None and not nonmax < hi:raise AssertionError('A noncaterpillar ties the finite maximum')
            row={'n':n,'counts':dict(cases),'minimum_mean':str(lo),'maximum_mean':str(hi),
                 'maximum_caterpillar_mean':str(catmax),'maximum_noncaterpillar_mean':rational(nonmax),
                 'extremal_gap':rational(hi-nonmax if nonmax is not None else None),
                 'maximizer_count':maximizers,'maximizer_graph6':bestg,
                 'minimum_constructive_gain':rational(min(gains) if gains else None),
                 'median_constructive_gain':rational(median(gains) if gains else None),
                 'maximum_constructive_gain':rational(max(gains) if gains else None)}
            summaries.append(row);totals.update(cases)
            print('completed order',n,'trees',cases['trees'],'max',hi,'cases',dict(cases),flush=True)
            (outdir/'enumeration_partial.json').write_text(json.dumps(summaries,indent=2))
    examples=[]
    for name,old,new in example_graphs():
        ds=subset_distribution(old);dz=subset_distribution(new)
        N=sum(ds);R=sum(i*v for i,v in enumerate(ds));Nz=sum(dz);Rz=sum(i*v for i,v in enumerate(dz))
        if (N,R)!=counts(old) or (Nz,Rz)!=counts(new):raise AssertionError('Independent subset enumeration mismatch')
        row={'name':name,'n':len(old),'old_N':N,'old_R':R,'new_N':Nz,'new_R':Rz,
             'mean_gain':str(Fraction(Rz,Nz)-Fraction(R,N)), 'cross_score':Rz*N-R*Nz,
             'old_adjacency':[sorted(a) for a in old],'new_adjacency':[sorted(a) for a in new],
             'old_distribution':ds,'new_distribution':dz,
             'nonempty_subsets_tested':2*((1<<len(old))-1)}
        examples.append(row)
        with (outdir/f'{name}_distribution.csv').open('w',newline='') as f:
            wr=csv.writer(f);wr.writerow(['subtree_order','source_count','competitor_count','source_probability','competitor_probability'])
            for k in range(1,len(old)+1):wr.writerow([k,ds[k],dz[k],str(Fraction(ds[k],N)),str(Fraction(dz[k],Nz))])
        print('example',name,'source',N,R,'competitor',Nz,Rz,'score',row['cross_score'],flush=True)
    result={'scope':'Fresh finite computations; not an independent proof of the all-order claim',
            'maximum_order':max_order,'totals':dict(totals),'by_order':summaries,'examples':examples,
            'elapsed_seconds':round(time.monotonic()-start,3),
            'environment':{'python':sys.version,'networkx':nx.__version__,'platform':platform.platform()},
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'verification'/'exhaustive_graph_check.py',ROOT/'verification'/'verify_jamison_all_orders.py']}}
    (outdir/'experiments.json').write_text(json.dumps(result,indent=2))
    # Portable summary table for plotting/reuse.
    flds=['n','trees','caterpillar','maximum_mean','maximum_noncaterpillar_mean','extremal_gap','minimum_constructive_gain','median_constructive_gain','maximizer_count']
    with (outdir/'enumeration_summary.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=flds);wr.writeheader()
        for row in summaries:wr.writerow({k:(row['counts'].get(k,0) if k in ('trees','caterpillar') else row.get(k)) for k in flds})
    print('TOTAL',dict(totals),'seconds',result['elapsed_seconds'],flush=True)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--max-order',type=int,default=17);ap.add_argument('--output-dir',type=Path,default=ROOT/'data');args=ap.parse_args()
    run(args.max_order,args.output_dir)
