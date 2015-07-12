from tco import C, C1, C2
import traceback
import time

# tests
def display(x):
  print((len(traceback.extract_stack()),x))
def display1(x,y):
  print(("ok",len(traceback.extract_stack()),(x,y)))
def display2(x,y):
  print(("err",len(traceback.extract_stack()),(x,y)))

disp  = C(lambda f: lambda x: display(x))()
disp1 = C(lambda f: lambda x,y: display1(x,y))()
disp2 = C(lambda f: lambda x,y: display2(x,y))()

print("Stress test")
t = C( lambda f, k1, k2: lambda n:
           C(lambda f: lambda i,j: f(i-1,not j) if i>0
                else k1(42,0) if j else k2(42,0))()(n,True) )

t(disp1,disp2)(1000)
t(disp1,disp2)(1001)

print("Comparison of speed between C, C1 and C2")
f = lambda self, d: lambda n: self(n-1) if n>0 else d(42)
t = time.time(); C(f)(disp)(100000); print("C",time.time()-t)
t = time.time(); C1(f)(disp)(100000); print("C1",time.time()-t)
t = time.time(); C2(f)(disp)(100000); print("C2",time.time()-t)

print("Comparison between built-in recursion and tco")
def recurs(n):
  return recurs(n-1) if n>0 else 0
f = lambda self: lambda n: f(n-1) if n>0 else 0
t = time.time(); recurs(500); print("built-in",time.time()-t)
t = time.time(); C(f)()(500); print("tco C",time.time()-t)
t = time.time(); C1(f)()(500); print("tco C1",time.time()-t)

