#!/usr/bin/env python3
"""Regenerate publication figures from the exact, freshly computed experiment data.

No computed result is inferred from an illustration. Fractions are converted to
floating point only at the final plotting stage. Each chart uses one axes.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data';FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'serif','mathtext.fontset':'cm','font.size':10,
                     'axes.labelsize':11,'legend.fontsize':9,'xtick.labelsize':9,
                     'ytick.labelsize':9,'pdf.fonttype':42,'ps.fonttype':42})

def save(fig,name):
    fig.tight_layout(pad=0.5)
    fig.savefig(FIG/f'{name}.pdf',bbox_inches='tight')
    fig.savefig(FIG/f'{name}.png',bbox_inches='tight',dpi=180)
    plt.close(fig)


def number(x):return float(Fraction(x))


def tree_position(adj,left,right,bottom,top):
    parent={0:-1};order=[0];children={}
    for u in order:
        children[u]=sorted(v for v in adj[u] if v!=parent[u])
        for v in children[u]:parent[v]=u;order.append(v)
    depth={0:0}
    for u in order[1:]:depth[u]=depth[parent[u]]+1
    leafpos={};nextleaf=0
    def visit(u):
        nonlocal nextleaf
        if not children[u]:
            leafpos[u]=float(nextleaf);nextleaf+=1
        else:
            for v in children[u]:visit(v)
            leafpos[u]=sum(leafpos[v] for v in children[u])/len(children[u])
    visit(0)
    lo=min(leafpos.values());hi=max(leafpos.values());maxdepth=max(depth.values())
    return {u:(left+(right-left)*(leafpos[u]-lo)/max(hi-lo,1),
               top-(top-bottom)*depth[u]/max(maxdepth,1)) for u in order}


def graph_pair(example):
    fig,ax=plt.subplots(figsize=(6.4,3.05))
    for i,key in enumerate(('old_adjacency','new_adjacency')):
        adj=example[key];G=nx.Graph();G.add_nodes_from(range(len(adj)))
        G.add_edges_from((u,v) for u,row in enumerate(adj) for v in row if u<v)
        left,right=(0.2,4.5) if i==0 else (6.5,10.8)
        pos=tree_position(adj,left,right,0.25,2.9)
        nx.draw_networkx_edges(G,pos,ax=ax,width=0.9)
        leaves=[u for u in G if G.degree(u)==1]
        supports=[u for u in G if G.degree(u)>1 and u!=0]
        nx.draw_networkx_nodes(G,pos,nodelist=leaves,node_size=19,ax=ax)
        nx.draw_networkx_nodes(G,pos,nodelist=supports,node_size=38,ax=ax)
        nx.draw_networkx_nodes(G,pos,nodelist=[0],node_shape='s',node_size=44,ax=ax)
        ax.text(pos[0][0]+0.14,pos[0][1]+0.05,r'$w$',fontsize=10)
        ax.text((left+right)/2,3.25,r'$T$' if i==0 else r'$G$',ha='center',fontsize=12)
    ax.annotate('',xy=(6.0,1.65),xytext=(5.0,1.65),arrowprops={'arrowstyle':'->','lw':1.2})
    ax.set_xlim(-0.1,11.2);ax.set_ylim(0,3.5);ax.axis('off')
    save(fig,f"{example['name']}_trees")


def main():
    d=json.loads((DATA/'experiments.json').read_text());rows=d['by_order'];ns=[r['n'] for r in rows]
    fig,ax=plt.subplots(figsize=(6.4,3.55))
    ax.plot(ns,[number(r['maximum_mean'])/r['n'] for r in rows],marker='o',ms=4,lw=1.6,label='Maximum over all trees')
    non=[r for r in rows if r['maximum_noncaterpillar_mean'] is not None]
    ax.plot([r['n'] for r in non],[number(r['maximum_noncaterpillar_mean'])/r['n'] for r in non],marker='s',ms=4,lw=1.3,ls='--',label='Maximum over non-caterpillars')
    ax.plot(ns,[(n+2)/(3*n) for n in ns],ls=':',lw=1.3,label=r'Path $P_n$')
    ax.plot(ns,[float(Fraction((n+1)*2**(n-2)+n-1,2**(n-1)+n-1)/n) for n in ns],ls='-.',lw=1.3,label=r'Star $K_{1,n-1}$')
    ax.set(xlabel=r'Tree order $n$',ylabel=r'Mean subtree density $\mu(T)/n$',xticks=ns)
    ax.legend(loc='best',frameon=False,ncol=2);ax.grid(axis='y',alpha=.2)
    save(fig,'extremal_density')

    fig,ax=plt.subplots(figsize=(6.4,3.3))
    xx=[r['n'] for r in non]
    ax.plot(xx,[number(r['extremal_gap']) for r in non],marker='o',ms=4,lw=1.5)
    ax.set(xlabel=r'Tree order $n$',ylabel=r'Extremal separation $\delta_n$',xticks=xx)
    ax.set_ylim(bottom=0);ax.grid(axis='y',alpha=.2)
    save(fig,'extremal_separation')

    fig,ax=plt.subplots(figsize=(6.4,3.3))
    ax.plot(xx,[number(r['minimum_constructive_gain']) for r in non],marker='o',ms=4,label='Minimum observed gain')
    ax.plot(xx,[number(r['median_constructive_gain']) for r in non],marker='s',ms=4,ls='--',label='Median observed gain')
    ax.set_yscale('log')
    ax.set(xlabel=r'Tree order $n$',ylabel=r'Constructive mean gain $g(T)$',xticks=xx)
    ax.grid(axis='y',which='both',alpha=.2);ax.legend(frameon=False,loc='best')
    save(fig,'constructive_gains')

    fig,ax=plt.subplots(figsize=(6.4,3.5))
    names=[('leaf_degree_two','Leaf / degree-two neighbor','o'),('cherry','Terminal cherry','s'),('broom','Nonstar broom','^'),('star','Larger terminal star','D'),('internal_packet','Internal leaf packet','v')]
    for key,title,marker in names:
        vals=[r for r in rows if r['counts'].get(key,0)>0]
        ax.plot([r['n'] for r in vals],[r['counts'][key] for r in vals],marker=marker,ms=4,label=title)
    ax.set_yscale('log');ax.set(xlabel=r'Tree order $n$',ylabel='Number handled in the prescribed case',xticks=xx)
    ax.legend(frameon=False,ncol=2,loc='best');ax.grid(axis='y',alpha=.2)
    save(fig,'case_coverage')

    for ex in d['examples']:
        graph_pair(ex)
        fig,ax=plt.subplots(figsize=(6.4,3.15))
        kk=list(range(1,ex['n']+1));N=ex['old_N'];Nz=ex['new_N']
        p=[v/N for v in ex['old_distribution'][1:]];pz=[v/Nz for v in ex['new_distribution'][1:]]
        ax.plot(kk,p,marker='o',ms=3,lw=1.35,label=rf"Source $T$: $\mu={ex['old_R']/N:.4f}$")
        ax.plot(kk,pz,marker='s',ms=3,lw=1.35,ls='--',label=rf"Competitor $G$: $\mu={ex['new_R']/Nz:.4f}$")
        ax.set(xlabel=r'Subtree order $j$',ylabel=r'Proportion $a_j(T)/N_T$',xticks=kk)
        ax.set_ylim(bottom=0);ax.legend(frameon=False,loc='best');ax.grid(axis='y',alpha=.2)
        save(fig,f"{ex['name']}_distribution")
    files=sorted(p.name for p in FIG.glob('*.pdf'))
    print('Generated',len(files),'vector PDF figures from freshly executed exact computations:')
    print('\n'.join(files))

if __name__=='__main__':main()
