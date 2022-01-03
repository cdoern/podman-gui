from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QTabWidget, QTableWidget, QTableWidgetItem, QApplication, QLineEdit, QStackedLayout, QComboBox, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QPalette, QPixmap
from PyQt5.QtCore import QSize, Qt
import podman
import sys
import urllib.parse
import os
import copy

lists = []
pageLayouts = []
pages = []
tables = []
currentUrl = ''

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
logoPath = os.path.abspath(os.path.join(bundle_dir, 'podman.png'))
stylePath = os.path.abspath(os.path.join(bundle_dir, 'stylesheet.qss'))
activePath = os.path.abspath(os.path.join(bundle_dir, 'active.png'))
inactivePath = os.path.abspath(os.path.join(bundle_dir, 'inactive.png'))
downPath = os.path.abspath(os.path.join(bundle_dir, 'down.png'))



client = podman.PodmanClient()


class Window(QWidget): 
    def __init__(self):
        super().__init__()
        self.setFixedHeight(400)
        self.ping_client()
        self.setWindowTitle("Podman GUI")
        self.setLayout(layout)
        self.left = 10
        self.top = 10
        self.initGUI()

    def initGUI(self):
        global currentUrl
        self.setLayout(layout)
        self.stackedLayout = QStackedLayout()

        imgs = QPushButton('List Images', self)
        ctrs = QPushButton('List Containers', self)
        pods = QPushButton('List Pods', self)
        ctrCreate = QPushButton('Create a Container', self)
        podCreate = QPushButton('Create a Pod', self)

        tableImg = QTableWidget()
        tableImg.setUpdatesEnabled(True)

        tableCtr = QTableWidget()
        tableCtr.setUpdatesEnabled(True)

        tablePod = QTableWidget()
        tablePod.setUpdatesEnabled(True)

        tables.append(tableImg)
        tables.append(tableCtr)
        tables.append(tablePod)

        self.page1 = QWidget()
        self.page1Layout = QVBoxLayout()
        self.page1LayoutSub = QGridLayout()
        self.page1LayoutSub.setHorizontalSpacing(50)
        self.page1LayoutButtons = QVBoxLayout()
        self.page1LayoutButtons.addWidget(imgs)
        self.page1LayoutButtons.addWidget(ctrs)
        self.page1LayoutButtons.addWidget(pods)
        self.page1LayoutButtons.addWidget(ctrCreate)
        self.page1LayoutButtons.addWidget(podCreate)
        self.page1.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                                 QSizePolicy.MinimumExpanding))
        self.page1LayoutSub.addLayout(self.page1LayoutButtons, 0, 0)
        version_report = client.version()
        self.page1LayoutInfo= QVBoxLayout()
        url = urllib.parse.unquote(client.api.base_url.geturl())
        url = url[url.index("+")+1:]
        podmanGUITitle = QLabel("PodmanGUI")
        podmanGUITitle.setFont(QFont('Arial', 20))
        self.page1LayoutInfo.addWidget(podmanGUITitle)
        socketLabel = QLabel("Unix Socket Location: "+url)
        self.page1LayoutInfo.addWidget(QLabel("Podman API Version: "+version_report["Components"][0]["Details"]["APIVersion"]))
        self.page1LayoutInfo.addWidget(socketLabel)
        currentUrl = url
        status = QHBoxLayout()
        status.setSpacing(2)
        status.addWidget(QLabel("Podman Service Status:"))
        active = QLabel()
        active.setPixmap(QPixmap(inactivePath))
        if client.ping():
           active.setPixmap(QPixmap(activePath))
        status.addWidget(active, alignment=Qt.AlignLeft)
        status.addStretch(1)
        self.page1LayoutInfo.addLayout(status)
        podmanPhoto = QPixmap(logoPath)
        logo = QLabel()
        logo.setPixmap(podmanPhoto)
        self.page1LayoutInfo.addWidget(logo)
        socketReset = QHBoxLayout()
        socketReset.setSpacing(5)
        newBox = QLineEdit()
        submit = QPushButton('Reset Socket Location', self)
        submit.clicked.connect(lambda: self.reset_socket(newBox.text(), socketLabel))
        socketReset.addWidget(newBox)
        socketReset.addWidget(submit)
        self.page1LayoutInfo.addLayout(socketReset)
        self.page1LayoutSub.addLayout(self.page1LayoutInfo, 0, 1)
        self.page1LayoutSub.setColumnStretch(1,1)
        self.page1LayoutSub.setVerticalSpacing(0)
        self.page1Layout.addLayout(self.page1LayoutSub)
        self.page1Layout.addStretch(1)
        pageLayouts.append(self.page1Layout)
        pages.append(self.page1)
        self.page1.setLayout(self.page1Layout)
        self.page1.setStyleSheet(open(stylePath).read())
        self.stackedLayout.addWidget(self.page1)

        self.page2 = QWidget()
        self.page2Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page2)
        pageLayouts.append(self.page2Layout)
        pages.append(self.page2)

        self.page3 = QWidget()
        self.page3Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page3)
        pageLayouts.append(self.page3Layout)
        pages.append(self.page3)

        self.page4 = QWidget()
        self.page4Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page4)
        pageLayouts.append(self.page4Layout)
        pages.append(self.page4)

        self.page5 = QWidget()
        self.page5Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page5)
        pageLayouts.append(self.page5Layout)
        pages.append(self.page5)

        self.page6 = QWidget()
        self.page6Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page6)
        pageLayouts.append(self.page6Layout)
        pages.append(self.page6)

        
        imgs.clicked.connect(lambda: self.list_on_click(0, 1))
        ctrs.clicked.connect(lambda: self.list_on_click(1, 2))
        pods.clicked.connect(lambda: self.list_on_click(2, 3))
        ctrCreate.clicked.connect(lambda: self.create_on_click(4))
        podCreate.clicked.connect(lambda: self.create_on_click(5))
        

        layout.addLayout(self.stackedLayout)

    def list_on_click(self, val, ind):
        client = podman.PodmanClient(base_url=currentUrl)
        self.define_lists(client)
        self.stackedLayout.setCurrentIndex(ind)
        pageLayouts[ind].removeWidget(tables[val])
        pageLayouts[ind] = QVBoxLayout()
        home = QPushButton('Home')
        home.clicked.connect(self.home_on_click)
        pageLayouts[ind].addWidget(home, alignment= Qt.AlignTop)  
        out = lists[val]()
        tables[val].clear()
        tables[val].setRowCount(len(out))
        tables[val].setColumnCount(2)
        tables[val].setHorizontalHeaderLabels(('Name', 'ID'))
        for i in range(0, len(out)):
            if ind == 1:
                value = str((out)[i])
                tables[val].setItem(i, 0, QTableWidgetItem(value[value.index(' '):value.index('>')]))
            else:
                value = out[i].name
                tables[val].setItem(i, 0, QTableWidgetItem(value))
            tables[val].setItem(i, 1, QTableWidgetItem(out[i].id))
        tables[val].resizeColumnsToContents()
        tables[val].resizeRowsToContents()
        tables[val].update()
        pageLayouts[ind].addWidget(tables[val])
        pageLayouts[ind].addStretch(1)
        pages[ind].setLayout(pageLayouts[ind])
        pages[ind].setStyleSheet(open(stylePath).read())

    def create(self, ind, name):
        if ind == 4:
            obj = client.containers.create(name)
        else:
            obj = client.pods.create(name)
        print(obj.id)
        pageLayouts[ind].addWidget(QLabel("Created with ID "+obj.id))
        pageLayouts[ind].addStretch(1)
        pages[ind].setLayout(pageLayouts[ind])
            
    def get_data(self, ind, newBox):
        if ind == 4:
            return newBox.currentText()
        return newBox.text()


    def create_on_click(self, ind):
        client = podman.PodmanClient(base_url=currentUrl)
        self.define_lists(client)
        self.stackedLayout.setCurrentIndex(ind)
        pageLayouts[ind] = QVBoxLayout()
        home = QPushButton('Home', self)
        home.clicked.connect(self.home_on_click)
        pageLayouts[ind].addWidget(home, alignment= Qt.AlignTop)
        self.newPageLayout= QHBoxLayout()
        imgs = lists[0]()
        if ind == 4: # container create
            newBox = QComboBox(pages[ind])
            for value in imgs:
                newBox.addItem(value.id)
        else: # pod create 
            newBox = QLineEdit(pages[ind])
        submit = QPushButton('Create', self)
        self.newPageLayout.addWidget(newBox)
        self.newPageLayout.addWidget(submit)
        pageLayouts[ind].addLayout(self.newPageLayout)
        pageLayouts[ind].addStretch(1)
        pages[ind].setLayout(pageLayouts[ind])
        pages[ind].setStyleSheet(open(stylePath).read())
        submit.clicked.connect(lambda: self.create(ind, self.get_data(ind, newBox)))

    def home_on_click(self):
        self.stackedLayout.setCurrentIndex(0)

    def ping_client(self):
        print("** Check Service Available")
        if client.ping():
            print("Service active")
        else:
            print(f"No service found @ {client.base_url}")

    def define_lists(self, client):
        lists.clear
        lists.append(client.images.list)
        lists.append(client.containers.list)
        lists.append(client.pods.list)

    def delete_widgets(self, ind):
        while pageLayouts[ind].count():
            child = pageLayouts[ind].takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def reset_socket(self, newUrl, oldLabel):
        global currentUrl
        currentUrl = newUrl
        self.page1LayoutInfo.replaceWidget(oldLabel, QLabel("Unix Socket Location: "+newUrl))


if __name__ == '__main__':
    layout = QVBoxLayout()
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())