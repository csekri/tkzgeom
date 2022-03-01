import math


def dot(X, Y):
    return X[0]*Y[0] + X[1]*Y[1]


def sub(X, Y):
    return X[0]-Y[0], X[1]-Y[1]


def add(X, Y):
    return X[0]+Y[0], X[1]+Y[1]


def norm_sqr(X):
    return dot(X, X)


def norm(X):
    return norm_sqr(X) ** 0.5


def dist_sqr(X, Y):
    return norm_sqr(sub(X, Y))


def dist(X, Y):
    return dist_sqr(X, Y) ** 0.5


def ortho_proj(A, B, P):
    # x = np.linalg.norm(P_ - A_) * (P_ - A_).dot(B_ - A_) / (np.linalg.norm(P_ - A_) * np.linalg.norm(B_ - A_))
    x = dot(sub(P, A), sub(B, A)) / dist_sqr(B, A)
    return A[0] + (B[0] - A[0]) * x, A[1] + (B[1] - A[1]) * x


def ll_intersection(A, B, P, Q):
    """
    SUMMARY
        computes the coordinates of the intersection of segment AB and segment PQ,
        (beware: when the segments are parallel the denominators are 0)
    PARAMETERS
        A: coordinates of vertex A
        B: coordinates of vertex B
        P: coordinates of vertex P
        Q: coordinates of vertex Q
    RETURNS
        ([float, float], float)
    """
    denominator = (A[0]-B[0]) * (P[1]-Q[1]) - (A[1]-B[1]) * (P[0]-Q[0])
    if denominator == 0:
        return (0.0, 0.0)
    numerator_x = (A[0]*B[1]-B[0]*A[1]) * (P[0]-Q[0]) - (A[0]-B[0]) * (P[0]*Q[1]-Q[0]*P[1])
    numerator_y = (A[0]*B[1]-B[0]*A[1]) * (P[1]-Q[1]) - (A[1]-B[1]) * (P[0]*Q[1]-Q[0]*P[1])

    return numerator_x/denominator, numerator_y/denominator


def translation(A, B, P):
    return add(sub(B, A), P)