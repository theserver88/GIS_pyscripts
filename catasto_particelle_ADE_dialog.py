# -*- coding: utf-8 -*-
"""

"""

import os
import requests
import zipfile

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtSvg import QSvgRenderer
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.utils import iface, Qgis
from qgis.core import QgsProject, QgsVectorLayer, QgsCoordinateReferenceSystem

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'catasto_particelle_ADE_base.ui'))

BASE_URL = 'https://iicd.geoinnova.it'

class ItalyInspireCadastreDownloaderDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ItalyInspireCadastreDownloaderDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface
        self.msgBar = iface.messageBar()
        
        self.plugin_dir = os.path.dirname(__file__)
        
        self.lineEdit_path.clear()
        self.comboBox_region.clear()
        self.comboBox_province.clear()
        self.comboBox_municipality.clear()
        self.checkBox_addToMap.setChecked(1)
        
        # show the dialog
        self.progressBar.setValue(0)
        self.setWindowIcon(QIcon(os.path.join(self.plugin_dir,'icons','icon.png')))
        self.show()
        
        # pixmap = QPixmap(100, 50)
        pixmap = QPixmap(os.path.join(self.plugin_dir,'icons',' '))  # Cargar imagen PNG
        # pixmap_scaled = pixmap.scaledToWidth(50)
        self.label_svg.setMaximumWidth(225)
        self.label_svg.setMaximumHeight(67)
        self.label_svg.setPixmap(pixmap)
        self.label_svg.setScaledContents(True)  # Escalar la imagen para ajustarla
               
        self.municipality_activated = False
        self.directory_activated = False
        
        self.pushButton_select_path.clicked.connect(self.select_output_folder)
        
        # Get data and load regions
        self.get_data()
        self.load_regions()
        
        # Conectar eventos
        self.comboBox_region.currentIndexChanged.connect(self.load_provinces)
        self.comboBox_province.currentIndexChanged.connect(self.load_municipalities)
        self.comboBox_municipality.currentIndexChanged.connect(self.restart_progressbar)
        self.pushButton_run.clicked.connect(self.download)
        # self.button_box.clicked.connect(self._close)


    def select_output_folder(self) -> None:
        """Select output folder"""
        self.lineEdit_path.clear()
        folder = QFileDialog.getExistingDirectory(self, self.tr("Select folder"))
        self.lineEdit_path.setText(folder)
        if os.path.isdir(self.lineEdit_path.text()):
            self.directory_activated = True
            self.restart_progressbar()
        
    
    def make_request(self, endpoint, save_directory=None, file_name=None):
        """
        Realiza una solicitud GET a un endpoint de la API.

        :param endpoint: El endpoint de la API.
        :param save_directory: (Opcional) Carpeta donde guardar el archivo si es una descarga.
        :param file_name: (Opcional) Nombre del archivo sin la extensión.
        :return: Datos JSON o confirma la descarga del archivo.
        """
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url)

        if response.status_code == 200:
            if save_directory and file_name:
                os.makedirs(save_directory, exist_ok=True)
                complete_file_path = os.path.join(save_directory, f"{file_name}.zip")
                with open(complete_file_path, 'wb') as file:
                    file.write(response.content)
                return True
            else:
                return response.json()
        else:
            msg = self.tr(f"An error occurred while request data. Code error: ")
            self.msgBar.pushMessage(f'{msg} {response.status_code}', level=Qgis.Warning, duration=3)
            return None

        # Ejemplo de uso
        # Descargar un archivo
            
    def get_data(self):
        
        self.json_data = self.make_request('/all_municipalities')
        self.comboBox_region.clear()
        self.comboBox_province.clear()
        self.comboBox_municipality.clear()
        
        
    def load_regions(self):
        """Cargar todas las regiones en el ComboBox de regiones."""
        self.comboBox_region.clear()
        self.comboBox_region.addItem(self.tr("Scegli Regione"), None)  # Opción por defecto
        for region in self.json_data.keys():
            self.comboBox_region.addItem(region, region)
            
        self.municipality_activated = False
        self.restart_progressbar()

    def load_provinces(self):
        """Cargar provincias basadas en la región seleccionada."""
        self.comboBox_province.clear()
        self.comboBox_municipality.clear()
        region = self.comboBox_region.currentData()

        if region and region in self.json_data:
            self.comboBox_province.addItem(self.tr("Scegli Provincia"), None)
            for province in self.json_data[region].keys():
                self.comboBox_province.addItem(province, province)
        
        self.municipality_activated = False
        self.restart_progressbar()

    def load_municipalities(self):
        """Cargar municipios basados en la provincia seleccionada."""
        self.comboBox_municipality.clear()
        region = self.comboBox_region.currentData()
        province = self.comboBox_province.currentData()

        if region and province and province in self.json_data[region]:
            self.comboBox_municipality.addItem(self.tr("Scegli Comune"), None)
            for municipality in self.json_data[region][province]:
                self.comboBox_municipality.addItem(municipality, municipality)
                
        self.municipality_activated = True
        self.restart_progressbar()
        
    
    def restart_progressbar(self):
        self.progressBar.setValue(0)
        
    
    def unzip_file(self, zipfilename, folder_extract):
        
        try:
            if os.path.exists(zipfilename):
                with zipfile.ZipFile(zipfilename, "r") as z:
                    z.extractall(folder_extract)
        except:
            msg = self.tr("An error occurred while decompressing the file")
            self.msgBar.pushMessage(f'{msg}', level=Qgis.Warning, duration=3)
            return None
        
    
    def add_layers(self, folder, group_name):

        project = QgsProject.instance()
        tree_root = project.layerTreeRoot()
        layers_group = tree_root.addGroup(group_name)


        for gmlfile in os.listdir(folder):
            if gmlfile.endswith('.gml'):
                layer_path = os.path.join(folder, gmlfile)
                file_name = os.path.splitext(gmlfile)[0]
                gml_layer = QgsVectorLayer(layer_path, file_name, "ogr")

                if gml_layer.isValid():
                 # Set CRS to EPSG:4326
                 crs = QgsCoordinateReferenceSystem("EPSG:4326")
                gml_layer.setCrs(crs, True)

                project.addMapLayer(gml_layer, False)
                layers_group.addLayer(gml_layer)

        

    def download(self):
        
        
        region = self.comboBox_region.currentData()
        province = self.comboBox_province.currentData()
        municipality = self.comboBox_municipality.currentData()
        folder = self.lineEdit_path.text()
        file = os.path.join(folder, municipality+".zip")
        
        folder_extract = os.path.splitext(file)[0]
        
        if os.path.isdir(folder_extract):
            msg = self.tr("The folder already exists")
            self.msgBar.pushMessage(f'{msg}', level=Qgis.Warning, duration=3)
            return None
        else:
            os.makedirs(folder_extract)
        
        if not self.directory_activated:
            msg = self.tr("You must add a download folder")
            self.msgBar.pushMessage(f'{msg}', level=Qgis.Warning, duration=3)
            return None

        
            
        if municipality not in ("",self.tr("Select a municipality")) and self.municipality_activated:
            self.make_request(f'/download/{region}/{province}/{municipality}', folder, municipality)
            self.progressBar.setValue(50)
            self.unzip_file(file, folder_extract)
            os.remove(file)
            self.progressBar.setValue(100)
            msg = self.tr("Download successfuly completed")
            self.msgBar.pushMessage(f'{msg}', level=Qgis.Info, duration=3)
            
            #Load layer
            if self.checkBox_addToMap.isChecked():
                self.add_layers(folder_extract, municipality)
                
        else:
            msg = self.tr("You must select a municipality")
            self.msgBar.pushMessage(f'{msg}', level=Qgis.Warning, duration=3)
            return None

    
    def check_form(self, option: int) -> None:
        """Message for fields without information"""

        messages = {
            1: self.tr('You must complete the data of the province and municipality and indicate the download route.'),
            2: self.tr('You must select at least one cadastral entity to download.')
        }

        QgsMessageLog.logMessage(messages[option], 'SICD',
                                 level=Qgis.Warning)

        self.msgBar.pushMessage(messages[option], level=Qgis.Warning, duration=3)
        
    
    def _close(self):
        self.close()
        
