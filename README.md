xbmc-remote
===========

A music remote control for xbmc

At the momment it's a bit rough, but does work.

Dependencies:

* python-bottle
* python-paste
* xbmcjson (python)
* xbmc
* It also assumes the Radio addon is installed in xbmc with the radio stations you want selected as 'My Stations' (http://wiki.xbmc.org/index.php?title=Add-on:Radio)

to run it, put the files in a directory on the xbmc computer, then run 'python remote.py'

By default, it will start a web server on port 8000 and server up the remote control there.

Note -- it doesn't have to be on the computer hosting xbmc (you can change this), but if it's not, downloading files won't work.


