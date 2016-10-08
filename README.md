# tco

## Tail Call Optimization for Python

*A module for performing tail-call optimization in Python code.*

The module allows a coder to write tail-recursive functions as well as using continuation-passing style in his/her code without having the size of the execution stack increasing.

A long explanation of how to use it can be found [here](http://baruchel.github.io/python/2015/11/07/explaining-functional-aspects-in-python/). This is the preferred documentation now.

### Installation

Just type:

    pip install tco

or (for a system-wide installation):

    sudo pip install tco

### New class provided by the module

The module implements a trampoline-based wrapper for tail-call optimized functions. It should be imported with:

    from tco import C

The main difference between all wrappers is speed; the first wrapper should be tried first. The wrappers `C` and `C1` should avoid returning callable objects as their final return value; the wrappers `C2` and `C3` are slower but are compatible with any kind of return value.

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

### Working with continuations

In the example above (for the factorial function), no explicit continuation is given as an argument to the C callable object (see the empty parenthesis at the end of the definition of the `fac` function); the single continuation used was implicit (a recursive call to the function itself). Explicit continuations may also be given.

    def disp(x):
        print(x)
    display = C(lambda self: lambda a: disp(a))()
    fac = C(
             lambda self, k:
                 lambda n, acc:
                     self(n-1,n*acc) if n>1 else k(acc)
           )(display)
    fac(5,1)

It should be noticed that the continuation to be passed as an argument should itself embed its own continuations (if any); this is why the `display` function above has the empty parenthesis at the end of the line.

Any number of explicit continuations may be used (for instance one for a success case and another one for a failure case).

Here is another example with two consecutive continuations:

    def disp(x):
        print(x)
    display = C(lambda self: lambda a: disp(a))()
    square = C(lambda f, k: lambda x: k(x**2))(display)
    fac = C(
             lambda self, k:
               lambda n, acc:
                 self(n-1,n*acc) if n>1 else k(acc)
           )(square)
    fac(5,1)
