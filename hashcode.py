# Painting Hashcode 2016

import sys
import numpy as np
from operator import itemgetter

def check_square(R,C,S,matrix, verbose=False):
    if R - S < 0:
        if verbose:  print 'R < S! Can\'t square'
        return False
    if R + S >= np.shape(matrix)[0]:
        if verbose:  print 'R + S > Size! Can\'t square'
        return False
    if C - S < 0:
        if verbose:  print 'C < S! Can\'t square'
        return False
    if C + S >= np.shape(matrix)[1]:
        if verbose:  print 'C + S > Size! Can\'t square'
        return False
    return True

def PAINT_SQUARE(R,C,S,matrix):
    matrix[R-S:R+S+1, C-S:C+S+1] = 1




def PAINT_LINE(R1,C1,R2,C2,matrix):
    matrix[R1:R2+1, C1:C2+1] = 1

def ERASE_CELL(R,C,matrix):
    if 0 <= R < np.shape(matrix)[0] and 0 <= R < np.shape(matrix)[1]:
        matrix[R,C] = 0
    else:
        print 'Bad coordinates'
        raise


def sym2ones(aList):
    return [1 if i == '#' else 0 for i in aList]

def read_image(path):
    matrix = []
    with open(path, 'r') as f:
        next(f)
        for line in f:
            matrix.append(sym2ones(list(line.rstrip())))
    f.close()
    return np.asarray(matrix)



def next_cell(m_in, m_work, R, C):
    for i in xrange(R, np.shape(m_in)[0]):
        for j in xrange(C, np.shape(m_in)[1]):
            if m_in[i,j] and not m_work[i,j]:
                return (i,j)
        C = 0
    return None


# min(square, lines, )
def algo(m_in, m_work, delta=0.22):
    R = 0
    C = 0
    all_commands = []
    while True:
        cell = next_cell(m_in, m_work, R, C)
        # print cell
        if cell == None:
            break
        sq = square(m_in, cell[0], cell[1], delta)
        hl = h_line(m_in, cell[0], cell[1])
        vl = v_line(m_in, cell[0], cell[1])


        if hl[0] >= vl[0]:
            choice = hl
        else:
            choice = vl

        if choice[0] < sq[0]:
            choice = sq

        for c in choice[1]: #parse commands
            if c[0] == 'PAINT_SQUARE':
                PAINT_SQUARE(c[1], c[2], c[3], m_work)
            elif c[0] == 'ERASE_CELL':
                ERASE_CELL(c[1], c[2], m_work)
            elif c[0] == 'PAINT_LINE':
                PAINT_LINE(c[1], c[2], c[3], c[4], m_work)
            # print m_work[c[1]-c[3]:c[1]+c[3]+1, c[2]-c[3]:c[2]+c[3]+1]
        all_commands += choice[1]

    if not (m_in==m_work).all():
        print 'ERROR! MATRICES DID NOT MATCH!'

    return m_work, all_commands

# returns (numwrittencells, [commands])
def square(m_in, R, C, delta=0.22):
    S = 0
    prev_dots = []
    while True:
        if check_square(R+S,C+S,S,m_in):
            rows = R + 2*S+1
            cols = C + 2*S+1
            dots = []
            for i in xrange(R, rows):
                for j in xrange(C, cols):
                    if m_in[i,j] == 0:
                        # print i,j
                        dots.append((i,j))
            if len(dots) >= (delta * ((2*S+1)**2)):
                break
            else:
                prev_dots = dots
                S += 1
        else:
            break

    commands = [('PAINT_SQUARE', R+S-1, C+S-1, S-1)]
    for i in prev_dots:
        commands.append(('ERASE_CELL', i[0], i[1]))
    return ((2*(S-1)+1)**2) - len(prev_dots), commands


def check_line(R1,C1,R2,C2,matrix, verbose=False):
    if R1 < 0 or R2 >= np.shape(matrix)[0] or C1 < 0 or C2 >= np.shape(matrix)[1]:
        if verbose:  print 'Out of bound'
        return False
    if R1 > R2 or C1 > C2:
        if verbose:  print 'Inverted indexes'
        return False
    if R1==R2 or C1==C2:
        return True
    return False

def h_line(m_in, R, C):
    S = 0
    while check_line(R,C,R,C + S,m_in):
        if m_in[R,C+S] == 1:
            S += 1
        else:
            break
    return S, [('PAINT_LINE', R, C, R, C+S-1)]


def v_line(m_in, R, C):
    S = 0
    while check_line(R,C,R + S,C,m_in):
        if m_in[R+S,C] == 1:
            S += 1
        else:
            break
    return S, [('PAINT_LINE', R, C, R+S-1, C)]
