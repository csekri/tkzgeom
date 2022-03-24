import math


def dot(X, Y):
    """Dot product two vectors."""
    return X[0]*Y[0] + X[1]*Y[1]


def sub(X, Y):
    """From the difference of two vectors."""
    return X[0]-Y[0], X[1]-Y[1]


def add(X, Y):
    """Add two vectors."""
    return X[0]+Y[0], X[1]+Y[1]


def norm_sqr(X):
    """Compute the square of the norm."""
    return dot(X, X)


def norm(X):
    """Compute the norm."""
    return norm_sqr(X) ** 0.5


def dist_sqr(X, Y):
    """Compute the square of the distance between two vectors."""
    return norm_sqr(sub(X, Y))


def dist(X, Y):
    """Compute the distance between two vectors."""
    return dist_sqr(X, Y) ** 0.5


def scalar_mul(c, X):
    """Multiply vector by scalar."""
    return [c*X[0], c*X[1]]


def ortho_proj(A, B, P):
    """Compute orthogonal projection of point onto a line """
    x = dot(sub(P, A), sub(B, A)) / dist_sqr(B, A)
    return A[0] + (B[0] - A[0]) * x, A[1] + (B[1] - A[1]) * x


def ll_intersection(A, B, P, Q):
    """Compute intersection of two segments formed by four points."""
    denominator = (A[0]-B[0]) * (P[1]-Q[1]) - (A[1]-B[1]) * (P[0]-Q[0])
    if denominator == 0:
        return 0.0, 0.0
    numerator_x = (A[0]*B[1]-B[0]*A[1]) * (P[0]-Q[0]) - (A[0]-B[0]) * (P[0]*Q[1]-Q[0]*P[1])
    numerator_y = (A[0]*B[1]-B[0]*A[1]) * (P[1]-Q[1]) - (A[1]-B[1]) * (P[0]*Q[1]-Q[0]*P[1])

    return numerator_x/denominator, numerator_y/denominator


def translation(A, B, P):
    """Translate point by vector."""
    return add(sub(B, A), P)


def point_segment_dist_sqr(A, B, P):
    """Compute distance square of a point to a segment."""
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
    """Compute the square of the distance from a point to a circle."""
    return abs(norm(sub(O, P)) - r) ** 2


def circumradius(A, centre):
    """Compute the radius of the circumscribed circle."""
    return norm(sub(A, centre))


def circumcentre(A, B, C):
    """Compute the centre of the circumscribed circle."""
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


def bisector_point(A, B, C):
    """Compute a point on the bisector. """
    scalar = dist(B, A) / dist(C, B)
    P = add(B, scalar_mul(scalar, sub(C, B)))
    cossixty, sinsixty = math.cos(math.radians(60)), math.sin(math.radians(60))
    rot = (P[0]-A[0])*cossixty - (P[1]-A[1])*sinsixty, (P[0]-A[0])*sinsixty + (P[1]-A[1])*cossixty
    Q = add(A, rot)
    return Q