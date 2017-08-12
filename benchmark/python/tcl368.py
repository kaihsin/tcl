import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 12
b = 12
m = 16
o = 12
n = 12
p = 16
u = 16
v = 12
gflops = a*b*m*o*n*p*u*v*2/1e9
A = np.empty((p,v,n,u,o,m), order='f', dtype=np.float32)
B = np.empty((u,b,v,a), order='f', dtype=np.float32)
C = np.empty((m,a,n,b,o,p), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "p,v,n,u,o,m", B, "u,b,v,a", beta, C, "m,a,n,b,o,p" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("pvnuom,ubva->manbop", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC