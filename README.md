## Synopsis

THREDDS Explorer is a QGIS-based plug-in designed to make it easy for users to access georeferenced data accessible through any THREDDS based server.  

Data catalogues and maps are exposed to the user through a simple user interface, which allows him to choose any map or explore all contents of the server without resorting to exploring the default web based THREDDS interface.

This plug-in should work with most THREDDS servers, and will be able to retrieve any layer provided through WMS, WMS-T and/or WCS services published by the server.

[![THREDDS Explorer](https://raw.githubusercontent.com/IHCantabria/THREDDSExplorer/master/doc/video.jpg)](https://vimeo.com/167414368)

## Installation

**Dependencies:** THREDDSExplorer requires the *processing* plug-in by V. Olaya, available within the standard QGIS Installation (also at https://plugins.qgis.org/plugins/processing/).

Installing the plug-in basically involves copying the code in a QGIS "plugins" directory, as detailed below.

Please note that it is mandatory that the folder where the code resides is called "THREDDSExplorer". If you download the code in ZIP format the default name ("THREDDSExplorer-$VERSION") must be changed to "THREDDSExplorer".

### For Windows

The folder where the code should be copied is the following, substituting "`%USERNAME%`" with your user name:

	C:\Users\%USERNAME%\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins


### For Linux

Not tested yet. 

### For Mac OS X

Not tested yet.

## User Manual

For more information you can find a PDF manual under the "doc" folder.
