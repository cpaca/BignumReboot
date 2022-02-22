def R(a, n):
    # "Reduces" an array by "1"
    # If a is an ordinal, this is the same as a[n] - 1
    # Otherwise it's the same as a - 1

    # Allow integer inputs of a
    # In the end, this might not matter
    #########
    # GUARANTEES: a is a list
    if type(a) == int:
        return a-1

    # Note: n will always be an integer
    # This allows for infinite recursion of R(a) as long as n-1 is done
    #########
    # GUARANTEES: a is a list
    # GUARANTEES: n is nonzero
    if n < 1:
        return 0

    # This allows [] ("zero parameter" input) to be valid
    # note this is the same as "if a == []"
    #########
    # GUARANTEES: a is a non-empty list
    # GUARANTEES: n is nonzero
    if not a:
        return n

    # And this allows all inputs to eventually reach []
    # Assuming inputs eventually reach [..., 0]
    #########
    # GUARANTEES: a is a non-empty list that does not end in 0
    # GUARANTEES: n is nonzero
    if a[-1] == 0:
        return a[:-1]

    # "Simple" situations where previous indexes and recursion need not be done
    if a[0] != 0:
        a[0] = R(a[0], n)
        return a

    # OTHERWISE: Recurse! A lot!
    # Find the value to actually reduce:
    i = 0
    while a[i] == 0:
        i += 1
    # This is guaranteed to *eventually* reach a nonzero value
    # If it's given [0,0,0] then a[-1]=0 and not reach here
    # If it's given [] then a==[] then "not a = True" and won't reach here

    # Recurse this function:
    # The a[:] is done so that edits to a don't propagate up
    a[i-1] = R(a[:], n-1)

    # And finally reduce a[i]
    a[i] = R(a[i], n)
    return a


def G(a, n, m=0):

    # Without this, the m-loop is infinite.
    if a==0:
        return n+1

    # m is multiplier, but m=0 is approx. f_{V(a)}(n)
    # and m=1 is approx. f_{V(a)*2}(n)
    # More accurately, for m>0, it is *less than*:
    # f_{V(a)*(m-1) + f_(V(a))(n)}(n)
    # This, unfortunately, assumes that:
    # f_{α+β}(n) < f_{α+f_β(n)}(n)

    if m:
        prgm = ""
        b = G(a, n)
        for i in range(b):
            prgm += "\t" * i + "for _ in range(n):\n"
        prgm += "\t" * b + "n=G(R(a,n),n,m-1)"
        exec(prgm)
    # Making this an "if" instead of an "elif"
    # makes it so for m>0 it's more like f_{ f_{V(a)*(m-1) + f_(V(a))(n)}(n) }(n)

    # beyond this point the "m" variable doesn't matter
    # you can basically treat it as if m = None here
    # but it's about to get overriden anyway

    # Originally had a "if a != 0", (not equal to "if a" due to a=[])
    # but after putting a "if a==0: return n+1" at the top, that became unnecessary
    m=1
    if type(a) == list:
        # Actually, this causes it to grow faster, doesn't it.
        # MUCH. MUCH. MUCH. faster.
        m = n
    for i in range(n):
        n = G(R(a, n), n, m)
    return n+1


k = G(1, 2, 1)
print(k)
