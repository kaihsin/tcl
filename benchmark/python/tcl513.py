import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 480
m = 24
n = 24
u = 24
w = 24
v = 24
gflops = a*m*n*u*w*v*2/1e9
A = np.empty((u,n,w,m,v), order='f', dtype=np.float32)
B = np.empty((a,w,v,u), order='f', dtype=np.float32)
C = np.empty((n,m,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,n,w,m,v", B, "a,w,v,u", beta, C, "n,m,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("unwmv,awvu->nma", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC