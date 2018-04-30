"""
Implements functions to use tData library.
"""

import numpy as np
from tData import ffi, lib
import pycblosc2 as cb2


def tData(src, sub_shp, inverse=False):
    """
    Apply a data transformation based in reorganize data partitions.

    Parameters
    ----------
    src : np.array
        Data to transform.
    sub_shp: int[] or tuple
        Data partition shape.
    inverse: bool, optional

    Returns
    -------
    dest: np.array
        Data transformed.
    d: dict
        Dictionary with partitions indexation.
    """

    # Obtain src parameters

    typesize = src.dtype.itemsize
    shape = src.shape
    dimension = len(shape)

    # Calculate the extended dataset parameters

    pad_shp = []

    for i in range(len(shape)):
        d = shape[i]
        if shape[i] % sub_shp[i] != 0:
            d = shape[i] + sub_shp[i] - shape[i] % sub_shp[i]
        pad_shp.append(d)

    size = np.prod(pad_shp)

    # Create destination dataset

    dest = np.empty(size, dtype=src.dtype).reshape(pad_shp)

    # Transform datasets to buffers (for use in cffi)

    src_b = ffi.from_buffer(src)
    dest_b = ffi.from_buffer(dest)

    # Execute the transformation

    lib.tData(src_b, dest_b, typesize, shape, pad_shp, sub_shp, size, dimension, inverse)

    d = createIndexation(pad_shp, sub_shp)

    return dest, d


def reorder_dim(dim, l):
    aux = []
    for i in range(len(dim)):
        aux.append(dim[(i+l) % len(dim)])
    return aux


def create_shape(s):
    s_aux = [1, 1, 1, 1, 1, 1, 1, 1]

    for i in range(len(s)):
        s_aux[-len(s) + i] = s[i]
    return s_aux


def createIndexation(shape, sub_shp):
    """
    Create an indexation of data partitions.

    Parameters
    ----------
    shape : int[] or tuple
        Data shape.
    sub_shp: int[] or tuple
        Data partition shape.

    Returns
    -------
    indexation: dict
        Dictianary containing the indexation.
        key: partition number
        value: schunk number to decompress
    """

    dimension = len(shape)

    # Calculate the partitions the size

    size = int(np.prod(shape)/np.prod(sub_shp))

    keys = np.zeros(size, dtype=np.int64)

    k_b = ffi.from_buffer(keys)

    # Create the indexation

    lib.createIndexation(k_b, shape, sub_shp, dimension)

    # Create a dicttionary with keys and values

    d = dict([(k, v) for v, k in enumerate(keys)])

    return d


def obtainIndex(dim, dic, s, sb):

    s = create_shape(s)
    sb = create_shape(sb)

    ind = []

    for a in range(dim[0][0]//sb[0]*sb[0], dim[0][1], sb[0]):
        for b in range(dim[1][0]//sb[1]*sb[1], dim[1][1], sb[1]):
            for c in range(dim[2][0]//sb[2]*sb[2], dim[2][1], sb[2]):
                for d in range(dim[3][0]//sb[3]*sb[3], dim[3][1], sb[3]):
                    for e in range(dim[4][0]//sb[4]*sb[4], dim[4][1], sb[4]):
                        for f in range(dim[5][0]//sb[5]*sb[5], dim[5][1], sb[5]):
                            for g in range(dim[6][0]//sb[6]*sb[6], dim[6][1], sb[6]):
                                for h in range(dim[7][0]//sb[7]*sb[7], dim[7][1], sb[7]):

                                    K = (h
                                         + g*s[7]
                                         + f*s[7]*s[6]
                                         + e*s[7]*s[6]*s[5]
                                         + d*s[7]*s[6]*s[5]*s[4]
                                         + c*s[7]*s[6]*s[5]*s[4]*s[3]
                                         + b*s[7]*s[6]*s[5]*s[4]*s[3]*s[2]
                                         + a*s[7]*s[6]*s[5]*s[4]*s[3]*s[2]*s[1])

                                    ind.append(((a, b, c, d, e, f, g, h), dic[K]))
    return ind


# Compression/decompression functions


def compress(src, pad_shp):
    size = src.size
    itemsize = src.dtype.itemsize
    bsize = size * itemsize

    dest = np.empty(size, dtype=src.dtype)

    cb2.blosc_set_blocksize(np.prod(pad_shp) * itemsize)

    size_c = cb2.blosc_compress(5, 1, itemsize, bsize, src, dest, bsize)

    return dest


def decompress(comp, s, itemsize, dtype):

    size = np.prod(s)
    bsize = size * itemsize

    dest = np.empty(size, dtype=dtype).reshape(s)

    size_d = cb2.blosc_decompress(comp, dest, bsize)

    return dest


def get_block(comp, index, pad_shp, dtype):

    size = np.prod(pad_shp)

    dest = np.empty(size, dtype=dtype)

    size_d = cb2.blosc_getitem(comp, index * size, size, dest)

    return dest


def decompress_trans(comp, indexation, dtype, s, ts, sb, a=None, b=None, c=None, d=None,
                     e=None, f=None, g=None, h=None):

    dim = reorder_dim([a, b, c, d, e, f, g, h], len(s))

    s = create_shape(s)
    ts = create_shape(ts)
    sb = create_shape(sb)

    index_aux = [1, 1, 1, 1, 1, 1, 1, 1]
    ul = np.copy(ts)
    ui = [(0, ts[0]), (0, ts[1]), (0, ts[2]), (0, ts[3]), (0, ts[4]), (0, ts[5]), (0, ts[6]),
          (0, ts[7])]

    for i in range(len(index_aux)):
        if dim[i] is not None:
            ul[i] = sb[i]
            ui[i] = (dim[i], dim[i]+1)
            index_aux[i] = 0
            dim[i] = dim[i] % ul[i]
        else:
            dim[i] = slice(0, s[i])

    subpl = ul

    ind = obtainIndex(ui, indexation, ts, sb)

    dest = np.zeros(np.prod(subpl), dtype=dtype).reshape(subpl)

    for index, n in ind:

        index = [index[q]*index_aux[q] for q in range(len(dim))]

        aux = get_block(comp, n, sb, dtype).reshape(sb)

        dest[index[0]:index[0]+sb[0],
             index[1]:index[1]+sb[1],
             index[2]:index[2]+sb[2],
             index[3]:index[3]+sb[3],
             index[4]:index[4]+sb[4],
             index[5]:index[5]+sb[5],
             index[6]:index[6]+sb[6],
             index[7]:index[7]+sb[7]] = aux

    return dest[dim]
