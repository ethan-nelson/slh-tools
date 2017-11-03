Read SLH Level 2
================

This script contains functions to read level 2 [Spectral Latent Heating (SLH)](http://www.eorc.jaxa.jp/TRMM/lh/) data from the [Tropical Rainfall Measurement Mission (TRMM)](https://trmm.gsfc.nasa.gov/). These scripts follow the file format in [the documentation](http://www.eorc.jaxa.jp/TRMM/lh/doc/ReadMe_SLH_v02.pdf).

Functions
---------

### `read_gridded(lh_filename, q1r_filename)`

This reads level 2 gridded data.

The inputs are optional, but are `lh_filename` for the full path of the latent heating file and `q1r_filename` for the full path of the q1-qr file. Files can be either gzipped or unzipped. It is assumed the files correspond to the same granule. 

The output is a dictionary with the following keys: `convLHMean`, `convPix`, `stratLHMean`, `stratPix`, and `allPix` for latent heating files; `convQ1RMean`, `convPix`, `stratQ1RMean`, `stratPix`, and `allPix` for the q1-qr files. Profiles will have the shape `hgt x lat x lon` which, because these are pre-gridded, are consistently `19 x 148 x 720`, while counts will be `lat x lon` or `148 x 720`.

### `read_nongridded(geo_filename, dat_filename)`

This reads level 2 non-gridded data.

`geo_filename` is the full path of the geodata file and it is required. `dat_filename` is the full path of the data file and is optional. Either file can be gzipped or unzipped. Again, it is assumed the files correspond to the same granule.

The output is a dictionary with the following keys: `Scantime`, `Lat`, `Lon`, `nscans`; if the data file is given, additional keys will include `lh`, `q1r`, `rtype`, `ltop`, `lmelt`, `lsfc`, `rmelt`, `rsfc`, `rtype2a25`, and `method`. Profiles will have the shape `nscans x 80 x 49`, the time variable will have the shape `nscans`, and other products will have the shape `nscans x 49`.
