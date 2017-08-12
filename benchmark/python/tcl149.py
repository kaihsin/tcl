import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 48
m = 40
u = 40
o = 40
n = 40
gflops = a*m*u*o*n*2/1e9
A = np.empty((a,u), order='f', dtype=np.float32)
B = np.empty((m,n,u,o), order='f', dtype=np.float32)
C = np.empty((a,n,o,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,u", B, "m,n,u,o", beta, C, "a,n,o,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("au,mnuo->anom", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC