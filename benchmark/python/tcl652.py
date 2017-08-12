import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 24
b = 25
m = 24
o = 25
n = 25
u = 25
v = 24
gflops = a*b*m*o*n*u*v*2/1e9
A = np.empty((v,b,a,u), order='f', dtype=np.float32)
B = np.empty((m,o,u,v,n), order='f', dtype=np.float32)
C = np.empty((a,o,n,m,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,b,a,u", B, "m,o,u,v,n", beta, C, "a,o,n,m,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vbau,mouvn->aonmb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC