import numpy as np
def small_primes(n):
    s=np.ones(n+1,bool); s[:2]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
def prime_stream(seg=1<<24):
    """Yield numpy arrays of consecutive primes (int64), unbounded."""
    base=small_primes(1<<17)
    lo=0
    while True:
        hi=lo+seg
        lim=int(hi**0.5)+1
        if lim>base[-1]: base=small_primes(lim*2)
        s=np.ones(seg,bool)
        if lo==0: s[:2]=False
        for p in base[base<=lim]:
            st=max(p*p,((lo+p-1)//p)*p)
            s[st-lo::p]=False
        yield (np.nonzero(s)[0]+lo).astype(np.int64)
        lo=hi
class Reader:
    def __init__(self): self.g=prime_stream(); self.buf=np.empty(0,np.int64)
    def take(self,k):
        while len(self.buf)<k: self.buf=np.concatenate([self.buf,next(self.g)])
        out=self.buf[:k]; self.buf=self.buf[k:]; return out
