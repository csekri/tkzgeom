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
        return 0.0, 0.0
    numerator_x = (A[0]*B[1]-B[0]*A[1]) * (P[0]-Q[0]) - (A[0]-B[0]) * (P[0]*Q[1]-Q[0]*P[1])
    numerator_y = (A[0]*B[1]-B[0]*A[1]) * (P[1]-Q[1]) - (A[1]-B[1]) * (P[0]*Q[1]-Q[0]*P[1])

    return numerator_x/denominator, numerator_y/denominator


def translation(A, B, P):
    return add(sub(B, A), P)


def point_segment_dist_sqr(A, B, P):
    x1, y1 = A
    x2, y2 = B
    x3, y3 = P
    if A == B:
        return dist_sqr(A, P)
    px = x2 - x1
    py = y2 - y1
    norm = px * px + py * py
    if norm == 0.0:
        return 0.0
    u = ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py
    dx = x - x3
    dy = y - y3

    dist = dx * dx + dy * dy
    return dist


def pt_circle_dist_sqr(O, r, P):
    return abs(norm(sub(O, P)) - r) ** 2


def circumradius(A, centre):
    return norm(sub(A, centre))


def circumcentre(A, B, C):
    D = 2 * (A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1]))
    if D == 0:
        return None
    K_x_A = (A[0]*A[0] + A[1]*A[1]) * (B[1]-C[1])
    K_x_B = (B[0]*B[0] + B[1]*B[1]) * (C[1]-A[1])
    K_x_C = (C[0]*C[0] + C[1]*C[1]) * (A[1]-B[1])
    K_x = (K_x_A + K_x_B + K_x_C) / D

    K_y_A = (A[0]*A[0] + A[1]*A[1]) * (C[0]-B[0])
    K_y_B = (B[0]*B[0] + B[1]*B[1]) * (A[0]-C[0])
    K_y_C = (C[0]*C[0] + C[1]*C[1]) * (B[0]-A[0])
    K_y = (K_y_A + K_y_B + K_y_C) / D

    return K_x, K_y