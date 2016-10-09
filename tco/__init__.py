"""
Allow to use tail-call optimized functions in Python code (for
tail-recursion or continuation-passing style).
"""

__version__ = '1.2.1'

class _TailCall(Exception):
    def __init__(self, f, args, uid):
        self.func, self.args, self.uid, self.follow = f.func, args, uid, id(f)

def _tailCallback(f, uid):
    """
    This is the "callable" version of the continuation, which sould only
    be accessible from the inside of the function to be continued. An
    attribute called "C" can be used in order to get back the public
    version of the continuation (for passing the continuation to another
    function).
    """
    def t(*args):
        raise _TailCall(f, args, uid)
    t.C = f
    return t

class _TailCallWrapper():
    """
    Wrapper for tail-called optimized functions embedding their
    continuations. Such functions are ready to be evaluated with
    their arguments.

    This is a private class and should never be accessed directly.
    Functions should be created by using the C() class first.
    """
    def __init__(self, func, k):
        self.func = func( _tailCallback(self, id(self)),
                          *map( lambda c: _tailCallback(c, id(self)), k) )
    def __call__(self, *args):
        f, expect = self.func, id(self)
        while True:
            try:
                return f(*args)
            except _TailCall as e:
                if e.uid == expect:
                    f, args, expect = e.func, e.args, e.follow
                else:
                    raise e

class C():
    """
    Main wrapper for tail-call optimized functions.
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *k):
        return _TailCallWrapper(self.func, k)

def with_continuations(**c):
    """
    A decorator for defining tail-call optimized functions.

    Example
    -------

        @with_continuations()
        def factorial(n, k, self=None):
            return self(n-1, k*n) if n > 1 else k
        
        @with_continuations()
        def identity(x, self=None):
            return x
        
        @with_continuations(out=identity)
        def factorial2(n, k, self=None, out=None):
            return self(n-1, k*n) if n > 1 else out(k)

        print(factorial(7,1))
        print(factorial2(7,1))

    """
    if len(c): keys, k = zip(*c.items())
    else: keys, k = tuple([]), tuple([])
    def d(f):
        return C(
            lambda kself, *conts:
                lambda *args:
                    f(*args, self=kself, **dict(zip(keys, conts)))) (*k)
    return d
