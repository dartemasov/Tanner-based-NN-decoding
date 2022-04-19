import numpy as np
import pyldpc as ldpc
import os

def getBinaryMatrix(source):
    source = os.path.expanduser(source)
    fileObj = bz2.BZ2File(source, 'r') if source.endswith('bz2') else open(source, 'rt')
    with fileObj as f:
        lines = [[int(x) for x in l.strip().split()]
                  for l in f.readlines()
                  if len(l.strip()) > 0]

    if lines[0][0] in (0, 1):  # explicit 0/1 representation
        return np.array(lines, dtype=np.int)
    return alistToNumpy(lines)

def alistToNumpy(lines):
    nCols, nRows = lines[0]
    if len(lines[2]) == nCols and len(lines[3]) == nRows:
        startIndex = 4
    else:
        startIndex = 2
    matrix = np.zeros((nRows, nCols), dtype=int)
    for col, nonzeros in enumerate(lines[startIndex:startIndex + nCols]):
        for rowIndex in nonzeros:
            if rowIndex != 0:
                matrix[rowIndex - 1, col] = 1
    return matrix


class Code:
	def __init__(self):
		self.num_edges = 0

def load_code(H_filename):

    H = getBinaryMatrix(H_filename)    
    m, n = H.shape
    k = n-m
    G = ldpc.coding_matrix(H).T
    var_degrees = H.sum(axis=0)
    chk_degrees = H.sum(axis=1)
    num_edges = H.sum()
    
    var_edges = [[] for _ in range(0,n)]
    for i in range(0,n):
        var_edges[i] = list(np.where(H[:,i] == 1)[0])
    
    chk_edges = [[] for _ in range(0,m)]
    for i in range(0,m):
        chk_edges[i] = list(np.where(H[i] == 1)[0])
    
    
    d = [[] for _ in range(0,n)]
    edge = 0
    for i in range(0,n):
        for j in range(0,var_degrees[i]):
            d[i].append(edge)
            edge += 1
    
    u = [[] for _ in range(0,m)]
    edge = 0
    for i in range(0,m):
        for j in range(0,chk_degrees[i]):
            v = chk_edges[i][j]
            for e in range(0,var_degrees[v]):
                if (i == var_edges[v][e]):
                    u[i].append(d[v][e])
    
    code = Code()
    code.H = H
    code.G = G
    code.var_degrees = var_degrees
    code.chk_degrees = chk_degrees
    code.num_edges = num_edges
    code.var_edges = var_edges
    code.chk_edges = chk_edges
    code.u = u
    code.d = d
    code.n = n
    code.m = m
    code.k = k
    return code