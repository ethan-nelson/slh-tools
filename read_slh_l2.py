# -*- coding: utf-8 -*-
# MIT License (c) 2017 Ethan Nelson

import struct
import numpy as np
import gzip

msg = "File can't be opened. Check its path and extension: %s"
gz_msg = "File not zipped or can't be opened. Check its path and extension: %s"
req_msg = "The %s is required to read this file type."


def _file_handler(filename):
    """
    Handles opening file and exception
    """
    if filename[-2:] == 'gz':
        try:
            f = gzip.open(filename, 'rb')
        except:
            raise Exception(gz_msg % (filename,))
    else:
        try:
            f = open(filename, 'rb')
        except:
            raise Exception(msg % (filename,))

    return f


def read_gridded(lh_filename=None, q1r_filename=None):
    """
    Reads gridded level 2 SLH files.

    Currently, no scaling is done.
    """

    prodshape = [19, 148, 720]
    countshape = [148, 720]

    prodsize = 720 * 148 * 19
    countsize = 720 * 148

    readprodsize = prodsize * 2
    readcountsize = countsize * 2

    prodstruct = "<" + ('h' * prodsize)
    countstruct = "<" + ('h' * countsize)

    data = {}

    if lh_filename is not None:
        f = _file_handler(lh_filename)
        f.seek(0)

        data['convLHMean'] = f.read(readprodsize)
        data['convPix'] = f.read(readcountsize)
        data['stratLHMean'] = f.read(readprodsize)
        data['stratPix'] = f.read(readcountsize)
        data['allPix'] = f.read(readcountsize)

        f.close()

    if q1r_filename is not None:
        f = _file_handler(q1r_filename)
        f.seek(0)
        data['convQ1RMean'] = f.read(readprodsize)
        data['convPix'] = f.read(readcountsize)
        data['stratQ1RMean'] = f.read(readprodsize)
        data['stratPix'] = f.read(readcountsize)
        data['allPix'] = f.read(readcountsize)

        f.close()

    for product in data:
        if 'Pix' in product:
            data[product] = struct.unpack(countstruct, data[product])
            data[product] = np.reshape(data[product], countshape)
        else:
            data[product] = struct.unpack(prodstruct, data[product])
            data[product] = np.reshape(data[product], prodshape)

    return data


def read_nongridded(geo_filename=None, dat_filename=None):
    """
    Reads non-gridded level 2 SLH files.

    Currently, no scaling is done.
    """

    if geo_filename is not None:
        f = _file_handler(geo_filename)
    else:
        raise Exception(req_msg % ("geo file",))
    f.seek(0)
    geo_data = f.read()
    f.close()

    nscans = len(geo_data) / 396

    geoshape = [nscans, 49]
    timeshape = [nscans]

    geosize = 49
    timesize = 1

    # Non-gridded files are written by scan, so we read one scan at a time
    readgeosize = geosize * 4
    readtimesize = timesize * 4
    onescansize = readgeosize * 2 + readtimesize

    timestruct = "<" + ('f' * timesize * nscans)
    geostruct = "<" + ('f' * geosize * nscans)

    geovars = ['Scantime', 'Lat', 'Lon']

    data = {}

    for var in geovars:
        data[var] = ''

    for scan in range(nscans):
        data['Scantime'] += geo_data[(onescansize*scan):
                                     (onescansize*scan)+readtimesize]
        data['Lat'] += geo_data[(onescansize*scan)+readtimesize:
                                (onescansize*scan)+readtimesize+readgeosize]
        data['Lon'] += geo_data[(onescansize*scan)+readtimesize+readgeosize:
                                onescansize*(scan+1)]

    for var in geovars:
        if var == 'Scantime':
            data[var] = struct.unpack(timestruct, data[var])
            data[var] = np.reshape(data[var], timeshape)
        else:
            data[var] = struct.unpack(geostruct, data[var])
            data[var] = np.reshape(data[var], geoshape)
    data['nscans'] = nscans

    del geo_data, timestruct, geostruct

    if dat_filename is not None:
        f = _file_handler(dat_filename)
        f.seek(0)

        prodshape = [nscans, 80, 49]
        countshape = [nscans, 49]

        # Non-gridded files are written by scan, so we read one scan at a time
        prodsize = 80 * 49
        countsize = 49

        readprodsize = prodsize * 2
        readcountsize = countsize * 2

        prodstruct = "<" + ('h' * prodsize * nscans)
        countstruct = "<" + ('h' * countsize * nscans)

        datvars = ['lh', 'q1r', 'rtype', 'ltop', 'lmelt', 'lsfc', 'rmelt',
                   'rsfc', 'rtype2a25', 'method']

        for var in datvars:
            data[var] = ''

        for i in range(nscans):
            data['lh'] += f.read(readprodsize)
            data['q1r'] += f.read(readprodsize)
            for var in datvars[2:]:
                data[var] += f.read(readcountsize)
        f.close()

        for var in datvars:
            if var in ['lh', 'q1r']:
                data[var] = struct.unpack(prodstruct, data[var])
                data[var] = np.reshape(data[var], prodshape)
            else:
                data[var] = struct.unpack(countstruct, data[var])
                data[var] = np.reshape(data[var], countshape)

    return data
