"""
Allow to use tail-call optimized functions in Python code (for
tail-recursion or continuation-passing style).
"""

__version__ = '1.1'

class _TailCall(Exception):
    def __init__(self, f, args, uid):
        self.func, self.args, self.uid, self.follow = f.func, args, uid, id(f)

def _tailCallback(f, uid):
    def t(*args):
        raise _TailCall(f, args, uid)
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

# TODO: see if there is any interest in trying to adapt the following
#       system (from the 1.0.1 version) to the new way (maybe it could
#       be a little quicker for Python 2).
#
# Same idea as previously but much quicker on Python2 (and slower on Python3)
# class _TailCall3(Exception):
#     def __init__(self):
#         pass
# 
# def _tailCallback3(f, e):
#     def t(*args):
#         e.func = f.func
#         e.args = args
#         raise e
#     return t
# 
# class _TailCallWrapper3():
#     """
#     Wrapper for tail-called optimized functions embedding their continuations.
#     Such functions are ready to be evaluated with their arguments.
# 
#     This is a private class and should never be accessed directly.
#     Functions should be created by using the C() class first.
#     """
#     def __init__(self, func, k):
#         e = _TailCall3()
#         self.func = func( _tailCallback3(self, e),
#                           *map( lambda c: _tailCallback3(c, e), k) )
#     def __call__(self, *args):
#         f = self.func
#         while True:
#             try:
#                 return f(*args)
#             except _TailCall3 as e:
#                 f = e.func
#                 args = e.args
#         
# class C3():
#     """
#     Main wrapper for tail-call optimized functions.
#     """
#     def __init__(self, func):
#         self.func = func
#     def __call__(self, *k):
#         return _TailCallWrapper3(self.func, k)
