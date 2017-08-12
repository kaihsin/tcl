import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 40
b = 45
m = 12
o = 12
n = 12
u = 12
w = 16
v = 16
gflops = a*b*m*o*n*u*w*v*2/1e9
A = np.empty((v,u,a,b,w), order='f', dtype=np.float32)
B = np.empty((w,n,m,v,o,u), order='f', dtype=np.float32)
C = np.empty((a,m,o,n,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,u,a,b,w", B, "w,n,m,v,o,u", beta, C, "a,m,o,n,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vuabw,wnmvou->amonb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC