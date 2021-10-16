"""
This script contains routines for computation in Eulidean geometry.
"""

import numpy as np


# estimates a circle with evenly space points sampled on it
# num number of samples
# with from_to we can set at what angle it starts and what angle it ends
# 0, 360 for full circle
def circle_approx_pts(centre, radius, num, from_to=[0,360]):
    centre = np.array(centre)
    if from_to[1] < from_to[0]:
        myrange = range(from_to[1], from_to[0]+360, (from_to[0]+360-from_to[1])//num)
    else:
        myrange = range(from_to[0], from_to[1], (from_to[1]-from_to[0])//num)

    return_pts = []
    for angle in myrange:
        return_pts.append(centre+radius*np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle))]))

    return return_pts


# A, B, C are pairs of coordinates
# the function computes the centre of the circumscribed circle
def circumcentre(A,B,C):
    D = 2 * (A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1]))
    K_x_A = (A[0]*A[0] + A[1]*A[1]) * (B[1]-C[1])
    K_x_B = (B[0]*B[0] + B[1]*B[1]) * (C[1]-A[1])
    K_x_C = (C[0]*C[0] + C[1]*C[1]) * (A[1]-B[1])
    K_x = (K_x_A + K_x_B + K_x_C) / D

    K_y_A = (A[0]*A[0] + A[1]*A[1]) * (C[0]-B[0])
    K_y_B = (B[0]*B[0] + B[1]*B[1]) * (A[0]-C[0])
    K_y_C = (C[0]*C[0] + C[1]*C[1]) * (B[0]-A[0])
    K_y = (K_y_A + K_y_B + K_y_C) / D

    return K_x, K_y


# A and centre are pairs of coordiantes
# the function computes the radius of the circumscribed circle given a vertex
# of the triangle and the computed centre of the circle
def circumradius(A, centre):
    return np.linalg.norm(np.array(A)-np.array(centre))


# A, B, C are pairs of coordinates
# combines circumcentre(A,B,C) and circumradius(A, centre) to compute both
# the centre and the radius
def circum_centre_and_radius(A,B,C):
    centre = circumcentre(A,B,C)
    radius = circumradius(A,centre)
    return centre, radius


# A, B, C are pairs of coordinates
# the function computes the centre of the inscribed circle
def incentre(A,B,C):
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    a = np.linalg.norm(C-B)
    b = np.linalg.norm(A-C)
    c = np.linalg.norm(B-A)

    I_x = (a*A[0]+b*B[0]+c*C[0]) / (a+b+c)
    I_y = (a*A[1]+b*B[1]+c*C[1]) / (a+b+c)
    return I_x, I_y


# A, B, C are pairs of coordinates
# the function computes the radius of the circumscribed circle given the
# three vertices of the triangle
def inradius(A,B,C):
    a = np.linalg.norm(np.array(B)-np.array(C))
    b = np.linalg.norm(np.array(C)-np.array(A))
    c = np.linalg.norm(np.array(A)-np.array(B))
    s = (a+b+c)/2
    return np.sqrt(s*(s-a)*(s-b)*(s-c)) / s


# A, B, C are pairs of coordinates
# combines circumcentre(A,B,C) and circumradius(A, centre) to compute both
# the centre and the radius
def in_centre_and_radius(A,B,C):
    centre = incentre(A,B,C)
    radius = inradius(A,B,C)
    return centre, radius


# A, B are pairs of coordinates of the endpoints of a segment
# P, Q are pairs of coordinates of the endpoints of a segment
# computes the coordinates of the intersection of segment AB and segment PQ,
# beware: when the segments are parallel the denominators are 0
def ll_intersection(A,B,P,Q):
    denominator = (A[0]-B[0]) * (P[1]-Q[1]) - (A[1]-B[1]) * (P[0]-Q[0])
    if denominator == 0:
        return (DEFAULT,DEFAULT)
    numerator_x = (A[0]*B[1]-B[0]*A[1]) * (P[0]-Q[0]) - (A[0]-B[0]) * (P[0]*Q[1]-Q[0]*P[1])
    numerator_y = (A[0]*B[1]-B[0]*A[1]) * (P[1]-Q[1]) - (A[1]-B[1]) * (P[0]*Q[1]-Q[0]*P[1])

    return numerator_x/denominator, numerator_y/denominator


# credit: https://stackoverflow.com/questions/55816902/finding-the-intersection-of-two-circles
# O0, r0 are to centre and radius of circle 1
# O1, r1 are to centre and radius of circle 2
# computes the intersection points of two circles
# note that there can be two intersection points, or one, or none.
def cc_intersection(O0, r0, O1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    x0, y0 = O0
    x1, y1 = O1

    d=np.sqrt((x1-x0)**2 + (y1-y0)**2)

    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=np.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d
        y2=y0+a*(y1-y0)/d
        x3=x2+h*(y1-y0)/d
        y3=y2-h*(x1-x0)/d

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d

        return (x3, y3, x4, y4)


# O, r are the centre and radius of a circle
# A, B are pair of coordinates representing the endpoints of a segment
# computes the intersection points of the circle (O,r) and segment AB
# warning: the number of intersection points may be 0, 1, or 2.
def lc_intersection(O, r, A, B):
    sign = lambda x : 1 if x >= 0 else -1
    O_ = np.array(O)
    A_ = np.array(A)
    B_ = np.array(B)
    dx, dy = B_ - A_
    dr = np.sqrt(dx*dx + dy*dy)
    D = np.cross(A_-O_, B_-O_)
    discriminant = r*r*dr*dr-D*D

    if discriminant > 0:
        x1 = (D*dy+sign(dy)*dx*np.sqrt(discriminant)) / (dr*dr) + O_[0]
        y1 = (-D*dx+np.abs(dy)*np.sqrt(discriminant)) / (dr*dr) + O_[1]
        x2 = (D*dy-sign(dy)*dx*np.sqrt(discriminant)) / (dr*dr) + O_[0]
        y2 = (-D*dx-np.abs(dy)*np.sqrt(discriminant)) / (dr*dr) + O_[1]
        if np.cross(A_-O_,A_-B_) <= 0:
            if sign(dy) == 1:
                return [[x1,y1], [x2,y2]], True
            else:
                return [[x2,y2], [x1,y1]], True
        else:
            if sign(dy) == 1:
                return [[x1,y1], [x2,y2]], False
            else:
                return [[x2,y2], [x1,y1]], False
    elif discriminant == 0:
        x = D*dy / (dr*dr)
        y = -D*dx / (dr*dr)
        return [[x,y], [x,y]], False
    else:
        return [[0,0],[0,0]], False


# credit
# https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
# A, B a pair of coordinates representing the endpoints of a segment
# P is a point
# computes the distance of point P from segment AB
def pt_segment_dist(A, B, P):
    x1, y1 = A
    x2, y2 = B
    x3, y3 = P
    px = x2-x1
    py = y2-y1
    norm = px*px + py*py
    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py
    dx = x - x3
    dy = y - y3

    dist = (dx*dx + dy*dy)**.5
    return dist


# O, r are the centre and radius of a circle
# P is a point
# computes the distance between the circle (O,r) and the point P
def pt_circle_dist(O, r, P):
    return abs(np.linalg.norm(np.array(O)-np.array(P))-r)


# A, B are the endpoints of a segment
# P is a point
# computes the orthogonal projection of P on AB
def orthogonal_projection(A, B, P):
    A_ = np.array(A)
    B_ = np.array(B)
    P_ = np.array(P)
    x = np.linalg.norm(P_ - A_) * (P_ - A_).dot(B_ - A_) / (np.linalg.norm(P_ - A_) * np.linalg.norm(B_ - A_))
    return A_ + (B_- A_) / np.linalg.norm(A_ - B_) * x


# In order to get the exact distance from the angle point we follow the
# construction method of tkz-euclide.
# 1. copy the first segment (A,B) on the second segment (B,C) to get (P)
# the result is the third coordinate of the equilateral triangle formed by AP.

# A, B, C are point forming an angle, B being in the middle
# computes a point which lies on the bisector of the angle
def bisector_point(A,B,C):
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    P = B + np.linalg.norm(B-A) * (C - B) / np.linalg.norm(C-B)
    rotation_matrix = np.array([[np.cos(np.radians(60)), -np.sin(np.radians(60))],\
                               [np.sin(np.radians(60)), np.cos(np.radians(60))]])
    Q = A.reshape(2,1) + rotation_matrix @ (P-A).reshape(2,1)
    return Q.flatten()
