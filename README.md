# tco

## Tail Call Optimization for Python (version 1.2.1)

*A module for performing tail-call optimization in Python code.*

The module allows a coder to write tail-recursive functions as well as using continuation-passing style in his/her code without having the size of the execution stack increasing.

The module internally uses standard and pythonic features (mostly lambda calculus and exceptions) and doesn't attempt to "inspect" the stack or the functions for modifying them. For this reason, it should integrate smoothly with any version of Python. Furthermore, nested systems of continuations are correctly handled.

I wrote a similar module handling called [continuation](https://github.com/baruchel/continuation).

### Installation

Just type:

    pip install tco

or (for a system-wide installation):

    sudo pip install tco

Since the module is rather small, the single file `__init__.py` can also be quickly renamed as `tco.py` and directly put in the directory of a given project for _ad hoc_ purposes.

### Low-level class and high-level decorator

The whole module relies on a new low-level class called `C`. Since embedding new functions in this wrapper may seem difficult to some users, a decorator has been added in the module since its version 1.2 in order to provide a convenient style of programming.

Both can be imported with:

    from tco import *

### Using the @with_continuations decorator

The module provides a decorator `@with_continuations` taking arguments for defining new tail-optimized functions. Below is an example for the _factorial_ function:

    @with_continuations()
    def factorial(n, k, self=None):
        return self(n-1, k*n) if n > 1 else k

The new `factorial` function can be used with something like `factorial(10,1)` for computing _factorial(10)_. Here the decorator has no argument because no external continuation is used; the tail-recursive call is implicit and always provided. The `self` keyword is mandatory for all decorated functions; it can be used in the body of the function for a tail-recursive call.

Other continuations can also be used:

    @with_continuations()
    def identity(x, self=None):
        return x
    
    @with_continuations(out=identity)
    def factorial2(n, k, self=None, out=None):
        return self(n-1, k*n) if n > 1 else out(k)

The `factorial2` function escapes form the recursive process (which however is no longer a stack) by using a continuation (in the example above, the continuation does nothing special).

More interesting continuations for success or failure cases can be defined by the user for escaping from the most inner call of a tail-recursive process.

The default value of all continuations (including the `self` one) may be any value of any kind, since it is not used (the decorator wraps the function and ensures it will be called with relevant internal values). Several style guidelines can be given:

  * using `None` as a default value for all continuations;
  * using `C` as a default value for all continuations in order to let a reader remember this keyword arguments are continuations;
  * using `None` or `C` for the `self` keyword argument and copying the name of the corresponding continuation for all other arguments.

Here are some examples for the previous style guidelines:

    @with_continuations(k1=success_func, k2=failure_func)
    def myfunc(a, b, c, self=None, k1=None, k2=None):
        pass

    @with_continuations(k1=success_func, k2=failure_func)
    def myfunc(a, b, c, self=C, k1=C, k2=C):
        pass

    @with_continuations(k1=success_func, k2=failure_func)
    def myfunc(a, b, c, self=None, k1=success_func, k2=failure_func):
        pass

    @with_continuations(k1=success_func, k2=failure_func)
    def myfunc(a, b, c, self=C, k1=success_func, k2=failure_func):
        pass

### Low-level class provided by the module

A long explanation of how to use the low-level class was written on a blog in 2015; it can be found [here](http://baruchel.github.io/python/2015/11/07/explaining-functional-aspects-in-python/). Old explanation for this class is below.

The module implements a trampoline-based wrapper for tail-call optimized functions. It should be imported with:

    from tco import C

The syntax for using the wrapper is:

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

### Dynamically creating new continuations

In version 1.2.1 was introduced an attribute allowing to get the original function passed as a continuation in order to dynamically build a new continuation with the very same function. In the example below, this attribute appears as `k.C`:

    from tco import C
    
    identity = C(lambda self: lambda x: x)()
    test = lambda self, k: lambda x: C(test2)(k.C)(x)
    test2 = lambda self, k: lambda x: k(x+1)
    
    print( C(test)(identity)(5) )
    
