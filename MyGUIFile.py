import sys
import cv2
from urllib.parse import urlparse

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui

import ExtractUrlDataFile as eud
import ReadWriteGoogleSheet as googleSheet
import PurchaseAnalysis as pa

class MyGUI(QMainWindow): #QMainWindow was imported from PyQt5.QtWidgets

    def __init__(self):
        super(MyGUI,self).__init__()
        uic.loadUi("qr_scanner_gui_v3.ui",self)
        self.show()
        
        self.current_file = ""
        self.url = ""
        self.actionLoad.triggered.connect(self.load_image) #accessing object names from ui file
        self.actionQuit.triggered.connect(self.quit_program)
        self.actionGeneral.triggered.connect(self.purchase_analysis_general)
        self.actionYearly.triggered.connect(self.purchase_analysis_year)
        self.actionMonthly.triggered.connect(self.purchase_analysis_month)
        self.pushButton.clicked.connect(self.read_code)
        self.pushButton_2.clicked.connect(self.update_purchase)

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self,"Open File", "", "All Files (*)",options=options) #we open a file dialog and get the file name
        #unnamed parameters since they are unused

        if filename != "":
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            pixmap = pixmap.scaled(300,415)
            self.label.setScaledContents(True)
            self.label.setPixmap(pixmap)

    def read_code(self):
        try:
            img = cv2.imread(self.current_file)
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(img)
            self.url = data
            if self.url != "":
                self.textEdit.setText("The URL was extracted: "+data)
            else:
                self.textEdit.setText("The URL was unable to be extracted from image.")
        except:
            self.textEdit.setText("No current file was loaded.")
    
    def update_purchase(self):
        if self.url != "":
            e = eud.ExtractUrlData(self.url)
            if e.evaluate_domain():
                date, place, prods, success = e.get_info_dict()
                #print(prods,date)
                if(success):
                    gs = googleSheet.ReadWriteGoogleSheet(prods,date)
                    if gs.update_sheet():
                        self.textEdit.setText("The purchase made in "+place+" emitted on "+date+" was updated to sheet.")
                    else:
                        self.textEdit.setText("The purchase's content was already updated to sheet previously.")
                    #print(prods)
                else:
                    self.textEdit.setText("The program failed to extract the products.")
            else:
              self.textEdit.setText("The domain is not correspondent to the nfce website.")
        else:
            self.textEdit.setText("No invoice was loaded.")

    def purchase_analysis(self, isYearly = False, isMonthly = False):
        gs = googleSheet.ReadWriteGoogleSheet()
        analysis = pa.PurchaseAnalysis()
        dict_sheet = gs.get_dict_sheet()
        if isYearly:
            try:
                analysis.get_analysis(dict_sheet,isYearly,isMonthly)
                self.textEdit.setText("The graph image was generated.")
            except:
                self.textEdit.setText("It was not possible to generate graph image.")
        elif isMonthly:
            try:
                analysis.get_analysis(dict_sheet,isYearly,isMonthly)
                self.textEdit.setText("The graph image was generated.")
            except:
                self.textEdit.setText("It was not possible to generate graph image.")
        else:
            try:
                analysis.get_analysis(dict_sheet,isYearly,isMonthly)
                self.textEdit.setText("The graph image was generated.")
            except:
                self.textEdit.setText("It was not possible to generate graph image.")

    def purchase_analysis_general(self):
        self.purchase_analysis()

    def purchase_analysis_year(self):
        self.purchase_analysis(isYearly=True)

    def purchase_analysis_month(self):
        self.purchase_analysis(isMonthly=True)

    def quit_program(self):
        sys.exit(0)