from tco import C1 as C
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

t = C( lambda f, k1, k2: lambda n:
           C(lambda f: lambda i,j: f(i-1,not j) if i>0
                else k1(42,0) if j else k2(42,0))()(n,True) )

t(disp1,disp2)(1000)

f = C(
       lambda self, d:
         lambda n:
           self(n-1) if n>0 else d(42)
      )(disp)
t = time.time(); f(100000); print(time.time()-t)
    
