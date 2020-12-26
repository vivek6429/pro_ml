# Import QApplication and all the required widgets from PyQt5.QtWidgets.
# Create an instance of QApplication.
# Create an instance of your application’s GUI.
# Show your application’s GUI.
# Run your application’s event loop (or main loo


import sys
from PyQt5.QtWidgets import QApplication,QLabel,QWidget

app=QApplication(sys.argv)
window=QWidget()
window.setWindowTitle("An app")
window.setGeometry(100,100,280,80) # x,y,w,h
window.move(100,100)
helomesage=QLabel("helo world",parent=window)
helomesage.move(100,50)



window.show()
sys.exit(app.exec_())