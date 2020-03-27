from numpy import hstack, inf, ndarray, ones
from osqp import OSQP
from scipy.sparse import csc_matrix, vstack
from warnings import warn


def conversion_warning(M):
    return "Converted %s to scipy.sparse.csc.csc_matrix\n" \
           "For best performance, build %s as a csc_matrix " \
           "rather than as a numpy.ndarray" % (M, M)


def solve(P, q, G=None, h=None, A=None, b=None, initvals=None):
    """
    Solve a Quadratic Program defined as:
        minimize
            (1/2) * x.T * P * x + q.T * x
        subject to
            G * x <= h
            A * x == b
    using OSQP <https://github.com/oxfordcontrol/osqp>.
    Parameters
    ----------
    P : scipy.sparse.csc_matrix
        Symmetric quadratic-cost matrix.
    q : numpy.array
        Quadratic cost vector.
    G : scipy.sparse.csc_matrix
        Linear inequality constraint matrix.
    h : numpy.array
        Linear inequality constraint vector.
    A : scipy.sparse.csc_matrix, optional
        Linear equality constraint matrix.
    b : numpy.array, optional
        Linear equality constraint vector.
    initvals : numpy.array, optional
        Warm-start guess vector.
    Returns
    -------
    x : array, shape=(n,)
        Solution to the QP, if found, otherwise ``None``.
    Note
    ----
    OSQP requires `P` to be symmetric, and won't check for errors otherwise.
    Check out for this point if you e.g. `get nan values
    <https://github.com/oxfordcontrol/osqp/issues/10>`_ in your solutions.
    """
    P = csc_matrix(P)
    if type(P) is ndarray:
        warn(conversion_warning("P"))
        P = csc_matrix(P)
    osqp = OSQP()
    if A is None and G is None:
        osqp.setup(P=P, q=q, verbose=False)
    elif A is not None:
        if type(A) is ndarray:
            warn(conversion_warning("A"))
            A = csc_matrix(A)
        if G is None:
            osqp.setup(P=P, q=q, A=A, l=b, u=b, verbose=False)
        else:  # G is not None
            l = -inf * ones(len(h))
            qp_A = vstack([G, A]).tocsc()
            qp_l = hstack([l, b])
            qp_u = hstack([h, b])
            osqp.setup(P=P, q=q, A=qp_A, l=qp_l, u=qp_u, verbose=False)
    else:  # A is None
        if type(G) is ndarray:
            warn(conversion_warning("G"))
            G = csc_matrix(G)
        l = -inf * ones(len(h))
        osqp.setup(P=P, q=q, A=G, l=l, u=h, verbose=False)
    if initvals is not None:
        osqp.warm_start(x=initvals)
    res = osqp.solve()
    if res.info.status_val != osqp.constant('OSQP_SOLVED'):
        print("OSQP exited with status '%s'" % res.info.status)
    return res.x
