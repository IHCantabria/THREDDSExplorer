# -*- coding: utf-8 -*-
"""
/***************************************************************************
 THREDDSExplorer
                                 A QGIS plugin
 Static and animated data viewer for THREDDS based servers
                             -------------------
        begin                : 2016-05-19
        copyright            : (C) 2016 by IH Cantabria
        email                : beneditom@unican.es
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load THREDDSExplorer class from file THREDDSExplorer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .THREDDS_Explorer import THREDDSExplorer
    return THREDDSExplorer(iface)
