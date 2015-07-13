# tco

## Tail Call Optimization for Python

*A module for performing tail-call optimization in Python code. Compatible with Python 2 and Python 3 as well as with both versions of the Pypy interpreter.*

The module allows a coder to write tail-recursive functions as well as using continuation-passing style in his/her code without having the size of the execution stack increasing.

The module contains various different implementations of a trampoline-based wrapper for tail-call optimized functions. Only one should be imported according to the needs; the following `import` statements will allow to use the very same syntax in the code to be written:

    from tcp import C
    from tco import C1 as C
    from tco import C2 as C

The main difference between all wrappers is speed and the first wrapper should be tried first. The wrappers `C` and `C1` should avoid returning callable objects as their final return value; the wrapper `C2` is slower but it is compatible with any return value.

The syntax for using all wrappers is:

    f = C(
           lambda self, k1, k2, k3, ...:
             lambda *args:
               ... code here ...
          )

where the argument `self` will be used for referring to the function itself (recursion case) and any number (including none) of other continuations `k1`, `k2`, etc. can be used as well.

Using the function is done as:

    f( k1, k2, k3, ...) ( *args )

where the self reference is implicit (only other continuations have to be provided). Functions used as continuations should of course be created with the `C` wrapper also.

A tail-recursive version of the factorial function (using an accumulator) is:

    fac = C(
             lambda self:
               lambda n, acc:
                 self(n-1,n*acc) if n>1 else acc
            )()
    print( fac(5,1) )

The file `test.py` gives some other examples.
