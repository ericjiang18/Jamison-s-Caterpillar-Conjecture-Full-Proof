"""Independent adjacency-based checks of the constructive proof steps.

Finite tests only. NetworkX is used solely to enumerate unlabeled input trees;
all modifications and subtree counts are implemented here on adjacency sets.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import random
from typing import Any
from verify_jamison_all_orders import Moments,ONE,join,word,score,require


def component(adj:list[set[int]],start:int,avoid:int)->set[int]:
    seen={start};todo=[start]
    for u in todo:
        for v in adj[u]:
            if v!=avoid and v not in seen:seen.add(v);todo.append(v)
    return seen


def rooted(adj:list[set[int]],root:int,allowed:set[int]|None=None)->Moments:
    if allowed is None:allowed=set(range(len(adj)))
    parent={root:-1};order=[root]
    for u in order:
        for v in adj[u]:
            if v in allowed and v!=parent[u]:
                require(v not in parent,'cycle in adjacency test')
                parent[v]=u;order.append(v)
    require(len(order)==len(allowed),'disconnected adjacency test')
    vals={}
    for u in reversed(order):
        row=ONE
        for v in adj[u]:
            if parent.get(v)==u:row=join(row,vals[v])
        vals[u]=row
    return vals[root]


def move_edge(adj:list[set[int]],old_parent:int,child:int,new_parent:int):
    require(child in adj[old_parent] and child not in adj[new_parent])
    adj[old_parent].remove(child);adj[child].remove(old_parent)
    adj[new_parent].add(child);adj[child].add(new_parent)


def clone(adj):return [set(row) for row in adj]


def caterpillar(adj)->bool:
    K={u for u,row in enumerate(adj) if len(row)>=2}
    return all(len(adj[u]&K)<=2 for u in K)


def improve(adj:list[set[int]], *, return_graph:bool=False)->dict[str,Any]:
    """Find a strictly improving tree when the input is not a caterpillar."""
    if caterpillar(adj):return {'case':'caterpillar'}
    n=len(adj);T=rooted(adj,0)
    require(T.R>2*T.N,'test inputs should have mean greater than two')
    for leaf,row in enumerate(adj):
        if len(row)==1:
            u=next(iter(row))
            if len(adj[u])==2:
                w=next(iter(adj[u]-{leaf}));G=clone(adj);move_edge(G,u,leaf,w)
                delta=score(T,rooted(G,0));require(delta>0,'pendant-path fold')
                out={'case':'leaf_degree_two','cross_score':delta}
                if return_graph:out['graph']=G
                return out
    K={u for u,row in enumerate(adj) if len(row)>=2}
    kd={u:len(adj[u]&K) for u in K}
    arms=[]
    for w in sorted(K):
        if kd[w]<3:continue
        for start in sorted(adj[w]&K):
            path=[];previous=w;u=start
            while kd[u]<=2:
                path.append(u)
                successors=(adj[u]&K)-{previous}
                if not successors:break
                require(len(successors)==1)
                previous,u=u,next(iter(successors))
            else:continue
            if kd[path[-1]]!=1:continue
            vertices=component(adj,start,w)
            moments=rooted(adj,start,vertices)
            packets=tuple(len(adj[v]-K) for v in path)
            require(moments==word(packets),'word versus adjacency moments')
            arms.append((moments.s,w,start,path,packets,vertices))
    require(bool(arms),'non-caterpillar has a terminal arm')
    m,w,start,path,packets,pvertices=min(arms,key=lambda item:(item[0],item[1],item[2]))
    others=sorted((adj[w]&K)-{start});require(len(others)>=2)
    for r in others:
        require(rooted(adj,r,component(adj,r,w)).s>=m,'minimum-count side dominance')
    br,cr=others[:2];bv=component(adj,br,w);cv=component(adj,cr,w)
    av=set(range(n))-bv-cv-pvertices
    A=rooted(adj,w,av);B=rooted(adj,br,bv);C=rooted(adj,cr,cv)
    H0=rooted(adj,w,set(range(n))-pvertices)
    require(H0.s>=(m+1)**2 and H0.t*(m+1)<=H0.s**2,'host bounds')
    terminal=path[-1];packet_leaves=sorted(adj[terminal]-K);k=len(packet_leaves)
    require(k>=2,'terminal packet size')
    candidates=[]
    # The shortening/folding alternative.
    G=clone(adj);predecessor=w if len(path)==1 else path[-2]
    for leaf in packet_leaves:move_edge(G,terminal,leaf,predecessor)
    candidates.append(('shorten' if len(path)>1 else 'fold',G))
    if any(packets[:-1]):
        last=max(i for i,a in enumerate(packets[:-1]) if a)
        support=path[last];H_vertices=set(range(n))-component(adj,support,w if last==0 else path[last-1])
        Hroot=w if last==0 else path[last-1]
        HH=rooted(adj,Hroot,H_vertices)
        suffix_s=rooted(adj,support,set(range(n))-H_vertices).s
        require(HH.s>=(suffix_s+1)**2 and HH.t*(suffix_s+1)<=HH.s**2,
                'propagated host bounds')
        G=clone(adj)
        for leaf in sorted(adj[support]-K):move_edge(G,support,leaf,terminal)
        candidates.append(('concentrate',G));kind='internal_packet'
    elif len(path)==1 and k==2:
        for r in others:
            G=clone(adj);move_edge(G,w,r,terminal);candidates.append(('cherry_swing',G))
        kind='cherry'
    else:
        for b in sorted({k//2,(k+1)//2}):
            for rb,rc in ((br,cr),(cr,br)):
                G=clone(adj);move_edge(G,w,rb,terminal)
                for idx,leaf in enumerate(packet_leaves):
                    move_edge(G,terminal,leaf,rb if idx<b else rc)
                candidates.append(('balanced_insertion',G))
        kind='broom' if len(path)>1 else 'star'
    computed=[(score(T,rooted(G,0)),name,G) for name,G in candidates]
    best,name,G=max(computed,key=lambda item:item[0])
    require(best>0,repr({'n':n,'edges':[(i,j) for i,row in enumerate(adj) for j in row if i<j],
                        'packets':packets,'case':kind,'scores':[(a,b) for a,b,_ in computed]}))
    out={'case':kind,'move':name,'cross_score':best,'selected_packets':list(packets)}
    if return_graph:out['graph']=G
    return out


def check_through_order(max_order:int)->dict[str,Any]:
    import networkx as nx
    require(max_order>=4)
    ledger=[];total=Counter()
    for n in range(4,max_order+1):
        counts=Counter()
        for T in nx.nonisomorphic_trees(n):
            adj=[set(T.neighbors(u)) for u in range(n)]
            outcome=improve(adj)
            counts['trees']+=1;counts[outcome['case']]+=1
        total.update(counts);ledger.append({'n':n,**dict(counts)})
        print('adjacency enumeration',n,dict(counts),flush=True)
    return {'maximum_order':max_order,'total':dict(total),'by_order':ledger}


def make_three_arms(packets:list[tuple[int,...]])->list[set[int]]:
    adj=[set()]
    def add(parent):
        idx=len(adj);adj.append({parent});adj[parent].add(idx);return idx
    for word0 in packets:
        previous=0
        for k in word0:
            u=add(previous)
            for _ in range(k):add(u)
            previous=u
    return adj


def connected_subset_counts(adj:list[set[int]])->tuple[int,int]:
    """Brute connected induced-subset enumeration, independent of recurrences."""
    n=len(adj);require(n<=21,'subset sanity check intentionally bounded')
    neigh=[sum(1<<j for j in row) for row in adj]
    N=R=0
    for mask in range(1,1<<n):
        reached=mask & -mask;front=reached
        while front:
            bit=front & -front;front^=bit
            extra=neigh[bit.bit_length()-1]&mask&~reached
            reached|=extra;front|=extra
        if reached==mask:N+=1;R+=mask.bit_count()
    return N,R


def example_checks()->dict[str,Any]:
    G=make_three_arms([(1,0,2),(4,),(4,)])
    # Gather the single proximal leaf of the first arm at its terminal support.
    K={u for u,row in enumerate(G) if len(row)>=2}
    start=next(u for u in G[0] if len(component(G,u,0))==6)
    path=[start];prev=0;u=start
    while (G[u]&K)-{prev}:
        nxt=next(iter((G[u]&K)-{prev}));path.append(nxt);prev,u=u,nxt
    Q=clone(G)
    for leaf in G[start]-K:move_edge(Q,start,leaf,path[-1])
    gcount=connected_subset_counts(G);qcount=connected_subset_counts(Q)
    require(gcount==(3821,37861) and qcount==(3249,32597),'17-vertex example')
    require(score(rooted(G,0),rooted(Q,0))==1542748)
    B=make_three_arms([(0,4)]*3)
    bout=improve(B,return_graph=True);Z=bout['graph']
    # The algorithm may choose a symmetric maximum-score insertion; the
    # previously displayed 19-vertex counts are independent of that orientation.
    bcount=connected_subset_counts(B);zcount=connected_subset_counts(Z)
    require(bcount==(5943,69363) and zcount==(5218,62038),'19-vertex example')
    return {'concentration_17_vertices':{'old':gcount,'new':qcount,'cross_score':1542748},
            'broom_19_vertices':{'old':bcount,'new':zcount,'cross_score':6755700},
            'nonempty_subsets_checked':2*((1<<17)-1)+2*((1<<19)-1)}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--max-order',type=int,default=16)
    p.add_argument('--output',type=Path,default=Path('graph_checks.json'));a=p.parse_args()
    out={'enumeration':check_through_order(a.max_order),'examples':example_checks()}
    a.output.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
