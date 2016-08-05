**CURRENT**

* ServerDataPersistenceManager.py
    - Fixed persistence of server list in Linux converting them to new format 


* AnimationController2.py, AnimationWMSManager.py, WMSBatchDownloadUtil.py, WMSParser.py
    - Added functionality to work with editable bbox


* Visor_UI.py
     - Added feedback when loading WCS layers with invalid bbox
     - Added functionality to work with editable bbox


* THREDDS_Explorer_dockwidget_base.ui, Animation_add_wcs_layer.ui
    - Modified interface with editable values for WCS boundingBox


* Utilities.py
    - Added function to check platform (Windows vs Linux)


* WCSParser.py
    - Solved bug when loading WCS layers: Creation of a temporal file to store the .tiff from the WCS request
    - Added functionality to work with editable bbox


* icon.png
    - Replaced the plugin icon (grey) to new one (blue)

**v1.1** (2016-06-10)

* ServerDataPersistenceManager.py
    - Solved bug when reading variable "GDALVersionErrorSetting" (2016.06.06)


* Visor_UI.py
    - Moved GDAL version warning to WCS tab for Linux users


* ServerDataPersistenceManager.py
    - Do not show server list window on `__init__` method


* VisorController.py
    - Show server list window when button is clicked


* THREDDS_Explorer_dockwidget_base.ui, THREDDS_Explorer_dockwidget.py
    - Add vertical and horizontal scrolls to the plugin's main user interface


* General
  - Trace errors into QGIS/THREDDSExplorer registry tab
  - ui2py: script to automate .ui to .py conversion (2016-06-10)

**v1.0** (2016-05-31)

* Connect to THREDDS Server
* List THREDDS Server contents
* Download WMS
* Download WCS
* Animate WMS/WCS layers
