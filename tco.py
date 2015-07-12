"""
Allow to use tail-call optimized functions in Python code (for tail-recursion or continuation-passing style).
"""

class _TailCall(Exception):
    def __init__(self, f, args):
        self.func = f.func
        self.args = args

def _tailCallback(f):
    def t(*args):
        raise _TailCall(f,args)
    return t

class _TailCallWrapper():
    """
    Wrapper for tail-called optimized functions embedding their continuations.
    Such functions are ready to be evaluated with their arguments.

    This is a private class and should never be accessed directly.
    Functions should be created by using the C() class first.
    """
    def __init__(self,func, k):
        self.func = func( _tailCallback(self),
                          *map( lambda c: _tailCallback(c) , k) )
    def __call__(self, *args):
        f = self.func
        while True:
            try:
                return f(*args)
            except _TailCall as e:
                f = e.func
                args = e.args
        
class C():
    """
    Main wrapper for tail-call optimized functions.

    Usage:
        f = C(
               lambda self [,k1, k2, ...]:
                 lambda *args:
             )
       where 'self' is intended for a recursive call
       and k1, k2, etc. are other contiuations also defined with C()

       Invoking 'f' is done as:
         f( [k1, k2, ...] )(*args)
       where the 'self' continuation is implicit.

    Examples:
      # Factorial function
      fac = C(
               lambda self:
                 lambda n, acc:
                   self(n-1,n*acc) if n>1 else acc
              )()
      print( fac(5,1) )
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *k):
        return _TailCallWrapper(self.func, k)




# tests
# import traceback
# def display1(x,y):
#   print(("ok",len(traceback.extract_stack()),(x,y)))
# def display2(x,y):
#   print(("err",len(traceback.extract_stack()),(x,y)))
# 
# disp1 = C(lambda f: lambda x,y: display1(x,y))()
# disp2 = C(lambda f: lambda x,y: display2(x,y))()
# 
# Y = lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))
# test = ( lambda f, k1, k2: lambda n:
#            Y(lambda f: lambda i,j: f(i-1,not j) if i>0
#                 else k1(42,0) if j else k2(42,0))(n,False) )
# 
# C(test)(disp1,disp2)(150)
