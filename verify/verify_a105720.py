# Independent check: fresh odd-only segmented sieve, exact Python-int sums.
import numpy as np, math, sys
n=111008771; lo_idx=n; hi_idx=2*n
def base_primes(m):
    s=bytearray([1])*(m+1); s[0]=s[1]=0
    for i in range(2,int(m**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(m+1) if s[i]]
LIM=4_800_000_000
bp=base_primes(int(LIM**.5)+2)[1:]   # odd base primes
count=1   # prime 2
total=0; p_lo=p_hi=None
SEG=1<<25   # odd numbers per segment
start=1     # odd numbers start, segment covers start, start+2, ...
while p_hi is None:
    s=np.ones(SEG,bool)
    if start==1: s[0]=False          # 1 is not prime
    end=start+2*SEG
    for p in bp:
        if p*p>=end: break
        first=max(p*p, ((start+p-1)//p)*p)
        if first%2==0: first+=p
        s[(first-start)//2::p]=False
    pr=(np.nonzero(s)[0]*2+start).astype(np.int64)
    c0=count; c1=count+len(pr)          # indices c0+1..c1
    if c1>=lo_idx and p_lo is None:
        p_lo=int(pr[lo_idx-c0-1])
    a=max(lo_idx,c0+1); b=min(hi_idx,c1)
    if a<=b:
        total+=int(pr[a-c0-1:b-c0].sum())
    if c1>=hi_idx:
        p_hi=int(pr[hi_idx-c0-1])
    count=c1; start=end
r=math.isqrt(total)
print("p_n =",p_lo,"p_2n =",p_hi)
print("a(n) =",total,"isqrt =",r,"square:",r*r==total)
