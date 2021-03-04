import inspect

def positional_arity(func):
    args, varargs = inspect.getfullargspec(func)
def curry_internal(func, arity, passed_args=None):
    if passed_args is None:
        passed_args = []

    def curried_function(x):
        if len(passed_args) + 1 < arity:
            return curry_internal(func, arity, [*passed_args, x])
        else:
            return func(*passed_args, x)

    return curried_function


def curry_explicit(func, arity):
    if arity == 0:
        return func
    else:
        return curry_internal(func, arity)


def uncurry_explicit(func, arity):
    def uncurried_function(*args):
        if len(args) != arity:
            raise Exception("dam")
        curried_result = func
        for arg in args:
            curried_result = curried_result(arg)
        return curried_result

    return uncurried_function


def f(x, y):
    return x + y


g = curry_explicit(f, 2)

print(g(1))
print(g(2))
print(g(1)(2))

h = uncurry_explicit(g, 2)

print(h(9, 11))

p = curry_explicit(print, 2)
p(1)(10)

def f():
    print("unary function")


ff = curry_explicit(f, 0)
ff()