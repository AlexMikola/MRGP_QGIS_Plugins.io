# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MRGP - набор функций для Qgis
 ***************************************************************************//
"""

from qgis.PyQt.QtCore import QCoreApplication, QTranslator, QSettings, qVersion
# from qgis.PyQt.QtGui import QIcon
# from qgis.PyQt.QtWidgets import QAction
from qgis.core import (QgsExpression, QgsExpressionFunction, QgsExpressionContextUtils, QgsProject)
from qgis.core import *
from qgis.utils import qgsfunction

import os.path

PLUGVER = '0.0.3'
PLUGNAME = 'mrgp_Functions'
NAMEICON = 'plug_icon.png'


def tr(string):
    return QCoreApplication.translate('@default', string)


class Main_cl(object):

    def __init__(self, iface):
        self.iface = iface
        self.plugDialog = None
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            f'{PLUGNAME}' + '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

            if qVersion() > PLUGVER:
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        QgsExpression.registerFunction(self.get_extend_map_from_layout)

    def unload(self):
        QgsExpression.unregisterFunction('get_extend_map_from_layout')

    comment = """
        <h1>Получаем extend карты из отчета где:</h1>
        <p><b>get_extend_map_from_layout</b>(<font color="#FF0000">composerTitle</font>, <font color="#FF0000">mapName</font>)
        <ul>
        <li><i><font color="#FF0000"> composerTitle </font> → название макета
        <li><i><font color="#FF0000"> mapName  </font> → название карты
        </ul>
        <p>----------------------------------------------------------------
        <h2>Example usage:</h2>
        <p><b>get_extend_map_from_layout('Фрагмент_КРТ','Карта_Фрагмент_КРТ')</b>
        <p><i>→ POLYGON((7598.6 13970.3, 8537.6 13970.3, 8537.6 14925.3, 7598.6 14925.3, 7598.3 13970.3))
        """

    @staticmethod
    @qgsfunction(args='auto', group='_MRGP_', usesGeometry=False, referencedColumns=[], helpText=f'{comment}')
    def get_extend_map_from_layout(composerTitle, mapName, feature, parent):
        project = QgsProject.instance()
        projectLayoutManager = project.layoutManager()
        layout = projectLayoutManager.layoutByName(composerTitle)
        map = layout.itemById(mapName)
        return str(map.extent().asWktPolygon())

