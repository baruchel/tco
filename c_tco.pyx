"""
Allow to use tail-call optimized functions in Python code (for tail-recursion or continuation-passing style).
"""

__version__ = '1.0.0 alpha'

cdef class _TailCallWrapper:
    """
    Wrapper for tail-called optimized functions embedding their continuations.
    Such functions are ready to be evaluated with their arguments.

    This is a private class and should never be accessed directly.
    Functions should be created by using the C() class first.
    """
    cdef object func
    cdef object trampoline
    def __init__(self,func, k):
        self.func = func(
          lambda *args: (self.func, args),
          *map( lambda c: lambda *args: (c.func, args), k) )
    cdef _start(self):
        #cdef object g,h
        while True:
            #g, h = self.trampoline
            #self.trampoline = g(*h)

            #g = self.trampoline[0]
            #h = self.trampoline[1]
            #self.trampoline = g(*h)

            self.trampoline = self.trampoline[0](*self.trampoline[1])

            #self.trampoline = apply(*self.trampoline)
    def __call__(self, *args):
        self.trampoline = (self.func, args)
        try:
            self._start()
        except TypeError:
            return self.trampoline
class C():
    """
    Main wrapper for tail-call optimized functions.
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *k):
        return _TailCallWrapper(self.func, k)

cdef class _TailCallWrapper1:
    """
    Wrapper for tail-called optimized functions embedding their continuations.
    Such functions are ready to be evaluated with their arguments.

    This is a private class and should never be accessed directly.
    Functions should be created by using the C() class first.
    """
    cdef object func
    cdef object trampoline
    def __init__(self, func, k):
        self.func = func(
          lambda *args: lambda: self.func(*args),
          *map( lambda c: lambda *args: lambda: c.func(*args), k) )
    cdef _start(self):
        while True:
            self.trampoline = self.trampoline()
    def __call__(self, *args):
        self.trampoline = lambda: self.func(*args)
        try:
            self._start()
        except TypeError:
            return self.trampoline

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

# Same idea as previously but much quicker on Python2 (and slower on Python3)
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
