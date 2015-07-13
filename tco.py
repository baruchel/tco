"""
Allow to use tail-call optimized functions in Python code (for tail-recursion or continuation-passing style).
"""

__version__ = '1.0.0 alpha'

try:
    apply(len,((),)) # test the version of Python
    # Python 2
    class _TailCallWrapper():
        """
        Wrapper for tail-called optimized functions embedding their continuations.
        Such functions are ready to be evaluated with their arguments.
    
        This is a private class and should never be accessed directly.
        Functions should be created by using the C() class first.
        """
        def __init__(self,func, k):
            self.func = func(
              lambda *args: (self.func, args),
              *map( lambda c: lambda *args: (c.func, args), k) )
        def __call__(self, *args):
            f = (self.func, args)
            while True:
                try:
                    f = apply(*f)
                except TypeError:
                    return f
except:
    # Python 3
    class _TailCallWrapper():
        """
        Wrapper for tail-called optimized functions embedding their continuations.
        Such functions are ready to be evaluated with their arguments.
    
        This is a private class and should never be accessed directly.
        Functions should be created by using the C() class first.
        """
        def __init__(self,func, k):
            self.func = func(
              lambda *args: (self.func, args),
              *map( lambda c: lambda *args: (c.func, args), k) )
        def __call__(self, *args):
            f = (self.func, args)
           #while type(f)==tuple and len(f)==2 and callable(f[0]):
           #    g,h = f
           #    f = g(*h)
            while True:
                try:
                    g,h = f
                    f = g(*h)
                except TypeError:
                    return f
class C():
    """
    Main wrapper for tail-call optimized functions.
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *k):
        return _TailCallWrapper(self.func, k)

class _TailCallWrapper1():
    """
    Wrapper for tail-called optimized functions embedding their continuations.
    Such functions are ready to be evaluated with their arguments.

    This is a private class and should never be accessed directly.
    Functions should be created by using the C() class first.
    """
    def __init__(self,func, k):
        self.func = func(
          lambda *args: lambda: self.func(*args),
          *map( lambda c: lambda *args: lambda: c.func(*args), k) )
    def __call__(self, *args):
        f = lambda: self.func(*args)
        while True:
          try:
            f = f()
          except TypeError:
            return f

class C1():
    """
    Main wrapper for tail-call optimized functions.
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *k):
        return _TailCallWrapper1(self.func, k)

class _TailCall2(Exception):
    def __init__(self, f, args):
        self.func = f.func
        self.args = args

def _tailCallback2(f):
    def t(*args):
        raise _TailCall2(f,args)
    return t

class _TailCallWrapper2():
    """
    Wrapper for tail-called optimized functions embedding their continuations.
    Such functions are ready to be evaluated with their arguments.

    This is a private class and should never be accessed directly.
    Functions should be created by using the C() class first.
    """
    def __init__(self,func, k):
        self.func = func( _tailCallback2(self),
                          *map( lambda c: _tailCallback2(c) , k) )
    def __call__(self, *args):
        f = self.func
        while True:
            try:
                return f(*args)
            except _TailCall2 as e:
                f = e.func
                args = e.args
        
class C2():
    """
    Main wrapper for tail-call optimized functions.
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *k):
        return _TailCallWrapper2(self.func, k)

# plus rapide en Python 2:
class _TailCall3(Exception):
    def __init__(self):
        pass

def _tailCallback3(f,e):
    def t(*args):
        e.func = f.func
        e.args = args
        raise e
    return t

class _TailCallWrapper3():
    """
    Wrapper for tail-called optimized functions embedding their continuations.
    Such functions are ready to be evaluated with their arguments.

    This is a private class and should never be accessed directly.
    Functions should be created by using the C() class first.
    """
    def __init__(self,func, k):
        e = _TailCall3()
        self.func = func( _tailCallback3(self, e),
                          *map( lambda c: _tailCallback3(c, e) , k) )
    def __call__(self, *args):
        f = self.func
        while True:
            try:
                return f(*args)
            except _TailCall3 as e:
                f = e.func
                args = e.args
        
class C3():
    """
    Main wrapper for tail-call optimized functions.
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *k):
        return _TailCallWrapper3(self.func, k)
