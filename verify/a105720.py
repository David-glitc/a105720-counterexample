# a(n) = sum_{i=n}^{2n} p_i ; squares known at n=3,6,4072. Search further.
import sys, numpy as np, math, time
from primes import Reader
N=int(sys.argv[1]); L=1<<20
lower=Reader(); upper=Reader()
# a(1)=p1+p2
up=upper.take(2); a=int(up.sum()); n=1; t0=time.time(); hits=[]
pending_low=lower.take(1)  # p1
while n<N:
    lo=np.concatenate([pending_low, lower.take(L)])   # p_n .. p_{n+L}
    hi=upper.take(2*L)                                  # p_{2n+1} .. p_{2n+2L}
    delta=-lo[:L]+hi[0::2]+hi[1::2]                     # a(n+j+1)-a(n+j)
    vals=a+np.cumsum(delta)                             # a(n+1..n+L)
    vals=np.concatenate([[a],vals[:-1]])               # a(n..n+L-1)
    r=np.rint(np.sqrt(vals.astype(np.float64))).astype(np.int64)
    for d in (-1,0,1):
        rr=r+d; idx=np.nonzero(rr*rr==vals)[0]
        for i in idx: hits.append((n+int(i), int(vals[i])))
    a=int(vals[-1]+delta[-1]); n+=L; pending_low=lo[L:L+1]
    print(f"n<{n:,} a~{a:.3e} hits {sorted(set(hits))} {time.time()-t0:.0f}s", flush=True)
