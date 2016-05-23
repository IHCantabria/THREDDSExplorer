## Synopsis

THREDDS Explorer is a QGIS-based plug-in designed to make it easy for users to access georeferenced data accessible through any THREDDS based server.  

Data catalogues and maps are exposed to the user through a simple user interface, which allows him to choose any map or explore all contents of the server without resorting to exploring the default web based THREDDS interface.

This plug-in should work with most THREDDS servers, and will be able to retrieve any layer provided through WMS, WMS-T and/or WCS services published by the server.

[![THREDDS Explorer](https://raw.githubusercontent.com/IHCantabria/THREDDSExplorer/master/doc/video.jpg)](https://vimeo.com/167414368)

## Installation

To install this plug-in, copy the content to your QGIS plug-in directory:
Usually these are the locations for plugins repository:

### For windows

    $ C:\Program Files\QGIS\python\plugins
    $ C:\Documents and Settings\$username\.qgis\python\plugins

### For Linux

This procedure works on Linux Mint 17.3, with QGIS 2.14 Essen. If you want to download the latest version of the code via git, and make it available for a single user:

    $ mkdir ~/.qgis2/python/plugins
    $ cd ~/.qgis2/python/plugins/
    $ git clone https://github.com/IHCantabria/THREDDSExplorer.git

If you want to download a ZIP, you can also do so:

    $ mkdir ~/.qgis2/python/plugins
    $ cd ~/.qgis2/python/plugins/
    $ wget https://github.com/IHCantabria/THREDDSExplorer/archive/master.zip
    $ unzip master.zip
    $ mv THREDDSExplorer-master THREDDSExplorer
    $ rm master.zip

In the examples above you can substitute the plugins directory for `/share/qgis/python/plugins/`, if you want to install the plugin system-wide, for all the users. In that case, you will have to use sudo or be root to `mkdir` the plugins folder, and download content to it.

### For Mac OS X

    $ /Contents/MacOS/share/qgis/python/plugins
    $ /Users/$username/.qgis/python/plugins

**NOTE**

It is possible to define additional paths for QGIS to look for your plug-ins, by defining the `_QGIS_PLUGINPATH_` environment variable with a full path to the new desired plug-in folder.

## User Manual

For more information you can find a PDF manual under the "doc" folder.
