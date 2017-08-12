import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 18
b = 18
m = 18
o = 16
n = 16
p = 18
u = 256
gflops = a*b*m*o*n*p*u*2/1e9
A = np.empty((n,u,m,o,p), order='f', dtype=np.float32)
B = np.empty((u,b,a), order='f', dtype=np.float32)
C = np.empty((o,a,p,b,m,n), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "n,u,m,o,p", B, "u,b,a", beta, C, "o,a,p,b,m,n" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("numop,uba->oapbmn", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC