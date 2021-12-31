from PyQt5.QtWidgets import QApplication, QStackedLayout, QComboBox, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt
import podman
import sys

lists = []
pageLayouts = []
pages = []

client = podman.PodmanClient()

class Window(QWidget):
        print("** Check Service Available")
        if client.ping():
            print("Service active")
        else:
            print(f"No service found @ {client.base_url}")

        lists.append(client.images.list())
        lists.append(client.containers.list())
        lists.append(client.pods.list())
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Podman GUI")
            self.setLayout(layout)
            self.left = 10
            self.top = 10
            self.width = 300
            self.height = 300
            self.initGUI()

        def initGUI(self):
            #palette = QPalette()
            #palette.setColor(QPalette.ButtonText, Qt.red)
            #app.setPalette(palette)

            #self.textbox = QLineEdit()

            self.setLayout(QVBoxLayout())
            self.stackedLayout = QStackedLayout()
            self.setFixedSize(500,500)

            home = QPushButton('Home', self)
            home.clicked.connect(self.home_on_click)
            imgs = QPushButton('List Images', self)
            ctrs = QPushButton('List Containers', self)
            pods = QPushButton('List Pods', self)
            ctrCreate = QPushButton('Create a Container', self)


            self.page1 = QWidget()
            self.page1Layout = QVBoxLayout()
            self.page1Layout.setSpacing(0)
            self.page1Layout.addWidget(home)
            self.page1Layout.addWidget(imgs)
            self.page1Layout.addWidget(ctrs)
            self.page1Layout.addWidget(pods)
            self.page1Layout.addWidget(ctrCreate)
            self.page1Layout.addStretch(1)
            pageLayouts.append(self.page1Layout)
            pages.append(self.page1)
            self.page1.setLayout(self.page1Layout)
            self.stackedLayout.addWidget(self.page1)

            self.page2 = QWidget()
            self.page2Layout = QVBoxLayout()
            #self.page2Layout.addWidget(home, alignment= Qt.AlignTop)
            self.stackedLayout.addWidget(self.page2)
            pageLayouts.append(self.page2Layout)
            pages.append(self.page2)

            self.page3 = QWidget()
            self.page3Layout = QVBoxLayout()
            #self.page3Layout.addWidget(home, alignment= Qt.AlignTop)
            self.stackedLayout.addWidget(self.page3)
            pageLayouts.append(self.page3Layout)
            pages.append(self.page3)

            self.page4 = QWidget()
            self.page4Layout = QVBoxLayout()
            #self.page4Layout.addWidget(home, alignment= Qt.AlignTop)
            self.stackedLayout.addWidget(self.page4)
            pageLayouts.append(self.page4Layout)
            pages.append(self.page4)

            self.page5 = QWidget()
            self.page5Layout = QHBoxLayout()
            #self.page4Layout.addWidget(home, alignment= Qt.AlignTop)
            self.stackedLayout.addWidget(self.page5)
            pageLayouts.append(self.page5Layout)
            pages.append(self.page5)

        
            imgs.clicked.connect(lambda: self.list_on_click(0, 1))
            ctrs.clicked.connect(lambda: self.list_on_click(1, 2))
            pods.clicked.connect(lambda: self.list_on_click(2, 3))
            ctrCreate.clicked.connect(lambda: self.create_on_click(4))

            layout.addLayout(self.stackedLayout)

        def list_on_click(self, val, ind):
            self.stackedLayout.setCurrentIndex(ind)
            for value in lists[val]:
                pageLayouts[ind].addWidget(QLabel('ID:  '+value.id))
            pageLayouts[ind].addStretch(1)
            pages[ind].setLayout(pageLayouts[ind])

        def create(self, img):
            print(img)
            ctr = client.containers.create(img)
            print(ctr)
            

        
        def create_on_click(self, ind):
            self.stackedLayout.setCurrentIndex(ind)
           # self.page5Layout = QHBoxLayout()
            newBox = QComboBox(self.page5)
            for value in lists[0]:
                newBox.addItem(value.id)
            submit = QPushButton('Create', self)
            self.page5Layout.addWidget(newBox)
            self.page5Layout.addWidget(submit)
            self.page5.setLayout(self.page5Layout)
            submit.clicked.connect(lambda: self.create(newBox.currentText()))
            #newBox.activated[str].connect(self.create)

        def home_on_click(self):
            self.stackedLayout.setCurrentIndex(0)


if __name__ == '__main__':
    layout = QVBoxLayout()
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())