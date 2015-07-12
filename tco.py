"""
Allow to use tail-call optimized functions in Python code (for tail-recursion or continuation-passing style).
"""

class _TailCallWrapper():
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
        while callable(f):
            f = f()
        return f

class C():
    """
    Main wrapper for tail-call optimized functions.
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *k):
        return _TailCallWrapper(self.func, k)

try:
    apply(len,((),))
    # Python 2
    class _TailCallWrapper1():
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
            while type(f)==tuple and len(f)==2 and callable(f[0]):
                f = apply(*f)
            return f
    
    class C1():
        """
        Main wrapper for tail-call optimized functions.
        """
        def __init__(self, func):
            self.func = func
        def __call__(self, *k):
            return _TailCallWrapper1(self.func, k)
except:
    # Python 3
    class _TailCallWrapper1():
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
            while type(f)==tuple and len(f)==2 and callable(f[0]):
                g,h = f
                f = g(*h)
            return f
    
    class C1():
        """
        Main wrapper for tail-call optimized functions.
        """
        def __init__(self, func):
            self.func = func
        def __call__(self, *k):
            return _TailCallWrapper1(self.func, k)

class _TailCall(Exception):
    def __init__(self, f, args):
        self.func = f.func
        self.args = args

def _tailCallback(f):
    def t(*args):
        raise _TailCall(f,args)
    return t

class _TailCallWrapper2():
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
        
class C2():
    """
    Main wrapper for tail-call optimized functions.
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *k):
        return _TailCallWrapper2(self.func, k)
