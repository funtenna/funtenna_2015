#Basic Installation Instructions

For notes on installation/creation of Gnuradio Out-Of-Tree modules:
https://gnuradio.org/redmine/projects/gnuradio/wiki/OutOfTreeModules

For Linux:
    `cd build`
    `cmake ..`
    `make`
    `make install`

Mac OS X Notes:
    On OS X, if you have linked your Gnuradio build with a non-system version
    of Python (homebrew, macports, etc.), you must supply cmake with the same
    Python paths.

    Here is an example if Gnuradio was linked with a homebrew python path:

    `cd build`
    `cmake -DPYTHON_LIBRARY=/usr/local/Cellar/python/2.7.10/Frameworks/Python.framework/Versions/2.7/lib/libpython2.7.dylib -DPYTHON_INCLUDE_DIR=/usr/local/Cellar/python/2.7.10/Frameworks/Python.framework/Versions/2.7/include/python2.7 ..`
    `make`
    `make install`
