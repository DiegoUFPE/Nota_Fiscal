
from urllib.parse import urlparse


from PyQt5.QtWidgets import *

import MyGUIFile as mg

def main():
    app = QApplication([])
    window = mg.MyGUI()
    app.exec_()

if __name__ == "__main__":
    main()
