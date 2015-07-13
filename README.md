# tco

## Tail Call Optimization for Python

*A module for performing tail-call optimization in Python code. Compatible with Python 2 and Python 3 as well as with both versions of the Pypy interpreter. A fast version to be compiled with Cython is also provided (with some pre-compiled binaries).*

The module allows a coder to write tail-recursive functions as well as using continuation-passing style in his/her code without having the size of the execution stack increasing.

### New class provided by the module

The module contains various different implementations of a trampoline-based wrapper for tail-call optimized functions. Only one should be imported according to the needs; the following `import` statements will allow to use the very same syntax in the code to be written:

    from tco import C
    from tco import C1 as C
    from tco import C2 as C
    from tco import C3 as C

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

### Using the Cython version

Speed can get improved by using the version compiled by Cython. Some binaries are provided in the current Github repository (in which case installing cython isn't required) but installing Cython and compiling the module is very easy (see the instructions in the relevant directory).

In order to try a pre-compiled binary, the library file `c_tco.so` can be put in the same directory than the python code and nothing more is required before importing the module.
