import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
c = 15
b = 15
m = 16
o = 15
n = 15
u = 2400
gflops = a*c*b*m*o*n*u*2/1e9
A = np.empty((u,m,n,o), order='f', dtype=np.float32)
B = np.empty((a,c,b,u), order='f', dtype=np.float32)
C = np.empty((m,o,b,a,n,c), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,m,n,o", B, "a,c,b,u", beta, C, "m,o,b,a,n,c" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("umno,acbu->mobanc", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC